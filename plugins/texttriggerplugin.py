from yapsy.IPlugin import IPlugin
from ircplugin import IRCPlugin

'''Abstract plugin that has a trigger.'''
class TextTriggerPlugin(IRCPlugin):

  def __init__(self):
    IRCPlugin.__init__(self)
    self.trigger = None
    self.synchronous = False ## Except for debugging, plugins should not be sync.

  def execute(self, ircMsg, userRole, regex_group, *args, **kwargs):
    raise NotImplementedError
