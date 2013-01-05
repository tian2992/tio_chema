from yapsy.IPlugin import IPlugin
from ircplugin import IRCPlugin

class TextTriggerPlugin(IRCPlugin):

  def execute(self, ircMsg, userRole, regex_group):
    raise NotImplementedError