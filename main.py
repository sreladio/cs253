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

# handlers
from handlers import main
from handlers import blog
from handlers import login

#
# Handlers registrations
#
app = webapp2.WSGIApplication([
    ('/', main.MainHandler),

    ('/blog/signup', login.Signup),
    ('/blog/login', login.Login),
    ('/blog/logout', login.Logout),
    ('/welcome', login.Welcome),

    ('/blog/?', blog.FrontPage),
    ('/blog/newpost', blog.NewPost),
    ('/blog/([0-9]+)', blog.Post),
    ('/blog/([0-9]+).json', blog.JsonPost),
    ('/blog/.json', blog.JsonBlog),
    
    ('/blog/flush', blog.FlushCache)
], debug=True)
