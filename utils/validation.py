import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
MAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
	return USER_RE.match(username)

def valid_password(password, verify):
    return PASS_RE.match(password) and password == verify

def valid_email(email):
	if email == '' or email == None:
		return True
	else:
		return MAIL_RE.match(email)

def empty_email(email):
	if email == '' or email == None:
		return True
	else:
		return False

# no use since jinja2 is use for render 
# the html pages
def escape_html(s):
	if '&' in s:
		s = s.replace('&', '&amp;')
	if '>' in s:
		s = s.replace('>', '&gt;')
	if '<' in s:
		s = s.replace('<', '&lt;')
	if '"' in s:
		s = s.replace('"', '&quot;')
	return s