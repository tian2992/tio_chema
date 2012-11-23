# Based on the minimal example: http://ur1.ca/6wjpm
# by thomson_matt
from yapsy.IPlugin import IPlugin

class Example(IPlugin):
    # This constructor is optional
    def __init__(self):
        # Possible roles
        # unknow # Not authenticated
        # know # this means authenticated
        # admin
        self.roles = {}
    # This is the default method called by the bot when we try to use
    # it from irc.  If the plugin is intended for internal use just
    # call return in this method.
    def execute(self, ircMsg):
        return

    def getRole(self, user):
        if user in self.roles:
            return self.roles[user]
        else:
            return

    def setRole(self, user, role):
        print "SetRole called, " + user #debug
        if role == "know":
            self.roles[user] = role
        else:
            self.roles[user] = "unknow"
        print "Current roles:"
        print self.roles
        return

    def deleteRole(self, user):
        if user in self.roles:
            del self.roles[user]
        print "delete role called " + user

