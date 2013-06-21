import time

from google.appengine.api import memcache

# base handler
from handlers import main

# db models
from entities import model

# Global variables
update_cache = True
post_query_creation_time = 0
blog_query_creation_time = 0

def time_since(initial_time):
  current_time = time.time()
  return round((current_time - initial_time), 3)

#
# Front Blog handler
#
class FrontPage(main.MainHandler):
  def get(self):
    global update_cache, blog_query_creation_time

    logged = self.is_logged()
    posts = memcache.get('posts')
    
    if not posts or update_cache:    
      posts = model.Post.get_all()
      memcache.set('posts', posts)
      update_cache = False
      blog_query_creation_time = time.time()
      
    time_from_last_query = time_since(blog_query_creation_time)
    template_values = {"posts":posts, 
                       "query_time_stat":time_from_last_query, 
                       "logged":logged}

    self.render('/blog/blog-front.html', **template_values)

#
# New Post handler
#
class NewPost(main.MainHandler):
  def get(self):
    logged = self.is_logged()
    self.render('/blog/new-post.html', logged=logged)

  def post(self):
    global update_cache

    subject = self.request.get("subject")
    content = self.request.get("content")
    messages = dict({'subject':subject, 'content':content})

    if subject == '' or content == '':
      messages['error'] = 'Subject and content, please!'
      self.render('/blog/new-post.html', **messages)
    else:  
      post = model.Post.create(subject, content)
      post.put()
      memcache.flush_all()
      update_cache = True
      self.redirect('/blog/' + str(post.key().id()), permanent=True)

#
# Post handler
#
class Post(main.MainHandler):
  def get(self, post_id):
    global post_query_creation_time

    logged = self.is_logged()
    post = memcache.get(post_id)
    
    if not post or update_cache:
      post = model.Post.get_by_id(long(post_id))
      if post:
        memcache.set(post_id, post)
        post_query_creation_time = time.time()
      else:
        self.error(404)
        return
    
    time_from_last_query = time_since(blog_query_creation_time)

    values = {"subject":post.subject, 
              "date":post.date, 
              "content":post.content,
              "query_time_stat":time_from_last_query, 
              "logged":logged
              
              }

    self.render('/blog/blog-post.html', **values)

  def post(self, post_id):
    self.get(post_id)

#
# JSON Post Handler
#
class JsonPost(main.MainHandler):
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
class FlushCache(main.MainHandler):
  def get(self):
    memcache.flush_all()
    self.redirect('/blog')