import unittest

from ircmessage import IRCMessage

class IRCMessageTest(unittest.TestCase):
  def setUp(self):
    self.channel = "#test-channel"
    self.user = "pedro"
    self.m = IRCMessage(self.channel, "---", self.user, True)

  def testIsInitialized(self):
    self.assertTrue(self.m.is_initialized())
    q = IRCMessage()
    self.assertFalse(q.is_initialized())
    ## Message with no channel should be false.
    q.channel = "#"
    q.msg = "notempty"
    self.assertFalse(q.is_initialized())
    ## Adding directed testing.
    q.channel = self.channel
    q.directed = True
    self.assertFalse(q.is_initialized())
    q.user = self.user
    self.assertTrue(q.is_initialized())


  def testEquality(self):
    n = IRCMessage(self.channel, "---", self.user, True)
    self.assertEquals(self.m, n)
    n.msg = "!-"
    self.assertNotEquals(self.m, n)
    n.msg = self.m.msg
    n.channel = "#"
    self.assertNotEquals(self.m, n)

    ## A fake directed should not be equal.
    n = IRCMessage(self.channel, "---", self.user, False)
    self.m.directed = True
    self.assertNotEquals(self.m, n)

    n.msg = "{0}: {1}".format(n.user, n.msg)
    self.assertNotEquals(self.m, n)

  def testRender(self):
    expected = "{0}: {1}".format(self.m.user, self.m.msg)
    self.assertEquals(self.m.render(), expected)
    expected = self.m.msg
    self.m.directed = False
    self.assertEquals(self.m.render(), expected)

if __name__ == "__main__":
    unittest.main()