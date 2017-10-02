import webapp2
import jinja2
import os
import time

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

class Post(db.Model):
    title = db.StringProperty(required=True)
    body = db.TextProperty(required=True)
    author = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

class Handler(webapp2.RequestHandler):
    """Helper function for writing and rendering output
       Code taken from Udacity and Steve Huffman"""
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(Handler):
    """Main entry point into app"""
    def render_front_page(self, title="", body="", author="", error=""):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")

        self.render("front_page.html", title=title, body=body, author=author, error=error, posts=posts)

    def get(self):
        self.render_front_page()

class NewPost(Handler):
    def render_newpost(self, title="", body="", author="Chuck Underwood", error=""):
        self.render("newpost.html", title=title, body=body, author=author, error=error)

    def get(self):
        self.render_newpost()

    def post(self):
        title = self.request.get("title")
        body = self.request.get("body")
        author = self.request.get("author")

        if title and body and author:
            p = Post(title=title, body=body, author=author)
            p.put()

            time.sleep(0.1)
            self.redirect('/')
        else:
            error = "We need a title, body and author"
            self.render_newpost(title, body, author, error)

class Delete(Handler):
    def get(self):
        db.delete(Post.all(keys_only=True))

        time.sleep(0.1)
        self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/newpost/', NewPost),
    ('/delete', Delete)
], debug=True)