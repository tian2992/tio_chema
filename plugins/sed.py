from plugins.texttriggerplugin import TextTriggerPlugin
from ircmessage import IRCMessage
from collections import deque

import logging
import re

class LoggingRegexTrigger():
  """A class that can trigger based on a regex but stores the last message that passed through it.

  Stores the last message of each user that has talked in the channel.
  """

  def __init__(self, regex):
    self.lines = {}
    self.regex = regex
    self.message_limit = 20

  def fire(self, ircm, *args, **kwargs):
    user = ircm.user
    message = ircm.msg
    try:
      self.lines[user].appendleft(message)
    except KeyError:
      self.lines[user] = deque([], self.message_limit)
      self.lines[user].appendleft(message)

    groups = self.regex.findall(message)
    if groups:
      return (groups, self.lines)
    else:
      return groups

class SedPlugin(TextTriggerPlugin):

  def __init__(self):
    self.trigger = LoggingRegexTrigger(re.compile("^s([\d]*)/([^/]+)/([^/]+)/$"))

  def execute(self, ircMsg, userRole, result):
    m = IRCMessage()
    m.channel = ircMsg.channel
    m.user = ircMsg.user

    groups, lines = result
    group = groups[0]

    logging.debug("RegexTriggerLogged {0}, {1}".format(groups, lines))

    try:
      try:
        index = int(group[0])
      except:
        index = 1
      m.msg = re.sub(group[1], group[2], lines[ircMsg.user][index])
      m.directed = True
    except (IndexError, KeyError):
      #TODO: proper error message
      return ircMsg

    return m
