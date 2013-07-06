# base handler
from handlers import main

# db models
from entities import model

# utils
from utils import decorator
from utils import validation

# lib
from lib import markdown

#
# Wiki Page Handler
#
class WikiPage(main.MainHandler):
	def get(self, page):

		# search for the wiki page in the DB
		version = self.request.get('v')
		if version:
			wiki_page = self.get_old_version(version)
		else:
			wiki_page = self.get_latest_version()

		# if doesn't exist, redirect to the edit page
		if wiki_page is None:
			self.redirect('/wiki/_edit/' + page)

		# if it already exist, render the wiki page
		else:
			content = markdown.markdown(wiki_page.content)
			self.render('/wiki/wiki-page.html', page=page, version=version, title=wiki_page.title, content=content)

	def get_old_version(self, version):
		url = self.request.url.split('?')[0]
		version_record = self.get_wiki_page_version_record(url)
		version_record.filter('version = ', int(version))
		return version_record.get()

	def get_latest_version(self):
		url = self.request.url
		return self.get_wiki_page(url)

	def get_wiki_page(self, url):
		return model.WikiPage.get_by_url(url)

	def get_wiki_page_version_record(self, url):
		wiki_page = self.get_wiki_page(url)
		version_record = wiki_page.version_record
		return version_record.order('version')

#
# Edit Page Handler
#
class EditPage(WikiPage):
	@decorator.login_required
	def get(self, path, error=""):

		page_url = self.uri_for('wiki-page', _full=True, page=path[1:])
		wiki_page = self.get_wiki_page(page_url)

		version = self.request.get('v')
		if version:
			version_record = self.get_wiki_page_version_record(page_url)
			version_record.filter('version = ', int(version))
			wiki_page = version_record.get()
		else:
			wiki_page = model.WikiPage.get_by_url(page_url)
		
		# if the wiki page exist, get the content and the title
		if wiki_page is not None:
			content = wiki_page.content
			title = wiki_page.title
		else:
			content = ''
			title = path[1:]

		# render the edit page
		self.render('/wiki/edit-page.html', page=path, title=title, content=content, error=error)		

	def post(self, path):
		title = self.request.get('wiki-title')
		content = self.request.get('wiki-content')
		page_url = self.uri_for('wiki-page', _full=True, page=path[1:])

		if title == '' or content == '':
			error = 'Title and content, please!'
			self.get(path, error)
			return

		# before doing anything, sanitize the input
		# deleting all html tags
		content = validation.delete_html_tags(content)

		# search for the wiki page in the DB
		wiki_page = model.WikiPage.get_by_url(page_url)

		# if doesn't exist, create new entity
		if wiki_page is None:
			wiki_page = model.WikiPage.create(page_url, title, content)

		# if it already exist, setting the new title and content
		else:
			wiki_page.title = title
			wiki_page.content = content
			wiki_page.version += 1

		# commit the changes in the DB
		wiki_page.put()

		# update de versions record
		model.WikiPageVersionRecord.create(wiki_page=wiki_page).put()

		# redirect to the wiki page
		self.redirect_to('wiki-page', page=path[1:])

#
# Front Wiki Handler
#
class FrontPage(main.MainHandler):
	def get(self):
		wiki = self.get_wiki()
		self.render('/wiki/wiki-front.html', wiki=wiki)

	def get_wiki(self):
		wiki = list(model.WikiPage.get_all())
		for i in range(len(wiki)):
			wiki[i].content = markdown.markdown(wiki[i].content)
		return wiki

#
# History Page Handler
#
class HistoryPage(WikiPage):
	def get(self, page):
		# build the url
		page_url = self.uri_for('wiki-page', _full=True, page=page[1:])

		# get the version record of the wiki page
		version_record = self.get_wiki_page_version_record(page_url)

		# render
		self.render('/wiki/history_page.html', version_record=version_record)