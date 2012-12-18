#!/usr/bin/env python2
import time, sys

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, threads
from twisted.python import log
from yapsy.PluginManager import PluginManager
from yapsy.ConfigurablePluginManager import ConfigurablePluginManager
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
    # TODO: create a list of localized ("_()") plugin triggers
    # Create a list of the names of all the plugins
    self.plugins = {}
    for pluginInfo in self.simplePluginManager.getAllPlugins():
      self.plugins[pluginInfo.name] = pluginInfo.plugin_object


  # Useful for debuggin
  def listPlugins(self):
      print 'Plugins:'
      for item in self.plugins:
          print item

  def signedOn(self):
    """Called when bot has succesfully signed on to server."""
    self.join(self.factory.channel)

  def joined(self, channel):
    """This will get called when the bot joins the channel."""
    pass

  def emitMessage(self, message, channel = None):
    """A function to abstract message emission."""
    if channel:
      self.say(channel, message)
    else:
      self.say(message.channel, message.render())

  def _parseAndExecute(self, ircm):
    """Recieves an IRCMessage, detects the command and triggers the appropiate plugin."""
    ## Main Command trigger is commonly '!'
    trigger = self.factory.main_trigger
    if ircm.msg.startswith(trigger):
      word_list = ircm.msg.split(' ')
      command = word_list[0].lstrip(trigger)
      ## TODO: Consider sending the split word list.
      self._execute_command(command, ircm)

    ## TODO: add main_triggers to nickname
    if ircm.msg.startswith(self.nickname):
      pass


  def _execute_command(self, command, message):
    ## TODO: add support for different, not threaded plugins
    plugin = self.plugins[command]
    d = threads.deferToThread(plugin.execute, message, None)
    d.addCallback(self.emitMessage)

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

    #TODO: add channel trigger plugins (user defined actions)

    self._parseAndExecute(message)


class ChemaBotFactory(protocol.ClientFactory):

  def __init__(self, config):
    self.config = config
    # TODO add multi channel support
    self.channel = "#"+self.config['channel']
    self.filename = self.config['log_file']
    self.main_trigger = self.config['main_command_trigger']

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
