from yapsy.IPlugin import IPlugin
from ircmessage import IRCMessage
from plugins.lengua import _
import tweepy
from tweepy import OAuthHandler
import sys

class identica(IPlugin):

  # This constructor is optional
  def __init__(self):
    self.threshold = 3
    self.counter = 0
    self.last_user = ""
    self.host = 'identi.ca'
    self.api_root = '/api'
    self.without_aut()

  def execute(self, ircMsg, userRole):
    user = ircMsg.user
    if user == self.last_user:
      self.counter += 1
    else:
      self.counter = 0
      self.last_user = user

    m = IRCMessage()
    self.api.update_status("Probando desde chema2 esto: " + self.user )

#    m.msg = _("msgSalida").format(self.counter)

    m.channel = ircMsg.channel
    m.user = user
    m.directed = True
    return m

  def with_auth(self):
    self.username = ""
    self.password = ""
    self.auth = tweepy.auth.BasicAuthHandler(self.username, self.password)
    self.api = tweepy.API(self.auth, self.host, self.api_root, secure = True)
    self.api.verify_credentials()
    if not self.api.verify_credentials():
      print _("msgIdentiFail")      
    else:
      print _("msgIdentiOk")

  def without_aut(self):
    self.oauth_root = self.api_root + 'oauth/'
    self.consumer_token = "d59d15c57b61cc37be4e4b6f112bac65e"
    self.consumer_secret = "bf6e387fb19397d8b842c02a9234e422e"

    try:
      self.auth = tweepy.OAuthHandler(self.consumer_token, self.consumer_secret)
      # self.auth.OAUTH_HOST = self.host
      # self.auth.OAUTH_ROOT = self.oauth_root
      # self.auth.secure = True  
      redirect_url = self.auth.get_authorization_url()
      print redirect_url    
    except:
      print _("msgToken")
      print "x",sys.exc_info()[0]
    
    # req_key = self.auth.request_token.key
    # req_secret = self.auth.request_token.secret


