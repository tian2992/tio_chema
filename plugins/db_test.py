from plugins.baseactionplugin import BaseActionPlugin
from ircmessage import IRCMessage
import sqlite3
import logging

class DB_Test(BaseActionPlugin):

  # DB based plugins should have self.synchronous set as False.
  def __init__(self):
    BaseActionPlugin.__init__(self)
    self.synchronous = False

  def execute(self, ircMsg, userRole, *args, **kwargs):
    user = ircMsg.user
    m = IRCMessage()
    conn = kwargs["connection"]
    conn.execute("select * from users").fetchall()
    m.msg = "dbtested"
    m.channel = ircMsg.channel
    m.user = user
    m.directed = True
    logging.debug("User: {0} pinged".format(user))
    return m
