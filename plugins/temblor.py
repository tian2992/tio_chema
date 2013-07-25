import requests
import types
import re
import json
from random import randint
from plugins.baseactionplugin import BaseActionPlugin
from ircmessage import IRCMessage
from plugins.lengua import _
from bs4 import BeautifulSoup

class Temblor(BaseActionPlugin):
  def __init_(self):
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

      print type( data['features'] )
      print len( data['features'] )
      for feature in data['features']:
        cadena = feature['properties']['place']
        
        if cadena.find( 'California' ) != -1 :
          print cadena

      m.msg = ''
      m.channel = ircMsg.channel
      m.user = user
      m.directed = True
      return m
