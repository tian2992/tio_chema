import requests
import types
import re
import json
import random
import logging
from plugins.baseactionplugin import BaseActionPlugin
from ircmessage import IRCMessage
from plugins.lengua import _

class CuatroChan(BaseActionPlugin):
  def __init__(self):
    BaseActionPlugin.__init__(self)
    self.synchronous = False
    self.url = 'http://api.4chan.org/'
    self.function_dict = {
                          "default": self.get_random,
                          "threads": self.get_threads,
                         }

  def get_boards( self, abuscar ):
      url = self.url + 'boards.json'
      f = requests.get( url )
      data = json.loads(f.text)

      for board in data[ 'boards' ]:
        if board[ 'board' ] == abuscar :
          return True

      return False

  def get_thread( self, board ):
      try:
        existe = self.get_boards( board )
        print existe
        if not existe :
          respuesta = 'Ese board mierda no existe'
          return respuesta

        url = self.url + board + '/threads.json'    
        f = requests.get( url )
        data = json.loads( f.text )
        page = random.choice( data )
        threads = random.choice( page[ 'threads' ] )
        id_thread = threads[ 'no' ]
        respuesta = 'Te recomiendo este thread http://4chan.org/{0}/{1}'.format( board, id_thread )
      except:
        respuesta = 'Fallo el api 4chanesco'
      return respuesta


  def get_threads( self, ircMsg ):
      message = ' '.join( ircMsg.msg.split() )      
      try:
        board = ircMsg.msg.split(' ')[ 1 ]
        ircMsg.msg = self.get_thread( board )
      except:
        ircMsg.msg = 'Fallo el api 4chanesco' 
      return ircMsg


  def get_random( self, ircMsg ):
      random = 'b'
      try:
        ircMsg.msg = self.get_thread( random )
      except:
        logging.exception( 'Fallo en obtener json' )
        ircMsg.msg =  'Fallo el api 4chanesco' 
      
      return ircMsg


  def execute(self, ircMsg, userRole, *args, **kwargs):
      user = ircMsg.user
      m = IRCMessage()      
      message = ' '.join( ircMsg.msg.split() )
      
      options = ircMsg.msg.split(' ')
      try:
        if( len( options ) > 1 ):
          func = self.function_dict[ 'threads' ]
          return func( ircMsg )
        else: 
          func = self.function_dict[ 'default' ]
          return func( ircMsg )
      except:
        logging.exception("Exception in 4chan command.")
        ircMsg.msg = "Fracaso en el plugin 4chan"
        return ircMsg
    
