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
    self.api_root = '/api/'
    self.oauth_root = self.api_root + 'oauth/'

  def execute(self, ircMsg, userRole):
    user = ircMsg.user
    if user == self.last_user:
      self.counter += 1
    else:
      self.counter = 0
      self.last_user = user

    m = IRCMessage()
    word_list = ircMsg.msg.split(' ')
    post = word_list[1]
    m.msg = _("msgIdentiPost").format(user, post)
    self.oauth()
    self.api = tweepy.API(self.auth, host = self.host, api_root = self.api_root)
    self.api.update_status(post[:140])
    
    m.channel = ircMsg.channel
    m.user = user
    m.directed = True
    return m

  def auth(self):
    self.username = ""
    self.password = ""
    self.auth = tweepy.auth.BasicAuthHandler(self.username, self.password)
    self.api = tweepy.API(self.auth, self.host, self.api_root, secure = True)
    self.api.verify_credentials()
    if not self.api.verify_credentials():
      print _("msgIdentiFail")      
    else:
      print _("msgIdentiOk")

  def oauth(self):
    self.consumer_token = "d59d15c57b61cc37be4e4b6f112bac65"
    self.consumer_secret = "bf6e387fb19397d8b842c02a9234e422"
    self.auth = tweepy.OAuthHandler(self.consumer_token, self.consumer_secret, 'oob')
    self.auth.OAUTH_HOST = self.host 
    self.auth.OAUTH_ROOT = self.oauth_root 
    self.auth.secure = True 
    self.access_key = "ff1e4c5f4101caad4abca87aed0d4982"
    self.access_secret = "3ae4d77cc97fa6520fc94203e8de9fd7"
    self.auth.set_access_token(self.access_key, self.access_secret)



