#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re

# handlers
from handlers import main
from handlers import blog
from handlers import auth
from handlers import wiki

# wiki page url pattern
PAGE_RE = r'((?:[a-zA-Z0-9_-]+/?)*)'
    
#
# Handlers registrations
#
app = webapp2.WSGIApplication([
    ('/', main.MainHandler),

    ('/signup/?', auth.Signup),
    ('/login/?', auth.Login),
    ('/logout/?', auth.Logout),
    ('/welcome/?', auth.Welcome),

    ('/blog/?', blog.FrontPage),
    ('/blog/newpost', blog.NewPost),
    ('/blog/([0-9]+)', blog.Post),
    ('/blog/([0-9]+).json', blog.JsonPost),
    ('/blog/.json', blog.JsonBlog),
    
    ('/blog/flush', blog.FlushCache),

    
    ('/wiki/_edit/' + PAGE_RE, wiki.EditPage),
    ('/wiki/_history/' + PAGE_RE, wiki.HistoryPage),
    webapp2.Route('/wiki/<page>', wiki.WikiPage, name='wiki-page'),
    ('/wiki/?', wiki.FrontPage),

], debug=True)


