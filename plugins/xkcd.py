import requests
import types
import re
import json
import random
import os, sys
from plugins.baseactionplugin import BaseActionPlugin
from ircmessage import IRCMessage
from plugins.lengua import _

class XKCD(BaseActionPlugin):
  def __init__(self):
    BaseActionPlugin.__init__(self)
    self.synchronous = False

  def get_current( self ):
    url = 'http://xkcd.com/info.0.json'
    f = requests.get( url )
    data = json.loads( f.text )
    imagen = data['img']
    titulo = data['title']
    alt = data['alt']
    respuesta = u'La tira actual es {0} - {1} - {2}'.format( titulo, imagen, alt )
    return respuesta

  def get_comic( self, comic ):
    url2 = u'http://xkcd.com/'+ comic + '/info.0.json'
    f = requests.get( url2 )
    try:
      data = json.loads( f.text )
      imagen = data['img']
      titulo = data['title']
      alt = data['alt']
      respuesta = u'La tira {0} es {1} - {2} - {3}'.format( comic, titulo, imagen, alt )
    except:
      respuesta = u'Esa tira cerota no existe'
    return respuesta


  def execute(self, ircMsg, userRole, *args, **kwargs):
      user = ircMsg.user
      m = IRCMessage()
      message = ' '.join(ircMsg.msg.split())
      numero = re.sub('^!xkcd ', '', message)

      if numero.isdigit():
        respuesta = self.get_comic( numero )
      else:
        respuesta = self.get_current()

      m.msg = respuesta
      m.channel = ircMsg.channel
      m.user = user
      m.directed = True
      return m

