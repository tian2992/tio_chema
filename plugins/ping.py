from yapsy.IPlugin import IPlugin
# from ..ircmessage import IRCMessage

class PluginPing(IPlugin):

  # This constructor is optional
  def __init__(self):
    self.counter = 0
    self.last_user = ""

  def execute(self, ircMsg, userRole):
    user = ircMsg.user
    self.last_user = user
    msg = "%s: pong" % user
    ircMsg.message = msg
    ircMsg.directed = True
    return ircMsg