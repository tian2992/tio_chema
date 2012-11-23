# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.


"""
An example IRC log bot - logs a channel's events to a file.

If someone says the bot's name in the channel followed by a ':',
e.g.

  <foo> logbot: hello!

the bot will reply:

  <logbot> foo: I am a log bot

Run this script with two arguments, the channel name the bot should
connect to, and the configuration file, e.g.:

  $ python ircLogBot.py pepito bot.cf

will log channel #test to the file 'test.log'.
"""


# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

# system imports
import time, sys

# For ultra simple handling of configuration files
# http://www.voidspace.org.uk/python/configobj.html
# License: http://opensource.org/licenses/BSD-3-Clause
from configobj import ConfigObj

# Yapsy A simple plugin system for Python applications
# http://yapsy.sourceforge.net/
# License: http://www.opensource.org/licenses/bsd-license.php
from yapsy.PluginManager import PluginManager

class MessageLogger:
    """
    An independent logger class (because separation of application
    and protocol logic is a good thing).
    """
    def __init__(self, file):
        self.file = file

    def log(self, message):
        """Write a message to the file."""
        timestamp = time.strftime("[%H:%M:%S]", time.localtime(time.time()))
        self.file.write('%s %s\n' % (timestamp, message))
        self.file.flush()

    def close(self):
        self.file.close()

class IrcMsg(irc.IRCClient):
    """An IRC message."""
    def __init__(self, channel=None, msg=None, user=None):
        if channel is None:
            self.channel = ""
        else:
            self.channel = channel
        if msg is None:
            self.msg = ""
        else:
            self.msg = msg
        if user is None:
            self.user = ""
        else:
            self.user = user


    def setChannel(self, channel):
        self.channel = channel

    def setMsg(self, msg):
        self.msg = msg

    def setUser(self, user):
        self.user = user

    def getChannel(self):
        return self.channel

    def getMsg(self):
        return self.msg

    def getUser(self):
        return self.user


