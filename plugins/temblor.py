import requests
import types
import re
import json
import logging
import random
from datetime import datetime
from plugins.baseactionplugin import BaseActionPlugin
from ircmessage import IRCMessage
from plugins.lengua import _
from bs4 import BeautifulSoup

class Temblor(BaseActionPlugin):
  def __init__(self):
    BaseActionPlugin.__init__(self)
    self.synchronous = False
    self.base_url = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"

  def execute(self, ircMsg, userRole, *args, **kwargs):
      user = ircMsg.user
      m = IRCMessage()
      definiciones = []
      term = ircMsg.arguments
      f = requests.get(self.base_url)
      data = f.json()

      ## If there was a selected place.
      if term:
        logging.debug("Getting earthquakes for: '{0}'.".format(' '.join(term)))
        for feature in data['features']:
          cadena = feature['properties']['place']
          if cadena.lower().find(' '.join(term).lower()) != -1 :
            definiciones.append(feature)
        ## In case there has not been any quake there recently.
        if not definiciones:
          ircMsg.msg = "There has not been any quake there in a while."
          return ircMsg
        temblo = random.choice(definiciones)
      ## Let's just pick the most recent quake.
      else:
        temblo = data['features'][0]


      ## Converting UNIX timestamp to human readable time.
      date_t = datetime.fromtimestamp(temblo['properties']['time'] / 1000)
      date = date_t.isoformat()

      response_string = "Quake in: {0} | Magnitude: {1} | Time: {2} | URI: {3}".format(
          temblo[ 'properties' ][ 'place' ],
          temblo[ 'properties' ][ 'mag' ],
          date,
          temblo[ 'properties' ][ 'url' ]
        )
      m.msg = response_string
      m.channel = ircMsg.channel
      m.user = user
      m.directed = True
      return m
