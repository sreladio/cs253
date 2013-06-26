#
# Requires that a user be logged in to access the resource
#
def login_required(handler):
  def check_login(self, *args, **kwargs): 
    logged = self.is_logged()
    if logged is None:
      return self.redirect('/login')
    else:
      return handler(self, *args, **kwargs)

  return check_login

#
# Pass through if user is already logged
#
def already_logged(handler):
  def check_login(self, *args, **kwargs): 
    logged = self.is_logged()
    if logged:
      return self.redirect('/welcome')
    else:
      return handler(self, *args, **kwargs)

  return check_login