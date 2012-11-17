# Based on the minimal example: http://ur1.ca/6wjpm
# by thomson_matt
from yapsy.IPlugin import IPlugin

class Example(IPlugin):
    # This is the default method called by the bot when we try to use
    # it from irc.  If the plugin is intended for internal use just
    # call return in this method.
    def execute(self, msg, user):
        return "This is the example plugin"
