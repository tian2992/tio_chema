from plugins.texttriggerplugin import TextTriggerPlugin
from ircmessage import IRCMessage

import tweepy
import re


class TwitterTextPlugin(TextTriggerPlugin):

  def __init__(self):
    self.trigger = re.compile(
      """((http|https)://(twitter.com|identi.ca)/(([A-Za-z0-9_]{1,15})/status|notice)/([\d]*))""",
      re.IGNORECASE)

  def execute(self, ircMsg, userRole, regex_groups):
    regex_group = regex_groups[0]

    api = self.createApi(regex_group[2])
    return self.fetchAndFormatStatus(ircMsg, api, regex_group)

  def createApi(self, host):
    if host == "twitter.com":
      api = tweepy.API()
    elif host == "identi.ca":
      api = tweepy.API(host = 'identi.ca', api_root = '/api/')
    else:
      raise Exception("No API defined for this handler.")
    return api

  def fetchAndFormatStatus(self, ircMsg, api, regex_group):
    m = IRCMessage()
    m.channel = ircMsg.channel

    status = api.get_status(regex_group[-1])
    if regex_group[-2]:
      author = regex_group[-2]
    else:
      author = status.author.screen_name

    m.msg = u"@{0}: {1}".format(author, status.text)
    m.user = ircMsg.user
    return m
