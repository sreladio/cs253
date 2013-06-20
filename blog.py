import logging
import time

from google.appengine.api import memcache

# base handler
from handlers import MainHandler

# db models
from entities import model

# utils
from utils import validation
from utils import encryption

# Global variables
UPDATE_CACHE = True
post_query_creation_time = 0
blog_query_creation_time = 0

#
# Signup handler
#
class Signup(MainHandler):
  def get(self):
    self.on_load('signup.html', '/welcome')

  def post(self):
    valid_form = True
    errors = {}

    u = self.request.get("username")
    p = self.request.get("password")
    v = self.request.get("verify")
    e = self.request.get("email")

    # grab the user and email input
    errors = dict({'username':u, 'email':e })

    # check if form fields are valid
    if not validation.valid_username(u):
      errors['username_error'] = "Invalid username"
      valid_form = False

    if not validation.valid_password(p, v):
      errors['password_error'] = "Invalid password"
      valid_form = False

    if not validation.valid_email(e):
      errors['email_error'] = "Invalid email"
      valid_form = False

    if validation.empty_email(e):
        e = None

    # check if user already exist
    user = model.User.get_by_name(u)
    if user is not None:
      if user.name ==  u:
        errors['username_error'] = "That user name already exist"
        valid_form = False

    # register user
    if valid_form:
      
      # hash a password
      pwd_hash = encryption.hash(p)

      # create the entitie and store in the D.B
      new_user = model.User.create(u, pwd_hash, e)
      new_user.put()

      # set cookie and redirect
      self.init_user(new_user)

    else:
      self.render('signup.html', **errors)

#
# Login Handler
#
class Login(MainHandler):
  def get(self):
    self.on_load('login.html', '/welcome')

  def post(self):
    # get the username and pass from the request
    username = self.request.get('username')
    password = self.request.get('password')
    message = dict({'username':username})

    # search for that user in the DB
    user = model.User.get_by_name(username)

    # check if user exist
    if not user:
      message['username_error'] = 'Name incorect'

    # check if password matches
    elif self.check_cookie(password, user.password):
        self.init_user(user)       

    else:
        message['password_error'] = 'Password incorect'    

    self.render('login.html', **message)

#
# Logout Handler
#
class Logout(MainHandler):
  def get(self):
    self.set_cookie('user_id')
    self.redirect('/blog/signup')

#
# Welcome Handler
#
class Welcome(MainHandler):
  def get(self):
    # get the cookie
    user_id, user_id_hash = self.get_cookie('user_id')
    logged = self.is_logged()
    if logged:
      # search for the ID in the data base
      user = model.User.get_by_id(user_id)
      # render the page
      if user:
        self.render('welcome.html', username=user.name, logged=True)
      else:
        self.error(404)
        return
    else:
      self.redirect('/blog/signup')

#
# Front Blog handler
#
class FrontBlog(MainHandler):
  def get(self):
    global UPDATE_CACHE, blog_query_creation_time

    logged = self.is_logged()
    posts = memcache.get('posts')
    
    if not posts or UPDATE_CACHE:    
      #logging.error("CACHEANDO BASE DE DATOS")
      posts = model.Post.get_all()
      memcache.set('posts', posts)
      UPDATE_CACHE = False
      blog_query_creation_time = time.time()
      
    current_time = time.time()
    last_time_query = round((current_time - blog_query_creation_time), 3)
    #logging.error('TIEMPO ULTIMA CONSULTA: ' + str(last_time_query))
    self.render('blog.html', posts=posts, query_time_stat=last_time_query, logged=logged)

#
# New Post handler
#
class NewPost(MainHandler):
  def get(self):
    self.render('newpost.html', logged=self.is_logged())

  def post(self):
    global UPDATE_CACHE

    subject = self.request.get("subject")
    content = self.request.get("content")
    messages = dict({'subject':subject, 'content':content})

    if subject == '' or content == '':
      messages['error'] = 'Subject and content, please!'
      self.render('newpost.html', **messages)
    else:  
      post = model.Post.create(subject, content)
      post.put()
      memcache.flush_all()
      UPDATE_CACHE = True
      self.redirect('/blog/' + str(post.key().id()), permanent=True)

#
# Post handler
#
class Post(MainHandler):
  def get(self, post_id):
    global post_query_creation_time

    post = memcache.get(post_id)
    logged = self.is_logged()

    if post is None:
      post = model.Post.get_by_id(long(post_id))
      if post:
        #logging.error('CACHEANDO POST')
        memcache.set(post_id, post)
        post_query_creation_time = time.time()
      else:
        self.error(404)
    
    current_time = time.time()
    last_time_query = round((current_time - post_query_creation_time), 3)
    values = {"subject":post.subject, "date":post.date, "content":post.content}
    self.render('blogentry.html', query_time_stat=last_time_query, logged=logged, **values)


  def post(self, post_id):
    self.get(post_id)

#
# JSON Post Handler
#
class JsonPost(MainHandler):
  def get(self, post_id):
    post = model.Post.get_by_id(long(post_id))
    if post:
      post_dic = self.parse_post(post)
      self.write_json(post_dic)
    else:
      self.error(404)

  def parse_post(self, post):
    return dict({'subject':post.subject, 'content':post.content})

#
# JSON Blog Handler
#
class JsonBlog(JsonPost):
  def get(self):
    posts = model.Post.get_all()
    blog_lis = []
    for post in posts:
      post_dic = self.parse_post(post)
      blog_lis.append(post_dic)
    self.write_json(blog_lis)

#
# Flush MEMCACHE Handler
#
class FlushCache(MainHandler):
  def get(self):
    memcache.flush_all()
    self.redirect('/blog')