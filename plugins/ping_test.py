import unittest

from ping import PluginPing
from ircmessage import IRCMessage

class PingCheck(unittest.TestCase):
  def setUp(self):
    self.p = PluginPing()

  def testSimplePing(self):
    channel = "#test-channel"
    user = "pedro"
    m = IRCMessage(channel, "---", user, True)
    response = self.p.execute(m, None)
    pong = IRCMessage(channel, "pong", user, True)
    self.assertEquals(response, pong)

  def testRepeatedPing(self):
    channel = "#test-channel"
    user1 = "pedro"
    m1 = IRCMessage(channel, "---", user1, True)
    for i in range(self.p.threshold+1):
      self.p.execute(m1, None)
    self.assertEquals(self.p.counter, self.p.threshold)
    user2 = "pepe"
    m2 = IRCMessage(channel, "---", user2, True)
    self.p.execute(m2, None)
    self.assertEquals(self.p.counter, 0)
    self.p.execute(m1, None)
    self.assertEquals(self.p.counter, 0)
    for i in range(self.p.threshold+1):
      self.p.execute(m2, None)
    self.assertEquals(self.p.counter, self.p.threshold)

if __name__ == "__main__":
    unittest.main()