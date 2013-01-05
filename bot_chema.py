#!/usr/bin/env python2
import time, sys
import logging

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, threads
from twisted.python import log
from yapsy.PluginManager import PluginManager
from configobj import ConfigObj

from ircmessage import IRCMessage
from plugins.baseactionplugin import BaseActionPlugin
from plugins.texttriggerplugin import TextTriggerPlugin

class ChemaBot(irc.IRCClient):
  """The main IRC bot class.

  ChemaBot mainly handles message dispatching
  to plugins and other general bot functions.
  """

  def __init__(self, nickname):
    self.nickname = nickname
    self.pluginsInit()

  def pluginsInit(self):
    logging.basicConfig(level=logging.DEBUG)
    self.pm = PluginManager(
      categories_filter = {
        "BaseActions" : BaseActionPlugin,
        "TextActions" : TextTriggerPlugin
      },
      directories_list=["plugins"],)

    self.pm.collectPlugins()
    for pluginInfo in self.pm.getAllPlugins():
      #TODO: turn into logger
      print(pluginInfo.name)
      self.pm.activatePluginByName(pluginInfo.name)

    # TODO: create a list of localized ("_()") plugin triggers
    # Create a dictionary of the names of all the plugins
    self.action_plugins = {}
    # List of the regexes and plugins
    self.regex_plugins = []
    # TODO: specify categories of plugins with each trigger http://yapsy.sourceforge.net/PluginManager.html
    for pluginInfo in self.pm.getPluginsOfCategory("BaseActions"):
      self.action_plugins[pluginInfo.name] = pluginInfo.plugin_object

    for pluginInfo in self.pm.getPluginsOfCategory("TextActions"):
      self.regex_plugins.append((pluginInfo.plugin_object.trigger, pluginInfo.plugin_object))


  # Useful for debugging
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
    message = ircm.msg
    for (regex, plugin) in self.regex_plugins:
      result_groups = regex.findall(message)

      if result_groups:
        ## Only takes the first of the matches.
        result = result_groups[0]
        d = threads.deferToThread(plugin.execute, ircm, None, result)
        d.addCallback(self.emitMessage)


    trigger = self.factory.main_trigger
    if message.startswith(trigger):
      word_list = message.split(' ')
      command = word_list[0].lstrip(trigger)
      ## TODO: Consider sending the split word list.
      try:
        plugin = self.action_plugins[command]
      except KeyError:
        ## TODO: Log missing plugin.
        print("Command {0} missing".format(command))
        return
      d = threads.deferToThread(plugin.execute, ircm, None)
      d.addCallback(self.emitMessage)

    ## TODO: add main_triggers to nickname
    if ircm.msg.startswith(self.nickname):
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
    observer = log.PythonLoggingObserver()
    observer.start()
    reactor.connectTCP(config['irc_server'],
                       config.as_int('irc_port'),
                       bot_factory)
    reactor.run()
  except:
    print("Usage: python bot_chema.py config_file.cf")
    exit(1)
