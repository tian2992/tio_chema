from plugins.baseactionplugin import BaseActionPlugin
from ircmessage import IRCMessage
from plugins.lengua import _

from ConfigParser import SafeConfigParser
import tweepy
from tweepy import OAuthHandler
import re

class PluginIdentica(BaseActionPlugin):

  def __init__(self):
    self.host = 'identi.ca'
    self.api_root = '/api/'
    self.oauth_root = self.api_root + 'oauth/'
    self.local_name = 'identica'

    try:
      parser = SafeConfigParser()
      parser.read('plugins/identica.yapsy-plugin')
      self.consumer_token = parser.get('Auth', 'consumer_token')
      self.consumer_secret = parser.get('Auth', 'consumer_secret')
      self.access_key = parser.get('Auth', 'access_key')
      self.access_secret = parser.get('Auth', 'access_secret')
    except:
      ## TODO: log plugin parser error
      pass


  def execute(self, ircMsg, userRole):
    m = IRCMessage()
    try:
      msg = ircMsg.msg
      option = msg.rsplit('identica')[1].strip().split(' ')[0]

      if option == 'post':
        m = self.post(ircMsg)
      elif option == 'pull':
        m = self.pull(ircMsg)
    except:
      m.msg =  _("msgIdentiFail")

    m.channel = ircMsg.channel
    m.user = ircMsg.user

    return m

  def auth(self):
    self.username = ""
    self.password = ""
    self.auth = tweepy.auth.BasicAuthHandler(self.username, self.password)
    self.api = tweepy.API(self.auth, self.host, self.api_root, secure = True)
    self.api.verify_credentials()
    if not self.api.verify_credentials():
      import traceback
      traceback.print_exc()
      print _("msgIdentiFail")
    else:
      print _("msgIdentiOk")

  def oauth(self):
    self.auth = tweepy.OAuthHandler(self.consumer_token, self.consumer_secret, 'oob')
    self.auth.OAUTH_HOST = self.host
    self.auth.OAUTH_ROOT = self.oauth_root
    self.auth.secure = True
    self.auth.set_access_token(self.access_key, self.access_secret)

  def post(self, ircMsg):
    user = ircMsg.user
    message = ' '.join(ircMsg.msg.split())

    post = re.sub('^!identica post ', '', message)
    m = IRCMessage()

    m.msg = _("msgIdentiPost").format(user, post)

    try:
      self.oauth()
      self.api = tweepy.API(self.auth, host = self.host, api_root = self.api_root)
      #self.api.update_status(post[:140])
    except:
      m.msg("msgIdentiFail")
      return m

  def pull(self, ircMsg):
    user = ircMsg.user
    message = ' '.join(ircMsg.msg.split())

    userid = re.sub('^!identica pull ', '', message)
    m = IRCMessage()

    #m.msg = _("msgIdentiPost").format(user, post)

    try:
      self.oauth()
      self.api = tweepy.API(self.auth, host = self.host, api_root = self.api_root)
      timeline = self.api.user_timeline(userid)
      #TODO: add support to pull an specific index
      m.msg = str(timeline[0].text)
    except:
      import traceback
      traceback.print_exc()
      m.msg("msgIdentiFail")

    return m

  def activate(self):
    super(identica, self).activate()
    print _("msgIdentiEn")


  def deactivate(self):
    super(identica, self).deactivate()
    print_("msgIdentiDis")


