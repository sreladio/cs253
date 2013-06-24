import logging

# base handler
from handlers import main

# db models
from entities import model

# utils
from utils import validation
from utils import encryption

def login_required(handler):
  "Requires that a user be logged in to access the resource"

  def check_login(self, *args, **kwargs): 
    logged = self.is_logged()
    if not logged:
      return self.redirect('/login')
    else:
      return handler(self, *args, **kwargs)

  return check_login

def already_logged(handler):
  "Pass through if user is already logged"

  def check_login(self, *args, **kwargs): 
    logged = self.is_logged()
    if logged:
      return self.redirect('/welcome')
    else:
      return handler(self, *args, **kwargs)

  return check_login

#
# Signup handler
#
class Signup(main.MainHandler):
  @already_logged
  def get(self):
    self.render('signup.html')

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
    if user:
      if user.name ==  u:
        errors['username_error'] = "That user name already exist"
        valid_form = False

    # register user
    if valid_form:
  
      # create the entitie and store in the D.B
      new_user = model.User.create(u, p, e)
      new_user.put()

      # set cookie and redirect
      self.init_user(new_user)

    else:
      self.render('signup.html', **errors)

#
# Login Handler
#
class Login(main.MainHandler):
  @already_logged
  def get(self):
    self.render('login.html')

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
class Logout(main.MainHandler):
  def get(self):
    self.set_cookie('user_id')
    self.redirect('/signup')

#
# Welcome Handler
#
class Welcome(main.MainHandler):
  @login_required
  def get(self):
    # get the cookie
    user_id, user_id_hash = self.get_cookie('user_id')

    # search for the ID in the data base
    user = model.User.get_by_id(user_id)
    
    # render the page
    if user:
      self.render('welcome.html', username=user.name, logged=True)
    else:
      self.error(404)
      return



    