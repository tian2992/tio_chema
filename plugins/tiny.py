import requests
import types
import re
from random import randint
from plugins.baseactionplugin import BaseActionPlugin
from ircmessage import IRCMessage
from plugins.lengua import _
from bs4 import BeautifulSoup

class Tiny(BaseActionPlugin):
  def __init_(self):
    BaseActionPlugin.__init__(self)
    self.synchronous = False

  def execute(self, ircMsg, userRole, *args, **kwargs):
      user = ircMsg.user
      m = IRCMessage()
      definiciones = []
      message = ' '.join(ircMsg.msg.split())
      path = re.sub('^!tiny ', '', message)
      if not path.startswith('http'):
          path = '%s%s' % ('http://', path)

      payload = {'url': path }
      url = "http://tinyurl.com/api-create.php?"

      f = requests.get( url, params=payload)
      data = f.text
      
      if data == '' :
          respuesta = 'No se pudo transformar la url marica'
      else:
          respuesta = data
  
      m.msg = respuesta
      m.channel = ircMsg.channel
      m.user = user
      m.directed = True
      return m
      

