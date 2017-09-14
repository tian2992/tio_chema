import re
import logging
from ConfigParser import SafeConfigParser

from ircmessage import IRCMessage
from twython import Twython

from plugins.texttriggerplugin import TextTriggerPlugin

class TuiterText(TextTriggerPlugin):

    def __init__(self):
        self.trigger = re.compile(
            """((http|https)://(twitter.com)/(([A-Za-z0-9_]{1,15})/"""\
            """status)/([\d]*))""",
            re.IGNORECASE
        )

        tuiter_conf = self.get_configuration('plugins/tuiterText.yapsy-plugin',
                                             [
                                                 {
                                                     "section" : "Auth",
                                                     "conf" : "app_key"
                                                 },
                                                 {
                                                     "section" : "Auth",
                                                     "conf" :"app_secret"
                                                 }
                                             ])


        self.api = Twython(tuiter_conf.get("app_key"),
                           tuiter_conf.get("app_secret"))

    def execute(self, ircMsg, userRole, regex_groups):
        m = IRCMessage()
        m.channel = ircMsg.channel
        regex_group = regex_groups[0]

        status = self.api.show_status(id = regex_group[-1])
        author = regex_group[-2]

        m.msg = u"@{0}: {1}".format(author, status.get("text"))
        m.user = ircMsg.user

        return m
