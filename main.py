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

class Comment(ndb.Model):
    user = ndb.StringProperty()
    content = ndb.StringProperty()
    post_time = ndb.DateTimeProperty(auto_now_add = True)
    post_key = ndb.KeyProperty(kind=Post)

class Like(ndb.Model):
    user = ndb.StringProperty()
    numLikes = ndb.IntegerProperty()
    post_key = ndb.KeyProperty(kind=Post)

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
        post_img_url = self.request.get('post_img_url')
        user = users.get_current_user().email()
        if title != "":
            post = Post(user=user, title=title, caption=caption, post_img_url=post_img_url)
            post.put()
        self.redirect('/')

class PostHandler(webapp2.RequestHandler):
    def get(self):
        #1. Get information from the request
        urlsafe_key = self.request.get("key")

        #2. Pulling the post from the database
        post_key = ndb.Key(urlsafe = urlsafe_key)
        post = post_key.get()

        comment_query = Comment.query()
        comments = comment_query.fetch()

        template_vars = {
            "post": post,
            "comments": comments
        }
        template = jinja_environment.get_template("templates/post.html")
        self.response.write(template.render(template_vars))

class NewCommentHandler(webapp2.RequestHandler):
    def post(self):
        user = ndb.StringProperty()
        content = ndb.StringProperty()

        #1. Getting information from the request
        user = self.request.get("user")
        content = self.request.get("content")
        urlsafe_key = self.request.get("post_key")

        #2. Interacting with our Database and APIs
        post_key = ndb.Key(urlsafe = urlsafe_key)
        post = post_key.get()

        #3. Creating Post
        comment = Comment(user=user,content=content, post_key=post_key)

        comment.put()
        url = "/post?key=" + post.key.urlsafe()
        self.redirect(url)

class LikeHandler(webapp2.RequestHandler):
    def post(self):
        user = ndb.StringProperty()
        numLikes = ndb.IntegerProperty()

        #1. Getting information from the request
        user = self.request.get("user")
        content = self.request.get("content")
        urlsafe_key = self.request.get("post_key")

        #2. Interacting with our Database and APIs
        post_key = ndb.Key(urlsafe = urlsafe_key)
        post = post_key.get()

        #3. Creating Post
        like = Like(user=user,numLikes=numLikes, post_key=post_key)

        like.put()
        url = "/post?key=" + post.key.urlsafe()
        self.redirect(url)

app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/post', PostHandler), ('/new_post', NewPostHandler),
    ('/new_comment', NewCommentHandler), ('/like', LikeHandler)
], debug=True)
