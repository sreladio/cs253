import os
import webapp2
import jinja2
import json

# db models
from entities import model

# utils
from utils import encryption

# Global variables
jinja_environment = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../templates')))

#
# Main Handler
#
class MainHandler(webapp2.RequestHandler):
  def get(self):
    self.render('index.html')

  def write_html(self, a):
    self.response.out.write(a)

  def write_json(self, data):
    json_object = json.dumps(data)
    self.response.headers["Content-Type"] = "application/json"
    self.write_html(json_object)

  def render(self, template, **params):
    t = jinja_environment.get_template(template)

    # this need to be refactored to avoid the 
    # query every time a page is rendered when
    # a user is logged
    user_id = self.is_logged()
    username = None

    if user_id:
      user = model.User.get_by_id(user_id)
      username = user.name

    params['logged'] = username
    self.write_html(t.render(params))

  def init_user(self, user):
    # make the cookie
    cookie_value = self.make_cookie(user)
    # add the cookie in the header request
    self.set_cookie('user_id', cookie_value)
    # redirect to welcome page
    self.redirect('/welcome')

  # return the user_id if the user is logged
  def is_logged(self):
    val, hash_val = self.get_cookie('user_id')
    if not val and not hash_val:
      return None
    elif self.check_cookie(val, hash_val) is False:
      return None
    else:
      return val

  def make_cookie(self, user):
    user_id = str(user.get_id())
    user_id_hash = encryption.hash(user_id)
    return user_id + '|' + user_id_hash

  def set_cookie(self, name="", value=""):
    self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/' %(name, value))

  def check_cookie(self, user_id, user_id_hash):
    return encryption.valid_hash(user_id, user_id_hash)

  def get_cookie(self, name):
    cookie = self.request.cookies.get(name, 0)
    if cookie:
      val = cookie.split('|')[0]
      hash_val = cookie.split('|')[1]
      return val, hash_val
    else:
      return None, None