class LogBot(irc.IRCClient):
    """A logging IRC bot."""

    def __init__(self, nickname):
        self.nickname = nickname
        self.pluginsInit() #Yay I have plugins :)

    def pluginsInit(self):
        # Build the manager
        self.simplePluginManager = PluginManager()
        # Tell it the default place(s) where to find plugins
        self.simplePluginManager.setPluginPlaces(["plugins"])
        # Load all plugins
        self.simplePluginManager.collectPlugins()
        # Create a list of the names of all the plugins
        self.listOfPlugins = []
        for pluginInfo in self.simplePluginManager.getAllPlugins():
            self.listOfPlugins.append(pluginInfo.name)
        # Get the security plugin
        plugin = self.simplePluginManager.getPluginByName("security")
        self.securityPlugin = plugin.plugin_object


    # Useful for debuggin
    def listPlugins(self):
        print 'Plugins:'
        for item in self.listOfPlugins:
            print item

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.logger = MessageLogger(open(self.factory.filename, "a"))
        self.logger.log("[connected at %s]" % 
                        time.asctime(time.localtime(time.time())))

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        self.logger.log("[disconnected at %s]" % 
                        time.asctime(time.localtime(time.time())))
        self.logger.close()


    # callbacks for events

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        self.join(self.factory.channel)

    def joined(self, channel):
        """This will get called when the bot joins the channel."""
        self.logger.log("[I have joined %s]" % channel)

    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""
        user = user.split('!', 1)[0]
        self.logger.log("<%s> %s" % (user, msg))

        ircMsg = IrcMsg(channel,msg,user)
        
        # Check to see if they're sending me a private message
        if channel == self.nickname:
            msg = "It isn't nice to whisper!  Play nice with the group."
            self.msg(user, msg)
            return

        # Otherwise check to see if it is a message directed at me
        # if msg.startswith(self.nickname + ":"):
        if msg.startswith(self.nickname):
            ircMsg = self.parseMessage(ircMsg)
            if(ircMsg):
                self.logger.log("<%s> %s" % (self.nickname, ircMsg.getMsg()))
                self.msg(ircMsg.getChannel(), ircMsg.getMsg())

    def parseMessage(self, ircMsg):
        # Check his role
        userRole = self.securityPlugin.getRole(ircMsg.getUser())
        # If the role is unknow
        if not userRole:
            # Checking with nickserv
            self.msg("NickServ", "ACC " + ircMsg.getUser())
        else:
            print ircMsg.getUser() + " role is " + userRole

        # Look for a plugin
        # Split the msg in three strings
        listOfWords = ircMsg.getMsg().split(' ',2)
        # This is a possible command
        command = listOfWords[1].lower()

        # Check if the plugin exists
        if command in self.listOfPlugins:
            # Call the plugin
            plugin = self.simplePluginManager.getPluginByName(command)
            ircMsg = plugin.plugin_object.execute(ircMsg, userRole)
            return ircMsg

        # Here we should pass the command to the -action- plugin
        # plugin = self.simplePluginManager.getPluginByName("action")
        #    msg = plugin.plugin_object.execute(msg, user)
        #    return msg

        # This is the default action
        # I will replace this, with an empty return
        # in order to avoid flood
        # return
        msg = "%s: I am a twisted log bot" % ircMsg.getUser()
        ircMsg.setMsg(msg)
        return ircMsg

    def action(self, user, channel, msg):
        """This will get called when the bot sees someone do an action."""
        user = user.split('!', 1)[0]
        self.logger.log("* %s %s" % (user, msg))

    # irc callbacks

    def irc_NICK(self, prefix, params):
        """Called when an IRC user changes their nickname."""
        old_nick = prefix.split('!')[0]
        new_nick = params[0]
        self.logger.log("%s is now known as %s" % (old_nick, new_nick))
        self.securityPlugin.deleteRole(old_nick)

    def irc_NOTICE(self, prefix, params):
        """This will get called when the bot receives a notice."""
        # Print all the notices
        print "IRC Notice:"
        print "Prefix: " + prefix
        print params
        print "IRC Notice end."
        # Look for NickServ notices
        prefixList = prefix.split('!')
        if prefixList[0] == "NickServ" and prefixList[1] == "NickServ@services.":
            paramsList = params[1].split()
            if paramsList[1] == "ACC":
                if paramsList[2] == "3":
                    # Set up the role of user
                    self.securityPlugin.setRole(paramsList[0], "know")
                    print paramsList[0] + " is now authenticated"
                else:
                    self.securityPlugin.setRole(paramsList[0], "unknow")

    def irc_PART(self, prefix, params):
        """Called when an IRC user leaves the channel."""
        nick = prefix.split('!')[0]
        # new_nick = params[0]
        # self.logger.log("%s is now known as %s" % (old_nick, new_nick))
        self.securityPlugin.deleteRole(nick)
        # Debug
        print "irc_PART, prefix:"
        print prefix
        print "params:"
        print params

    def irc_QUIT(self, prefix, params):
        """Called when an IRC user quits the network."""
        nick = prefix.split('!')[0]
        # new_nick = params[0]
        # self.logger.log("%s is now known as %s" % (old_nick, new_nick))
        self.securityPlugin.deleteRole(nick)
        # Debug
        print "irc_QUIT, prefix:"
        print prefix
        print "params:"
        print params

    def irc_JOIN(self, prefix, params):
        """Called when an IRC user joins to the channel."""
        nick = prefix.split('!')[0]
        # new_nick = params[0]
        # self.logger.log("%s is now known as %s" % (old_nick, new_nick))
        # Checking with nickserv
        self.msg("NickServ", "ACC " + nick)
        # Debug
        print "irc_JOIN, prefix:"
        print prefix
        print "params:"
        print params

    def irc_KICK(self, prefix, params):
        """Called when an IRC user kicks other user."""
        nick = prefix.split('!')[0]
        kicked_nick = params[1]
        channel = params[0]
        comment = params[2]
        self.logger.log("*** %s has kicked %s off channel %s : %s" % (nick, kicked_nick, channel, comment))
        self.securityPlugin.deleteRole(nick)
        # Debug
        print "irc_KICK, prefix:"
        print prefix
        print "params:"
        print params

    # For fun, override the method that determines how a nickname is changed on
    # collisions. The default method appends an underscore.
    def alterCollidedNick(self, nickname):
        """
        Generate an altered version of a nickname that caused a collision in an
        effort to create an unused related name for subsequent registration.
        """
        return nickname + '^'



class LogBotFactory(protocol.ClientFactory):
    """A factory for LogBots.

    A new protocol instance will be created each time we connect to the server.
    """

    def __init__(self, channel, config):
        self.channel = channel
        # Load the configuration file
        self.config = config
        self.filename = self.config['logFile']

    def buildProtocol(self, addr):
        p = LogBot(self.config['nickname'])
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()


if __name__ == '__main__':
    # initialize logging
    log.startLogging(sys.stdout)

    # Load the configuration file
    config = ConfigObj(sys.argv[2])

    # create factory protocol and application
    f = LogBotFactory(sys.argv[1], config)

    # connect factory to this host and port
    reactor.connectTCP(config['ircServer'], config.as_int('ircPort'), f)

    # run bot
    reactor.run()
