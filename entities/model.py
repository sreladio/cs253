from google.appengine.ext import db

# utils
from utils import encryption

#
# Entitie Post
#
class Post(db.Model):
	subject = db.StringProperty()
  	content = db.TextProperty()
  	date = db.DateProperty(auto_now_add=True)

  	@classmethod
  	def create(cls, subject, content):
  		return Post(subject = subject, content = content)

  	@classmethod
  	def get_all(cls):
  		return db.GqlQuery("SELECT * FROM Post ORDER BY date DESC")

#
# Entitie User
#
class User(db.Model):
	name = db.StringProperty()
	password = db.StringProperty()
	email = db.EmailProperty(default=None)

	def get_id(self):
		return self.key().id()

	@classmethod
	def create(cls, name, password, email=None):
		hashed_password = encryption.hash(password)
		return User(name=name, password=hashed_password, email=email)

	@classmethod
	def get_by_name(cls, name):
		query = db.Query(User)
		query.filter('name = ', name)
		return query.get()

	@classmethod
	def get_by_pswd(cls, pswd):
		query = db.Query(User)
		query.filter('password =', pswd)
		returnquery.get()

	@classmethod
	def get_by_id(cls, user_id):
		key = db.Key.from_path('User', int(user_id))
		return db.get(key)

#
# Entitie WikiPage
#
class WikiPage(db.Model):
	url = db.LinkProperty()
	title = db.StringProperty()
	content = db.TextProperty()
	created = db.DateProperty(auto_now_add=True)
	version = db.IntegerProperty()

  	def get_version_record(self):
  		return self.version_record
  		
	@classmethod
	def get_by_url(cls, url):
		query = db.Query(WikiPage)
		query.filter('url = ', url)
		return query.get()

	@classmethod
	def create(cls, url, title, content):
		return WikiPage(url=url, title=title, content=content, version=1)

	@classmethod
  	def get_all(cls):
  		return db.GqlQuery("SELECT * FROM WikiPage ORDER BY created DESC")

#
# Entity Wiki Page Version Record
#
class WikiPageVersionRecord(db.Model):
	wiki_page = db.ReferenceProperty(WikiPage, collection_name='version_record')
	url = db.LinkProperty()
	title = db.StringProperty()
	content = db.TextProperty()
	created = db.DateProperty(auto_now_add=True)
	version = db.IntegerProperty()
 
 	@classmethod
 	def create(cls, wiki_page):
 		url = wiki_page.url
 		title = wiki_page.title
 		content = wiki_page.content
		version = wiki_page.version
		return WikiPageVersionRecord(wiki_page=wiki_page, url=url, title=title, 
									 content=content, version=version)
