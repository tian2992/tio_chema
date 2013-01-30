import unittest
from twittertext import TwitterTextPlugin
from ircmessage import IRCMessage

#from plugins.twitterText import TwitterTextPlugin

class TwitterTextTest(unittest.TestCase):
  def setUp(self):
    self.p = TwitterTextPlugin()
    self.n = IRCMessage("#test-channel", "http://identi.ca/notice/98533495", "josema", True)


  def testTrigger(self):
    regex = self.p.trigger
    message_list = [
      ("https://twitter.com/EFF/status/284750284557783040",
        [("https://twitter.com/EFF/status/284750284557783040", "https", "twitter.com", "EFF/status", "EFF", "284750284557783040")]),
      ("http://identi.ca/notice/98533495",
        [("http://identi.ca/notice/98533495", "http", "identi.ca", "notice", '', "98533495")]),
      ("http://xkcd.com",
        []),
    ]
    for message in message_list:
      result_groups = regex.findall(message[0])
      self.assertEquals(message[1], result_groups)

  def testExecute(self):
    ## TODO: Fix Test
    #api = DummyAPI()
    #m = self.p.fetchAndFormatStatus(self.n, api, self.p.trigger.findall(self.n.msg))


class DummyAPI:
  def __init__(self, *args, **kwargs):
    pass

  def get_status(self, user_id):
    return

if __name__ == "__main__":
  unittest.main()