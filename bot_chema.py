#!/usr/bin/env python2
import time, sys, re
import logging

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, threads, defer
from twisted.python import log
from yapsy.PluginManager import PluginManager
from configobj import ConfigObj

from ircmessage import IRCMessage
from plugins.baseactionplugin import BaseActionPlugin
from plugins.texttriggerplugin import TextTriggerPlugin

from db_mgr import DatabaseManager

# global constant
RE_TYPE = re.compile('').__class__

class ChemaBot(irc.IRCClient):
  """The main IRC bot class.

  ChemaBot mainly handles message dispatching
  to plugins and other general bot functions.
  """

  def __init__(self, nickname):
    self.nickname = nickname
    logging.basicConfig(level=logging.DEBUG)
    self.plugins_init()
    #TODO: database location should be taken fron config file.
    self.db_manager = DatabaseManager("bot.db")

  def plugins_init(self, is_reloading = False):
    if is_reloading:
      logging.info("Deactivating All Plugins")
      for pluginInfo in self.pm.getAllPlugins():
        self.pm.deactivatePluginByName(pluginInfo.name)

    self.pm = PluginManager(
      categories_filter = {
        "BaseActions" : BaseActionPlugin,
        "TextActions" : TextTriggerPlugin,
      },
      directories_list=["plugins"],)

    self.pm.collectPlugins()
    for pluginInfo in self.pm.getAllPlugins():
      ## This stops the plugins marked as Disable from being activated.
      ## Consider changing activations to category plugins load.
      if (not pluginInfo.details.has_option("Core", "Disabled")):
        self.pm.activatePluginByName(pluginInfo.name)
        logging.info("Plugin {0} activated".format(pluginInfo.name))

    # TODO: create a list of localized ("_()") plugin triggers
    # Create a dictionary of the names of all the plugins
    self.action_plugins = {}
    # List of the regexes and plugins
    self.text_trigger_plugins = []
    # TODO: specify categories of plugins with each trigger http://yapsy.sourceforge.net/PluginManager.html

    for pluginInfo in self.pm.getPluginsOfCategory("BaseActions"):
      if (not pluginInfo.details.has_option("Core", "Disabled")):
        self.action_plugins[pluginInfo.name] = pluginInfo.plugin_object

    logging.debug("Action plugins: {0}".format(self.action_plugins))

    for pluginInfo in self.pm.getPluginsOfCategory("TextActions"):
      if (not pluginInfo.details.has_option("Core", "Disabled")):
        self.text_trigger_plugins.append((pluginInfo.plugin_object.trigger, pluginInfo.plugin_object))

    logging.debug("Regex plugins: {0}".format(self.text_trigger_plugins))


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
      self.msg(channel, message.render().encode('utf-8'))
    ## Handling private messages.
    elif message.channel == self.nickname:
      self.msg(message.user.split("!")[0], message.render().encode('utf-8'))
    else:
      self.msg(message.channel, message.render().encode('utf-8'))

  def _parseAndExecute(self, ircm):
    """Recieves an IRCMessage, detects the command and triggers the appropiate plugin."""

    message = ircm.msg
    for (text_trigger, plugin) in self.text_trigger_plugins:
      if isinstance(text_trigger, RE_TYPE):
        result = text_trigger.findall(message)
      #TODO: specify the info sent to the trigger.
      else:
        #trigger.fire(message, *args, **kwargs)
        result = text_trigger.fire(ircm)

      if result:
        d = threads.deferToThread(plugin.execute, ircm, None, result)
        d.addCallback(self.emitMessage)

    ## Main Command trigger is commonly '!'
    trigger = self.factory.main_trigger
    if message.startswith(trigger) or message.startswith(self.nickname):
      word_list = message.split(' ')
      if message.startswith(trigger):
        command = word_list[0].lstrip(trigger)
      elif message.startswith(self.nickname):
        try:
          command = word_list[1].strip()
        except IndexError:
          logging.warning('Invalid call: "{0}"'.format(ircm.render()))
          return

      ## TODO: Reload should be dependant on userRole
      ## TODO: Localize
      if command == "reload":
        self.plugins_init(is_reloading=True)
        return

      ## TODO: Consider sending the split word list.
      try:
        plugin = self.action_plugins[command]
      except KeyError:
        logging.warning("Command {0} missing".format(command))
        return

      if plugin.synchronous:
        d = defer.maybeDeferred(plugin.execute, ircm, None)
      else:
        d = threads.deferToThread(plugin.execute, ircm, None, connection = self.db_manager)
      d.addCallback(self.emitMessage)
      return

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
    #print message

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

def main():
  try:
    if len(sys.argv) < 2:
      config = ConfigObj("./bot_devel.cf")
    else:
      # Load the configuration file
      config = ConfigObj(sys.argv[1])
    # create factory protocol and application
    print(sys.argv)
    bot_factory = ChemaBotFactory(config)
    observer = log.PythonLoggingObserver()
    observer.start()
    reactor.connectTCP(config['irc_server'],
                       config.as_int('irc_port'),
                       bot_factory)
    reactor.run()
  except Exception as e:
    print(repr(e))
    print("Usage: python bot_chema.py config_file.cf")
    exit(1)


if __name__ == '__main__':
  main()

main()