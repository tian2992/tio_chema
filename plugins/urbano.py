import requests
from plugins.baseactionplugin import BaseActionPlugin
from ircmessage import IRCMessage
import HTMLParser
from plugins.lengua import _

class Urbano(BaseActionPlugin):
  def __init_(self):
    BaseActionPlugin.__init__(self)
    self.synchronous = False
  def execute(self, ircMsg, userRole, *args, **kwargs):
      user = ircMsg.user
      m = IRCMessage()

      term = m.msg
      print 'el valor de term es' + term

      payload = {'term': 'stfu'  }
      url = "http://www.urbandictionary.com/define.php?"

      f = requests.get( url, params=payload)
      data = f.text

      link =  LinksParser()
      link.feed(data)
      m.msg = link.data[0]
      m.channel = ircMsg.channel
      m.user = user
      m.directed = True
      return m



class LinksParser(HTMLParser.HTMLParser):
  def __init__(self):
    HTMLParser.HTMLParser.__init__(self)
    self.recording = 0
    self.data = []

  def handle_starttag(self, tag, attributes):
    if tag != 'div':
      return
    if self.recording:
      self.recording += 1
      return
    for name, value in attributes:
      if name == 'id' and value == 'definition':
        break
    else:
      return
    self.recording = 1

  def handle_endtag(self, tag):
    if tag == 'div' and self.recording:
      self.recording -= 1

  def handle_data(self, data):
    if self.recording:
      self.data.append(data)
