#!/usr/bin/env python2
import time, sys

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

from configobj import ConfigObj

from ircmessage import IRCMessage

class ChemaBot(irc.IRCClient):
  """The main IRC bot class.

  ChemaBot mainly handles message dispatching
  to plugins and other general bot functions.
  """

  def __init__(self, nickname):
    self.nickname = nickname
    self.pluginsInit()
      
  def pluginsInit(self):
    self.simplePluginManager = PluginManager()
    self.simplePluginManager.setPluginPlaces(["plugins"])
    self.simplePluginManager.collectPlugins()
    # Create a list of the names of all the plugins
    # TODO: create a list of plugin triggers
    self.listOfPlugins = {}
    for pluginInfo in self.simplePluginManager.getAllPlugins():
      #TODO: consider adding several entries for the different names of the plugin
      self.listOfPlugins[pluginInfo.name](pluginInfo.plugin_object)
    ## Get the security plugin
    #plugin = self.simplePluginManager.getPluginByName("security")
    #self.securityPlugin = plugin.plugin_object


  # Useful for debuggin
  def listPlugins(self):
      print 'Plugins:'
      for item in self.listOfPlugins:
          print item

  def signedOn(self):
    """Called when bot has succesfully signed on to server."""
    self.join(self.factory.channel)

  def joined(self, channel):
    """This will get called when the bot joins the channel."""
    pass

  def privmsg(self, user, channel, msg):
    """Gets called when the bot receives a message in a channel or via PM.

    Here is contained the main logic of tio_chema. Should dispatch messages
    to the plugins registered, depending if they register for a global or
    a specific trigger keyword.
    It blocks, so it should not include heavy or slow logic.

    Args:
      user: A string containing the origin user.
      channel: A string with the originating channel or PM channel.
      msg: A string containing the message recieved.

    """
    
    message = IRCMessage(channel, msg, user)

    #TODO: add logging
    #print msg

    #TODO: add channel trigger plugins

    if msg.startswith(self.nickname):
      self.say(channel, "Hello "+ user)
      
      #TODO: add nick trigger plugins


class ChemaBotFactory(protocol.ClientFactory):

  def __init__(self, config):
    self.config = config
    # TODO add multi channel support
    self.channel = "#"+self.config['channel']
    self.filename = self.config['log_file']

  def buildProtocol(self, addr):
    p = ChemaBot(self.config['nickname'])
    p.factory = self
    return p

  def clientConnectionLost(self, connector, reason):
    """If we get disconnected, reconnect to server."""
    connector.connect()

  def clientConnectionFailed(self, connector, reason):
    print "connection failed:", reason
    reactor.stop()

if __name__ == '__main__':
  try:
    # Load the configuration file
    config = ConfigObj(sys.argv[1])
    # create factory protocol and application
    bot_factory = ChemaBotFactory(config)
    reactor.connectTCP(config['irc_server'],
                       config.as_int('irc_port'),
                       bot_factory)
    reactor.run()
  except:
    print("Usage: python bot_chema.py config_file.cf")
    exit(1)