import os
import webapp2
import jinja2
import json

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
    logged = self.is_logged()
    self.render('index.html', logged=logged)

  def write(self, a):
    self.response.out.write(a)

  def write_json(self, data):
    json_object = json.dumps(data)
    self.response.headers["Content-Type"] = "application/json"
    self.write(json_object)

  def render(self, template, **params):
    t = jinja_environment.get_template(template)
    self.write(t.render(params))

  def init_user(self, user):
    # make the cookie
    cookie_value = self.make_cookie(user)
    # add the cookie in the header request
    self.set_cookie('user_id', cookie_value)
    # redirect to welcome page
    self.redirect('/welcome')

  def is_logged(self):
    val, hash_val = self.get_cookie('user_id')
    if not val and not hash_val:
      return False
    else:
      return self.check_cookie(val, hash_val)

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