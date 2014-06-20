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
    self.url = 'https://a.4cdn.org/'
    self.function_dict = {
                          "default": self.handle_get_random_thread,
                          "random_thread": self.handle_get_random_thread,
                         }
    self.boards = self.__fetch_boards_dict()


  def __fetch_boards_dict(self):

    def extract(item):
      return {item["board"]: {"title": item["title"], "worksafe":item["ws_board"]}}

    def add_dict(dictionary, new_dictionary):
      dictionary.update(new_dictionary)
      return dictionary

    logging.debug("Getting boards")
    url = self.url + 'boards.json'
    f = requests.get( url )
    data = f.json()

    boards_list = map(extract, data["boards"])
    boards = reduce(add_dict, boards_list, {})

    return boards

  def __get_random_thread( self, board ):
      try:
        existe = self.boards.get(board)
        if not existe :
          respuesta = 'Ese board mierda no existe'
          return respuesta

        threads_url = (self.url+"{0}/threads.json").format(board)
        f = requests.get( threads_url )
        data = json.loads( f.text )
        page = random.choice( data )
        threads = random.choice( page[ 'threads' ] )
        id_thread = threads[ 'no' ]
        respuesta = '4chan thread http://4chan.org/thread/{0}/{1}'.format( board, id_thread )
      except:
        logging.exception("Get thread fail.")
        respuesta = 'Fallo el api 4chanesco'
      return respuesta


  def get_random_thread_string(self, board="b"):
    logging.debug("Getting random thread from {0}".format(board))
    try:
      return self.__get_random_thread(board)
    except:
      logging.exception("4chan: get threads API fail.")
      return 'Fallo el api 4chanesco'


  def handle_get_random_thread(self, ircMsg):
    ## Nasty hack as there is only one action.
    args = "".join(ircMsg.arguments)
    board = args if args else "b"
    try:
      return self.get_random_thread_string(board)
    except:
      logging.exception("something happened")


  def execute(self, ircMsg, userRole, *args, **kwargs):
      user = ircMsg.user
      m = IRCMessage()
      options = ircMsg.msg.split(' ')[1::]
      logging.debug("called {0}".format(options))
      try:
        if options:
          command = options[0]
        else:
          command = "default"
        func = self.function_dict.get(command, self.function_dict['random_thread'])
        message = func(ircMsg)
        ircMsg.msg = message
        return ircMsg
      except:
        logging.exception("Exception in 4chan command.")
        ircMsg.msg = "Fracaso en el plugin 4chan"
        return ircMsg

