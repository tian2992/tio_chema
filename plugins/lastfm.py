from plugins.baseactionplugin import BaseActionPlugin
from ircmessage import IRCMessage
from ConfigParser import SafeConfigParser

import logging

import pylast

class PluginLastfm(BaseActionPlugin):
  def __init__(self):
    BaseActionPlugin.__init__(self)
    try:
      parser = SafeConfigParser()
      parser.read('plugins/lastfm.yapsy-plugin')
      self._api_key = parser.get('Auth', 'key')
    except:
      logging.error("Error when parsing lastfm plugin info.")

    self.last = pylast.get_lastfm_network(api_key = self._api_key)

  def execute(self, ircMsg, userRole, *args, **kwargs):
    m = IRCMessage()
    m.user = ircMsg.user
    m.channel = ircMsg.channel

    user_s = ircMsg.msg.split(' ')[1]
    logging.info("Getting last.fm user {0}".format(user_s))
    user = self.last.get_user(user_s)

    try:
      recent_tracks = user.get_recent_tracks()
    except:
      #TODO: Localize
      m.msg = "No user with that name"
      return m

    try:
      last_track = recent_tracks[0].track
    except:
      m.msg = "No tracks avaliable for that username"
      return m

    #TODO: add localization
    m.msg = u"Listening to: {0} - {1}".format(last_track.title, last_track.artist.name)

    return m