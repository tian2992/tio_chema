from yapsy.IPlugin import IPlugin
from ircplugin import IRCPlugin

class TextTriggerPlugin(IRCPlugin):

  def trigger():
      doc = "The trigger property, should be a regex."
      def fget(self):
          return self.trigger
      def fset(self, value):
          self.trigger = value
      def fdel(self):
          del self.trigger
      return locals()
  trigger = property(**trigger())

  def execute(self, ircMsg, userRole, regex_group):
    raise NotImplementedError