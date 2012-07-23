import cgi
import datetime
import urllib
import wsgiref.handlers
import time
import hashlib
import os
import socket


from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class Viewers(db.Model):
  email    = db.StringProperty(multiline=False)
  fullName = db.StringProperty(multiline=False)
  time     = db.FloatProperty()
  date     = db.DateTimeProperty(auto_now_add=True)


class Log(db.Model):
  email    = db.StringProperty(multiline=False)
  fullName = db.StringProperty(multiline=False)
  ip       = db.StringProperty(multiline=False)
  city     = db.StringProperty(multiline=False)
  state    = db.StringProperty(multiline=False)
  country  = db.StringProperty(multiline=False)
  date     = db.DateTimeProperty(auto_now_add=True)


class Deck(webapp.RequestHandler):
  def get(self):
    userHash = ''
    deckUser = db.GqlQuery("SELECT * "
                              "FROM Viewers "
                              "WHERE email ='" + self.request.get('email') + "' "
                              "ORDER BY date DESC LIMIT 1",
                              )

    for user in deckUser:
      userHash = hashlib.sha224(user.email + '%s' % user.time).hexdigest()

      if userHash == self.request.get('x'):
        template_values = {
            'user': user
        }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))
      else:
        self.response.out.write('Expired. Please contact david@alpinereplay.com')

class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.out.write('<html><body>')
    self.response.out.write("""
          <form action="/add" method="post">
            <div>Email</div>
            <div><textarea name="email" rows="1" cols="80"></textarea></div>
            <div>Full Name</div>
            <div><textarea name="fullName" rows="1" cols="80"></textarea></div>
            <div><input type="submit" value="Add User"></div>
          </form>
        </body>
      </html>""")


class Printing(webapp.RequestHandler):
  def get(self):
    allLogs = db.GqlQuery("SELECT * "
                              "FROM Log"
                              )

    for log in allLogs:
      self.response.out.write(log.fullName + '*' + log.email + '*' + log.ip + '*' + log.state + ' and ' + log.country)


class Logging(webapp.RequestHandler):
  def post(self):
    log   = Log()

    log.email    = self.request.get('email')
    log.fullName = self.request.get('name')
    log.ip       = self.request.remote_addr
    log.city     = self.request.get('city')
    log.country  = self.request.get('country')
    log.state    = self.request.get('state')
    log.put()


class Userbook(webapp.RequestHandler):
  def post(self):

    viewers       = Viewers()

    timestamp        = time.mktime(time.localtime())
    viewers.email    = self.request.get('email')
    viewers.fullName = self.request.get('fullName')
    viewers.time     = timestamp
    viewers.put()

    userHash      = hashlib.sha224(self.request.get('email') + '%s' %timestamp).hexdigest()
    self.redirect('/display?email=' + self.request.get('email') + '&x=%s' %userHash)


class UniqueURL(webapp.RequestHandler):
  def get(self):
    self.response.out.write('The uniquer URL for this user is: http://deck.alpinereplay.com/?email=%s&x=%s' %(self.request.get('email'), self.request.get('x')))

application = webapp.WSGIApplication([
  ('/hb92648', MainPage),
  ('/add', Userbook),
  ('/display', UniqueURL),
  ('/log', Logging),
  ('/printlog', Printing),
  ('/', Deck)
], debug=True)


def main():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()
