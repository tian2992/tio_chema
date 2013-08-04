import requests
import types
import re
import json
import random
from plugins.baseactionplugin import BaseActionPlugin
from ircmessage import IRCMessage
from plugins.lengua import _

class CuatroChan(BaseActionPlugin):
  def __init__(self):
    BaseActionPlugin.__init__(self)
    self.synchronous = False

  def get_boards( self, abuscar ):
      url = 'http://api.4chan.org/boards.json'
      f = requests.get( url )
      data = json.loads(f.text)

      for board in data['boards']:
        if board['board'] == abuscar :
          return True

      return False

  def get_threads( self, board ):
      url = 'http://api.4chan.org/' + board + '/threads.json'
      f = requests.get( url )
      data = json.loads(f.text)

      page = random.choice( data )
      threads = random.choice( page['threads'] )
      id_thread = threads['no']
      
      url_resp = 'http://4chan.org/' + board + '/' + str(id_thread)

      return url_resp

  def execute(self, ircMsg, userRole, *args, **kwargs):
      user = ircMsg.user
      m = IRCMessage()
      definiciones = []
      message = ' '.join(ircMsg.msg.split())
      board = re.sub('^!4chan ', '', message)
      
      existe = self.get_boards( board )
      respuesta = ''
      if existe :
        respuesta = self.get_threads( board )
        respuesta = 'Te recomiendo este thread ' + respuesta
      else :
        respuesta = 'Ese board mierda no existe'

      m.msg = respuesta
      m.channel = ircMsg.channel
      m.user = user
      m.directed = True
      return m

