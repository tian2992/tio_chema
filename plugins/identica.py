from yapsy.IPlugin import IPlugin
from ircmessage import IRCMessage
from plugins.lengua import _

class identica(IPlugin):

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

    m.msg = _("msgSalida").format(self.counter)

    m.channel = ircMsg.channel
    m.user = user
    m.directed = True
    return m
