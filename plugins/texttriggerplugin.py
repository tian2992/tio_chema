from yapsy.IPlugin import IPlugin
from ircplugin import IRCPlugin

class TextTriggerPlugin(IRCPlugin):

  def __init__(self):
    IRCPlugin.__init__(self)
    self.trigger = None

  def execute(self, ircMsg, userRole, regex_group, *args, **kwargs):
    raise NotImplementedError
