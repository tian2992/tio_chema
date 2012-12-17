from yapsy.IPlugin import IPlugin
from ircmessage import IRCMessage
import gettext

class plugin_identica(IPlugin):

  # This constructor is optional
  def __init__(self):
    self.threshold = 3
    self.counter = 0
    self.last_user = ""
    self.loc_dir = "../locale/"
    self.trans = gettext.translation("IDENTICA", self.loc_dir)
    _ = trans.ugettext

    trans.install()


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
