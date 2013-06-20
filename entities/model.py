from google.appengine.ext import db

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

class User(db.Model):
	name = db.StringProperty()
	password = db.StringProperty()
	email = db.EmailProperty(default=None)

	# @staticmethod probar que esta etiqueta funciona bien
	def get_id(self):
		return self.key().id()

	@classmethod
	def create(cls, name, password, email=None):
		return User(name = name, password = password, email = email)

	@classmethod
	def get_by_name(cls, name):
		query = db.Query(User)
		query.filter('name = ', name)
		return query.get()

	@classmethod
	def get_by_id(cls, user_id):
		key = db.Key.from_path('User', int(user_id))
		return db.get(key)