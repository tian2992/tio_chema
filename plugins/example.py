# Based on the minimal example: http://ur1.ca/6wjpm
# by thomson_matt
from yapsy.IPlugin import IPlugin

class Example(IPlugin, userRole):
    # This constructor is optional
    def __init__(self):
        self.counter = 0
    # This is the default method called by the bot when we try to use
    # it from irc.  If the plugin is intended for internal use just
    # call return in this method.
    def execute(self, ircMsg):
        self.counter += 1
        if self.counter > 10:
            self.counter = 0
        msg = "This is the example plugin, counter " + str(self.counter)
        ircMsg.setMsg(msg)
        return ircMsg
