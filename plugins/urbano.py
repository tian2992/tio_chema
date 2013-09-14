import requests
import types
import re
from random import randint
from plugins.baseactionplugin import BaseActionPlugin
from ircmessage import IRCMessage
from plugins.lengua import _
from bs4 import BeautifulSoup

class Urbano(BaseActionPlugin):
  def __init__(self):
    BaseActionPlugin.__init__(self)
    self.synchronous = False

  def execute(self, ircMsg, userRole, *args, **kwargs):
      user = ircMsg.user
      m = IRCMessage()
      definiciones = []
      message = ' '.join(ircMsg.msg.split())
      term = re.sub('^!urbano ', '', message)

      payload = {'term': term  }
      url = "http://www.urbandictionary.com/define.php?"    

      f = requests.get( url, params=payload)
      data = f.text

      soup = BeautifulSoup( data )
      tag = soup.find_all('div', attrs={'class' : 'definition' } )

      for tagita in tag:
        if type(tagita.string) != types.NoneType :
          definiciones.append( tagita.string.strip() )

      respuesta = definiciones[ randint( 0, len( definiciones ) - 1 ) ]

      m.msg = respuesta
      m.channel = ircMsg.channel
      m.user = user
      m.directed = True
      return m
