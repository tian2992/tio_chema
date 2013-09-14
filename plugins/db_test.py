from plugins.baseactionplugin import BaseActionPlugin
from ircmessage import IRCMessage
import sqlite3
import logging
import random

class DB_Test(BaseActionPlugin):

  # DB based plugins should have self.synchronous set as False.
  def __init__(self):
    BaseActionPlugin.__init__(self)
    self.synchronous = False

  def execute(self, ircMsg, userRole, *args, **kwargs):
    user = ircMsg.user
    m = IRCMessage()
    conn = kwargs["connection"]
    m.msg = unicode()
    all_rows = conn.execute("select * from users").fetchall()
    choice = random.choice(all_rows)
    m.msg = "The selected user is {0}".format(choice[0])

    m.channel = ircMsg.channel
    m.user = user
    m.directed = True
    logging.debug("User: {0} hit the DB".format(user))
    return m
