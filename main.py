#importing stuff
import logging
import webapp2
import os
import jinja2
import datetime

from google.appengine.api import users
from google.appengine.ext import ndb
jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

#==================MODELS=======================

class College(ndb.Model):
    name = ndb.StringProperty()
    location = ndb.StringProperty()
    logo_url = ndb.StringProperty()

class Post(ndb.Model):
    user = ndb.StringProperty()
    post_time = ndb.DateTimeProperty(auto_now_add=True)
    title = ndb.StringProperty()
    caption = ndb.StringProperty()
    post_img_url = ndb.StringProperty()
    like_count = ndb.IntegerProperty(default=0)
    dislike_count = ndb.IntegerProperty(default=0)
    view_count = ndb.IntegerProperty(default=0)
    recent_view_count = ndb.IntegerProperty(default=0)
    college_key = ndb.KeyProperty(kind=College)

class Comment(ndb.Model):
    user = ndb.StringProperty()
    content = ndb.StringProperty()
    post_time = ndb.DateTimeProperty(auto_now_add = True)
    post_key = ndb.KeyProperty(kind=Post)

class Like(ndb.Model):
    user = ndb.StringProperty()
    post_key = ndb.KeyProperty(kind=Post)
    like_type = ndb.BooleanProperty()

class View(ndb.Model):
    user = ndb.StringProperty()
    post_key = ndb.KeyProperty(kind=Post)
    view_time = ndb.DateTimeProperty(auto_now_add=True)


#=================HANDLERS===========================


class MainHandler(webapp2.RequestHandler):
    def get(self):
        post_query = Post.query()
        posts = post_query.fetch()
        current_user = users.get_current_user()
        login_url = users.create_login_url('/')
        logout_url = users.create_logout_url('/')
        #===trending calculations===
        views = View.query().fetch()
        time_difference = datetime.datetime.now() - datetime.timedelta(hours=2)
        for post in posts:
            post_key = post.key.urlsafe()
            post.recent_view_count = 0
            for view in views:
                if view.post_key.urlsafe() == post_key and view.view_time > time_difference:
                    post.recent_view_count += 1
                    post.put()
        #order trending
        posts = Post.query().order(-Post.recent_view_count).fetch()
        colleges = College.query().fetch()
        template_vars = {
            "posts": posts,
            "current_user": current_user,
            "logout_url": logout_url,
            "login_url": login_url,
            "colleges": colleges
        }
        template = jinja_environment.get_template('templates/home.html')
        self.response.write(template.render(template_vars))



class PostHandler(webapp2.RequestHandler):
    def get(self):
        #1. Get information from the request
        urlsafe_key = self.request.get("key")
        #2. Pulling the post from the database
        post_key = ndb.Key(urlsafe = urlsafe_key)
        post = post_key.get()
        current_user = users.get_current_user()
        #query, fetch, and filter the comments
        comments = Comment.query().filter(Comment.post_key == post_key).order(Comment.post_time).fetch()
        #Get the number of likes, filter them by post key
        #likes = Like.query().filter(Like.post_key == post_key).fetch()

        #==view counter==
        post.view_count += 1
        post.put()
        views = View.query().fetch()
        view = View(user=current_user.email(), post_key=post_key)
        view.put()
        views = View.query().fetch()

        #========================
        template_vars = {
            "post": post,
            "comments": comments,
            "current_user": current_user,
            'views': views
        }
        template = jinja_environment.get_template("templates/post.html")
        self.response.write(template.render(template_vars))

class NewPostHandler(webapp2.RequestHandler):
    def get(self):
        posts = Post.query().order(-Post.post_time).fetch()
        colleges = College.query().fetch()
        template_vars = {
            'colleges': colleges
        }
        template = jinja_environment.get_template('templates/new_post.html')
        self.response.write(template.render(template_vars))

    def post(self):
        title = self.request.get('title')
        caption = self.request.get('caption')
        post_img_url = self.request.get('post_img_url')
        urlsafe_key = self.request.get('urlsafe_college_key')
        college_key = ndb.Key(urlsafe=urlsafe_key)
        user = users.get_current_user().email()
        if title != "":
            post = Post(user=user, title=title, caption=caption, post_img_url=post_img_url, college_key=college_key)
            post.put()
        self.redirect('/')

class NewCommentHandler(webapp2.RequestHandler):
    def post(self):
        user = ndb.StringProperty()
        content = ndb.StringProperty()
        #1. Getting information from the request
        user = users.get_current_user().email()
        content = self.request.get("content")
        urlsafe_key = self.request.get("post_key")
        #2. Interacting with our Database and APIs
        post_key = ndb.Key(urlsafe=urlsafe_key)
        post = post_key.get()
        #3. Creating Post
        comment = Comment(user=user,content=content, post_key=post_key)
        comment.put()
        url = "/post?key=" + post.key.urlsafe()
        self.redirect(url)

class LikeHandler(webapp2.RequestHandler):
    def post(self):
        user = ndb.StringProperty()
        user = users.get_current_user().email()
        #1. Getting information from the request
        urlsafe_key = self.request.get("post_key")
        #2. Interacting with our Database and APIs
        post_key = ndb.Key(urlsafe = urlsafe_key)
        post = post_key.get()

        if post.like_count == None:
            post.like_count = 0

         # Increase the photo count and update the database.

        post.like_count = post.like_count + 1
        post.put()

        # === 3: Send a response. ===
        # Send the updated count back to the client.
        url = "/post?key=" + post.key.urlsafe()
        self.redirect(url)

class DislikeHandler(webapp2.RequestHandler):
    def post(self):
        user = ndb.StringProperty()
        user = users.get_current_user().email()
        #1. Getting information from the request
        urlsafe_key = self.request.get("post_key")
        #2. Interacting with our Database and APIs
        post_key = ndb.Key(urlsafe = urlsafe_key)
        post = post_key.get()

        if post.dislike_count == None:
            post.dislike_count = 0

         # Increase the photo count and update the database.

        post.dislike_count = post.dislike_count + 1
        post.put()

        # === 3: Send a response. ===
        # Send the updated count back to the client.
        url = "/post?key=" + post.key.urlsafe()
        self.redirect(url)

class CollegeHomeHandler(webapp2.RequestHandler):
    def get(self):
        urlsafe_key = self.request.get('key')
        college_key = ndb.Key(urlsafe=urlsafe_key)
        college = college_key.get()
        posts = Post.query().filter(Post.college_key==college_key).fetch()
        template_vars = {
            'college': college,
            'posts': posts
        }
        template = jinja_environment.get_template('templates/college_home.html')
        self.response.write(template.render(template_vars))

class AddCollegeHomeHandler(webapp2.RequestHandler):
    def get(self):
        colleges = College.query().fetch()
        template_vars = {
            'colleges': colleges
        }
        template = jinja_environment.get_template('templates/add_college.html')
        self.response.write(template.render(template_vars))

    def post(self):
        name = self.request.get('name')
        location = self.request.get('location')
        logo_url = self.request.get('logo_url')

        college = College(name = name, location = location, logo_url= logo_url)
        college.put()
        self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/post', PostHandler),
    ('/new_post', NewPostHandler),
    ('/new_comment', NewCommentHandler),
    ('/like', LikeHandler),
    ('/dislike', DislikeHandler),
    ('/college_home', CollegeHomeHandler),
    ('/add_college', AddCollegeHomeHandler)
], debug=True)
