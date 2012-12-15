from yapsy.IPlugin import IPlugin
from ircmessage import IRCMessage

class PluginPing(IPlugin):

  # This constructor is optional
  def __init__(self):
    self.threshold = 3
    self.counter = 0
    self.last_user = ""

  def execute(self, ircMsg, userRole):
    user = ircMsg.user
    if user == self.last_user:
      self.counter += 1
    else:
      self.counter = 0
      self.last_user = user

    m = IRCMessage()
    if self.counter > self.threshold:
      #TODO: localize
      m.msg = "yarr, it's the {0} time you've called me!".format(self.counter)
    else:
      m.msg = "pong"
    m.channel = ircMsg.channel
    m.user = user
    m.directed = True
    return m