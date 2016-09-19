import re
import urllib2
import logging

from ircmessage import IRCMessage

from plugins.texttriggerplugin import TextTriggerPlugin

class WebTitle(TextTriggerPlugin):
    def __init__(self):
        self.trigger = re.compile(
            """((http|https)://((?!twitter))\S*)""",
            re.IGNORECASE
        )

    def get_title(self, url):
        _title_re = re.compile("<title>(.+?)</title>")
        _response = urllib2.urlopen(url)
        content = _response.read()
        return _title_re.search(content).group(1)

    def execute(self, ircMsg, userRole, regex_groups):
        try:
            url = regex_groups[0][0]
            msg = IRCMessage()
            msg.channel = ircMsg.channel
            msg.msg = " - ".join([
                self.get_title(url),
                url
            ])
        except:
            logging.error(":(")

        return msg
