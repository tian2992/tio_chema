import requests
import types
import re
import json
from datetime import datetime
from random import randint
from plugins.baseactionplugin import BaseActionPlugin
from ircmessage import IRCMessage
from plugins.lengua import _
from bs4 import BeautifulSoup

class Temblor(BaseActionPlugin):
  def __init__(self):
    BaseActionPlugin.__init__(self)
    self.synchronous = False

  def execute(self, ircMsg, userRole, *args, **kwargs):
      user = ircMsg.user
      m = IRCMessage()
      definiciones = []
      message = ' '.join(ircMsg.msg.split())
      term = re.sub('^!temblor ', '', message)
      url = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
      f = requests.get( url )
      data = json.loads(f.text)

      for feature in data['features']:
        cadena = feature['properties']['place']
        
        if cadena.upper().find( term.upper() ) != -1 :
          definiciones.append( feature )

      size = len( definiciones )
      temblo = definiciones[ randint( 0, size ) ]
      fecha_t = datetime.fromtimestamp( temblo[ 'properties' ][ 'time' ] / 1000 )
      fecha = fecha_t.strftime( '%d/%M/%Y %H:%m:%s')
      
      respuesta = '' + str( temblo[ 'properties' ][ 'mag' ] ) + ' | ' + temblo[ 'properties' ][ 'place' ] +  ' | ' + fecha + ' | '+ temblo[ 'properties' ][ 'url' ] 
      m.msg = respuesta
      m.channel = ircMsg.channel
      m.user = user
      m.directed = True
      return m
