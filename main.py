#importing stuff
import webapp2
import os
import jinja2

from google.appengine.api import users
from google.appengine.ext import ndb

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Post(ndb.Model):
    user = ndb.StringProperty()
    post_time = ndb.DateTimeProperty(auto_now_add=True)
    title = ndb.StringProperty()
    content = ndb.StringProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        meme = ndb.StringProperty()
        post_time = ndb.DateTimeProperty(auto_now_add=True)
        
        template = jinja_environment.get_template('templates/home.html')
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)

class PostHandler(webapp2.RequestHandler):
    def get(self):
        template_vars = {
            "post": post,
        }
        template = jinja_environment.get_template("templates/post.html")
        self.response.write(template.render(template_vars))
