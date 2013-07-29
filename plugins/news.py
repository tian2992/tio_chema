import requests
import types
import re
from random import randint
from plugins.baseactionplugin import BaseActionPlugin
from ircmessage import IRCMessage
from plugins.lengua import _
from bs4 import BeautifulSoup

class News(BaseActionPlugin):
  def __init_(self):
    BaseActionPlugin.__init__(self)
    self.synchronous = False

  def execute(self, ircMsg, userRole, *args, **kwargs):
      user = ircMsg.user
      m = IRCMessage()
      url = 'http://hosted2.ap.org/atom/APDEFAULT/3d281c11a96b4ad082fe88aa0db04305'

      f = requests.get( url )
      data = f.text
      soup = BeautifulSoup( data )
      tag = soup.find_all( 'entry' )
      tagita = tag[ randint( 0, len( tag ) -1 ) ]
      respuesta = tagita.title.string.encode( 'utf8')  + ' | ' + tagita.link[ 'href' ].encode( 'utf8' )
      
      m.msg = respuesta
      m.channel = ircMsg.channel
      m.user = user
      m.directed = True
      return m

  
