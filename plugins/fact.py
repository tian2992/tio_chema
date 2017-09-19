from plugins.baseactionplugin import BaseActionPlugin
from ircmessage import IRCMessage
import logging
import data_manager

class PluginFact(BaseActionPlugin):

  def __init__(self):
    BaseActionPlugin.__init__(self)
    self.db = data_manager.Factoider()

  def execute(self, ircMsg, userRole, *args, **kwargs):
    user = ircMsg.user

    toko = ircMsg.tokens[0]
    factz = self.db.get_factz(unicode(toko))

    m = IRCMessage()
    m.msg = "{}".format(factz)
    m.channel = ircMsg.channel
    m.user = user
    m.directed = True
    logging.debug("Queried factz :{0}".format(factz))
    return m
