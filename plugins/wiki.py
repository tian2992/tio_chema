import requests
import types
import re
import json
from random import randint
from plugins.baseactionplugin import BaseActionPlugin
from ircmessage import IRCMessage
from plugins.lengua import _
from bs4 import BeautifulSoup
import logging


class Wiki(BaseActionPlugin):
  def __init_(self):
    BaseActionPlugin.__init__(self)
    self.synchronous = False

  def execute(self, ircMsg, userRole, *args, **kwargs):
      user = ircMsg.user
      m = IRCMessage()
      definiciones = []
      split_msg = ircMsg.arguments
      try:
        #TODO: fix more languages for wiki plugin
        if split_msg[0] in ['es', 'en', 'de', 'fr']:
          url = "http://"+ split_msg[0] +".wikipedia.org/wiki/"
          split_msg = split_msg[1::]
        else:
          #TODO: wiki base url should depend on language
          url = "http://es.wikipedia.org/wiki/"
      except:
        url = "http://es.wikipedia.org/wiki/"

      term = re.sub( ' ', '_', ' '.join(split_msg))
      url += term

      logging.debug("Fetching wiki page: '{0}'.".format(url))

      f = requests.get(url)
      data = f.text
      try:
        soup = BeautifulSoup( data )
        tag = soup.find_all('div', attrs={'class' : 'mw-content-ltr' } )
        p = tag[0].p.text[:250]
      except:
        ircMsg.msg = "Wiki: An error ocurred."
        return ircMsg

      m.msg = p
      m.channel = ircMsg.channel
      m.user = user
      m.directed = True
      return m

