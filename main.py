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
    school = ndb.StringProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        post_query = Post.query().order(-Post.post_time)
        posts = post_query.fetch()
    
        template = jinja_environment.get_template('templates/home.html')
        self.response.write(template.render(template_vars))

class NewPostHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/new_post.html')
        self.response.write(template.render())


class PostHandler(webapp2.RequestHandler):
    def get(self):
        template_vars = {
            "post": post,
        }
        template = jinja_environment.get_template("templates/post.html")
        self.response.write(template.render(template_vars))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/new_post', NewPostHandler)
], debug=True)
