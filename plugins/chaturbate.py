
import json
import urllib
import logging

from plugins.baseactionplugin import BaseActionPlugin
from ircmessage import IRCMessage


class Chaturbate(BaseActionPlugin):

    url = 'http://chaturbate.com/affiliates/api/onlinerooms/?format=json&wm=mnzQo'

    def __init__(self):
        BaseActionPlugin.__init__(self)
        self.last_user = ""
        self.synchronous = False

        self.function_dict={
            'genre': self.get_online_by_gender,
            'nick': self.get_url_by_nick,
            'help': self.help,
            }


    def _get_online_users_list(self):
        jsonurl = urllib.urlopen(self.url)
        try:
            if jsonurl:
                return json.loads(jsonurl.read())
            else:
                return None
        except :
            logging.error('An error ocurred while retrieving users list ')
            return None

    def help(self, command):

        if command == 'nick':
            return "!chaturbate nick <nick_de_la_puta> te muestro informacion importante de la puta que quieres ver"

        elif command == 'genre':
            return '!chaturbate genre <opcion>. Opciones: f=perras, m=garrotes, s=trannys(!lfac), c=parejas'
        else:
            return "!chaturbate <opcion> <parametro> | Mas info: !chaturbate help (genre|nick)"

    def get_online_by_gender(self, gender):
        """gender: Can be f, m, s, or c for female, male, shemale,
        and couple
        """
        _online_users=''
        users_list = self._get_online_users_list()
        count = 0
        if users_list is not None:
            for user in users_list:
                if user.get('gender') == gender:
                    _online_users = _online_users + user.get('username') +' '
                    count +=1
                    if count >15:
                        return _online_users
            return  _online_user
        else:
            return u'oops! no hay putas en este momento'


    def get_url_by_nick(self, username):
        users_list = self._get_online_users_list()
        if users_list is not None:
            
            for user in users_list:
                if user.get('username') == username:
                    slut_metadata = u'Nombre: {name} - Edad: {age} - URL: {slut_url}'
                    return slut_metadata.format(name=user.get('display_name'),
                                                age = str(user.get('age')),
                                                slut_url = user.get('chat_room_url')
                                                )
            return u'Por califas quien buscabas se ha cansado de chaturbar'
        else:
            return u'No hay putas :('


    def execute(self, ircMsg, userRole, *args, **kwargs):
        
        command = ircMsg.msg.split(' ')
        command_type = command[1]
        
        irc_msg = IRCMessage()
        irc_msg.channel = ircMsg.channel
        irc_msg.user = ircMsg.user
        irc_msg.directed = True
        
        try:
            args = command[2]
        
            func = self.function_dict[command_type]

            if args != '' or args is not None:
                print args;
                irc_msg.msg = func(args)

            else:
                irc_msg.msg = func('help')
                
        except:
            irc_msg.msg =  self.help(None)
            logging.error('Error processing commands')
            
        return irc_msg
