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

  def get_quake(self, place = ""):
    data = self.__fetch_data(self.base_url)
    quakes = []
    ## If there was a selected place.
    if place:
        logging.debug("Getting earthquakes for: '{0}'.".format(place))
        for feature in data['features']:
          cadena = feature['properties']['place']
          if cadena.lower().find(place.lower()) != -1 :
            quakes.append(feature)
        ## In case there has not been any quake there recently.
        if not quakes:
          raise Exception("There has not been any quake there in a while.")
        quake = random.choice(quakes)
    ## Otherwise let's just pick the most recent quake.
    else:
      quake = data['features'][0]
    return quake

  def __fetch_data(self, base_url):
     f = requests.get(base_url)
     return f.json()

  def execute(self, ircMsg, userRole, *args, **kwargs):
      user = ircMsg.user
      m = IRCMessage()
      term = ' '.join(ircMsg.arguments)

      try:
        temblo = self.get_quake(term)
      except Exception as e:
        ircMsg.msg = e.args[0]
        return ircMsg

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
