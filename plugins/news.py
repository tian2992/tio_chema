import requests
import types
import re
from random import choice
from plugins.baseactionplugin import BaseActionPlugin
from ircmessage import IRCMessage
from plugins.lengua import _
from bs4 import BeautifulSoup

try:
    import xml.etree.cElementTree as ETree
except ImportError:
    import xml.etree.ElementTree as ETree

class News(BaseActionPlugin):
    def __init__(self):
        BaseActionPlugin.__init__(self)
        self.synchronous = False

    def execute(self, ircMsg, userRole, *args, **kwargs):
        user = ircMsg.user
        m = IRCMessage()
        url = 'http://feeds.reuters.com/reuters/topNews'

        req = requests.get(url)
        tree = ETree.fromstring(req.text.encode("UTF-8"))
        tag_list = tree.findall("./channel/item")
        tagita = choice(tag_list)
        respuesta = u"{} | {}".format(tagita.find("title").text, tagita.find("link").text)

        m.msg = respuesta
        m.channel = ircMsg.channel
        m.user = user
        m.directed = True
        return m
