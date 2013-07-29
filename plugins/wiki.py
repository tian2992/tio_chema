import requests
import types
import re
import json
from random import randint
from plugins.baseactionplugin import BaseActionPlugin
from ircmessage import IRCMessage
from plugins.lengua import _
from bs4 import BeautifulSoup


class Wiki(BaseActionPlugin):
  def __init_(self):
    BaseActionPlugin.__init__(self)
    self.synchronous = False

  def execute(self, ircMsg, userRole, *args, **kwargs):
      user = ircMsg.user
      m = IRCMessage()
      definiciones = []
      message = ' '.join(ircMsg.msg.split())
      term = re.sub('^!wiki ', '', message)
      term = re.sub( ' ', '_', term )

      url = "http://es.wikipedia.org/wiki/" + term    

      f = requests.get( url )
      data = f.text

      soup = BeautifulSoup( data )
      tag = soup.find_all('div', attrs={'class' : 'mw-content-ltr' } )
      p = tag[0].p.text.encode('utf8')
      
#      dic = json.loads(data)
      m.msg = p
      m.channel = ircMsg.channel
      m.user = user
      m.directed = True
      return m

