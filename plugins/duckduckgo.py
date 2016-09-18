import re

import duckduckgo

from ircmessage import IRCMessage

from plugins.baseactionplugin import BaseActionPlugin

class DuckDuckGo(BaseActionPlugin):
    def __init__(self):
        BaseActionPlugin.__init__(self)
        self.synchronous = False

    def execute(self, ircMsg, userRole, *args, **kwargs):
        irc_msg = IRCMessage()
        irc_msg.channel = ircMsg.channel
        irc_msg.user = ircMsg.user
        irc_msg.directed = True

        try:

            search_query_list = ircMsg.msg.split(' ')
            search_query_list.pop(0)
            search_query = ' '.join(search_query_list)

            result = duckduckgo.query(search_query)

            irc_msg.msg = ' - '.join([
                result.results[0].text,
                result.results[0].url
            ])

        except:
            irc_msg.msg = 'Cagadales, el API del pato es una mierda'\
            ' https://duckduckgo.com/api'

        return irc_msg
