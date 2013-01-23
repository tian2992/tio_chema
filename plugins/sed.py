from plugins.texttriggerplugin import TextTriggerPlugin
from ircmessage import IRCMessage

import re


class SedPlugin(TextTriggerPlugin):

  def __init__(self):
    self.trigger = None

  def execute(self, ircMsg, userRole, regex_groups):
    regex_group = regex_groups[0]

    return ircMsg