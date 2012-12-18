from yapsy.IPlugin import IPlugin
from ircmessage import IRCMessage
from plugins.lengua import _
from ConfigParser import SafeConfigParser
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
    
    try:
      parser = SafeConfigParser()
      parser.read('plugins/identica.yapsy-plugin')
      self.consumer_token = parser.get('Auth', 'consumer_token')
      self.consumer_secret = parser.get('Auth', 'consumer_secret')
      self.access_key = parser.get('Auth', 'access_key')
      self.access_secret = parser.get('Auth', 'access_secret')
    except:
      print "Error", sys.exc_info()


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
    self.auth = tweepy.OAuthHandler(self.consumer_token, self.consumer_secret, 'oob')
    self.auth.OAUTH_HOST = self.host 
    self.auth.OAUTH_ROOT = self.oauth_root 
    self.auth.secure = True 
    self.auth.set_access_token(self.access_key, self.access_secret)
    
  def activate(self):
    super(identica, self).activate()
    print _("msgIdentiEn")


  def deactivate(self):
    super(identica, self).deactivate()
    print_("msgIdentiDis")

