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
from handlers import MainHandler
from blog import *

#
# Handlers registrations
#
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/blog/signup', Signup),
    ('/blog/login', Login),
    ('/blog/logout', Logout),
    ('/welcome', Welcome),
    ('/blog/?', FrontBlog),
    ('/blog/newpost', NewPost),
    ('/blog/([0-9]+)', Post),
    ('/blog/([0-9]+).json', JsonPost),
    ('/blog/.json', JsonBlog),
    ('/blog/flush', FlushCache)
], debug=True)
