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
    caption = ndb.StringProperty()
    school = ndb.StringProperty()
    post_img_url = ndb.StringProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        post_query = Post.query()
        posts = post_query.fetch()
        template_vars = {
            "posts": posts
        }
        template = jinja_environment.get_template('templates/home.html')
        self.response.write(template.render(template_vars))

class NewPostHandler(webapp2.RequestHandler):
    def get(self):
        posts = Post.query().order(-Post.post_time).fetch()
        template = jinja_environment.get_template('templates/new_post.html')
        self.response.write(template.render())

    def post(self):
        title = self.request.get('title')
        caption = self.request.get('caption')
        user = users.get_current_user().email()
        if title != "":
            post = Post(user=user, title=title, caption=caption)
            post.put()
        self.redirect('/')

class PostHandler(webapp2.RequestHandler):
    def get(self):
        #1. Get information from the request
        #urlsafe_key = self.request.get("key")

        #2. Pulling the post from the database
        #post_key = ndb.Key(urlsafe = urlsafe_key)
        #post = post_key.get()

        #template_vars = {
        #    "post": post,
        #}
        template = jinja_environment.get_template("templates/post.html")
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/post', PostHandler), ('/new_post', NewPostHandler)
], debug=True)
