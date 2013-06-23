# base handler
from handlers import main

# db models
from entities import model

#
# Edit Page Handler
#
class EditPage(main.MainHandler):
	def get(self, path):
		# build the uri for the wiki page
		page_url = self.uri_for('wiki-page', _full=True, page=path[1:])

		# if the wiki page exist, get the content and the title
		wiki_page = model.WikiPage.get_by_url(page_url)
		if wiki_page is not None:
			content = wiki_page.content
			title = wiki_page.title
		else:
			content = ''
			title = path[1:]

		# render the edit page
		self.render('/wiki/edit-page.html', page=path, title=title, content=content)		

	def post(self, path):
		title = self.request.get('wiki-title')
		content = self.request.get('wiki-content')
		page_url = self.uri_for('wiki-page', _full=True, page=path[1:])

		# search for the wiki page in the DB
		wiki_page = model.WikiPage.get_by_url(page_url)

		# if doesn't exist, create new entity
		if wiki_page is None:
			wiki_page = model.WikiPage.create(page_url, title, content)

		# if it already exist, setting the new title and content
		else:
			wiki_page.title = title
			wiki_page.content = content

		# commit the changes in the DB
		wiki_page.put()

		# redirect to the wiki page
		self.redirect_to('wiki-page', page=path[1:])

#
# Wiki Page Handler
#
class WikiPage(main.MainHandler):
	def get(self, page):
		# search for the wiki page in the DB
		url = self.request.url
		wiki_page = model.WikiPage.get_by_url(url)

		# if doesn't exist, redirect to the edit page
		if wiki_page is None:
			self.redirect('/wiki/_edit/' + page)

		# if it already exist, render the wiki page
		else:
			self.render('/wiki/wiki-page.html', page=page, title=wiki_page.title, content=wiki_page.content)

#
# Front Wiki Handler
#
class FrontPage(main.MainHandler):
	def get(self):
		wiki = model.WikiPage.get_all()
		self.render('/wiki/wiki-front.html', wiki=wiki)