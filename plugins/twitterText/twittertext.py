from plugins.texttriggerplugin import TextTriggerPlugin
from ircmessage import IRCMessage

import tweepy
import re


class TwitterTextPlugin(TextTriggerPlugin):

  def __init__(self):
    self.trigger = re.compile(
      """((http|https)://(twitter.com|identi.ca)/(([A-Za-z0-9_]{1,15})/status|notice)/([\d]*))""",
      re.IGNORECASE)

  def execute(self, ircMsg, userRole, regex_group):
    m = IRCMessage()
    m.channel = ircMsg.channel

    if regex_group[2] == "twitter.com":
      api = tweepy.API()
    elif regex_group[2] == "identi.ca":
      api = tweepy.API(host = 'identi.ca', api_root = '/api/')
    else:
      raise Exception("No API defined for this handler.")

    status = api.get_status(regex_group[-1])
    if regex_group[-2]:
      author = regex_group[-2]
    else:
      author = status.author.screen_name

    m.msg = u"@{0}: {1}".format(author, status.text)
    m.user = ircMsg.user
    return m
