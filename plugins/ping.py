# Based on the minimal example: http://ur1.ca/6wjpm
# by thomson_matt
from yapsy.IPlugin import IPlugin

class PluginPing(IPlugin):
    def execute(self, ircMsg, userRole):
        msg = "%s: pong" % ircMsg.getUser()
        ircMsg.setMsg(msg)
        return ircMsg
