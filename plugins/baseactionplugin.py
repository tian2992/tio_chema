from yapsy.IPlugin import IPlugin
from ircplugin import IRCPlugin

class BaseActionPlugin(IRCPlugin):

  def __init__(self):
    IRCPlugin.__init__(self)

  def execute(self, ircMsg, userRole, *args, **kwargs):
    """
    An abstract method that should be overriden by the subclasses.
    """
    raise NotImplementedError

