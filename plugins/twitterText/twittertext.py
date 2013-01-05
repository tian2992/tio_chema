from plugins.texttriggerplugin import TextTriggerPlugin
from ircmessage import IRCMessage

import tweepy
import re


class TwitterTextPlugin(TextTriggerPlugin):

  def __init__(self):
    self.trigger = re.compile(
      """((http|https)://twitter.com/([A-Za-z0-9_]{1,15})/status/([\d]*))""",
      re.IGNORECASE)

  def execute(self, ircMsg, userRole, regex_group):
    m = IRCMessage()
    m.channel = ircMsg.channel

    status = tweepy.api.get_status(regex_group[-1])
    m.msg = u"@{0}: {1}".format(regex_group[-2], status.text)

    m.user = ircMsg.user
    return m
