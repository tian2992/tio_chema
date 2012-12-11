#!/usr/bin/env python2
import time, sys

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

from configobj import ConfigObj

class ChemaBot(irc.IRCClient):
  """The main IRC bot class.

  ChemaBot mainly handles message dispatching
  to plugins and other general bot functions.
  """

  def __init__(self, nickname):
    self.nickname = nickname
    self.pluginsInit()

  def connectionMade(self):
    irc.IRCClient.connectionMade(self)

  def connectionLost(self, reason):
    irc.IRCClient.connectionLost(self, reason)

  # Callback Functions

  def signedOn(self):
    """Called when bot has succesfully signed on to server."""
    self.join(self.factory.channel)


  def joined(self, channel):
    """This will get called when the bot joins the channel."""
    self.msg("Hello World!") #TODO(tian): remove
    pass

  def privmsg(self, user, channel, msg):
    """This will get called when the bot receives a message."""
    user = user.split('!', 1)[0]

    # Check to see if they're sending me a private message
    if channel == self.nickname:
      msg = "It isn't nice to whisper!  Play nice with the group."
      self.msg(user, msg)
      return

    # Otherwise check to see if it is a message directed at me
    # if msg.startswith(self.nickname + ":"):
    if msg.startswith(self.nickname):
      pass

  def parseMessage(self, ircMsg):
    # Look for a plugin
    # Split the msg in strings
    word_list = ircMsg.getMsg().split(' ',2)
    # This is a possible command
    command = word_list[1].lower()

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


class ChemaBotFactory(protocol.ClientFactory):

  def __init__(self, channel, config):
    self.channel = channel
    # Load the configuration file
    self.config = config
    self.filename = self.config['log_file']

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
  #try:
    # Load the configuration file
    config = ConfigObj(sys.argv[1])
    # create factory protocol and application
    bot_factory = ChemaBotFactory(sys.argv[1], config)
    reactor.connectTCP(config['irc_server'],
                       config.as_int('irc_port'),
                       bot_factory)
    reactor.run()
  #except:
   # print("Usage: python bot_chema.py config_file.cf")
   # exit(1)