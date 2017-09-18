import re
import urllib2
import logging

from ircmessage import IRCMessage

from plugins.texttriggerplugin import TextTriggerPlugin

MAXCHARS = 120

class WebTitle(TextTriggerPlugin):
    def __init__(self):
        self.trigger = re.compile(
            """((http|https)://((?!(twitter|tiny)))\S*)""",
            re.IGNORECASE
        )

    @staticmethod
    def get_title(url):
        _title_re = re.compile("<title>(.+?)</title>")
        _response = urllib2.urlopen(url)
        content = _response.read()
        return unicode(_title_re.search(content).group(1)[:MAXCHARS], "utf-8")

    def execute(self, ircMsg, userRole, regex_group):
        try:
            url = regex_group[0][0]
            msg = IRCMessage()
            msg.channel = ircMsg.channel
            msg.msg = WebTitle.get_title(url)
        except:
            logging.error(":(")

        return msg
