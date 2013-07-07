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
		wiki_page = self.get_wiki_page(page, version)

		# if doesn't exist, redirect to the edit page
		if wiki_page is None:
			self.redirect('/wiki/_edit/' + page)

		# if it already exist, render the wiki page
		else:
			content = markdown.markdown(wiki_page.content)
			params = {'page':page, 
					  'version':version, 
					  'title':wiki_page.title, 
					  'content':content}
			self.render('/wiki/wiki-page.html', **params)

	def get_wiki_page(self, page, version):
		url = self.buid_wiki_page_url(page)
		if version:
			return self.get_old_version(url, version)
		else:
			return self.get_latest_version(url)

	def get_old_version(self, url, version):
		version_record = self.get_wiki_page_version_record(url)
		version_record.filter('version = ', int(version))
		return version_record.get()

	def get_latest_version(self, url):
		return model.WikiPage.get_by_url(url)

	def get_wiki_page_version_record(self, url):
		wiki_page = self.get_latest_version(url)
		version_record = wiki_page.version_record
		return version_record.order('version')

	def buid_wiki_page_url(self, page):
		return self.uri_for('wiki-page', _full=True, page=page)

#
# Edit Page Handler
#
class EditPage(WikiPage):
	@decorator.login_required
	def get(self, page, error=""):		
		version = self.request.get('v')
		wiki_page = self.get_wiki_page(page, version)
		
		# if the wiki page exist, get the content and the title
		if wiki_page is not None:
			content = wiki_page.content
			title = wiki_page.title
		else:
			content = ''
			title = page

		# render the edit page
		params = {'page':page, 'title':title, 'content':content, 'error':error}
		self.render('/wiki/edit-page.html', **params)		

	def post(self, page):
		title = self.request.get('wiki-title')
		content = self.request.get('wiki-content')

		# check for empty title or content
		if title == '' or content == '':
			error = 'Title and content, please!'
			self.get(page, error)
			return

		# before doing anything, sanitize the input
		# deleting all html tags
		content = validation.delete_html_tags(content)
		
		# get the wiki page from the DB
		wiki_page = self.get_wiki_page(page, None)

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
		self.redirect_to('wiki-page', page=page)

#
# History Page Handler
#
class HistoryPage(WikiPage):
	def get(self, page):
		# build the url
		page_url = self.buid_wiki_page_url(page)

		# get the version record of the wiki page
		version_record = self.get_wiki_page_version_record(page_url)

		# render
		self.render('/wiki/history_page.html', version_record=version_record)

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