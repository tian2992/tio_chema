from plugins.baseactionplugin import BaseActionPlugin
from ircmessage import IRCMessage
from ConfigParser import SafeConfigParser

import logging

import pylast

#TODO: Localize
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

    #TODO: Localize commands
    self.function_dict = {
                          "user": self.get_user_track,
                          "artist": self.get_artist_tracks,
                          #"genre": get_genre_artists,
                          #"track": get_related_tracks,
                         }
                         
  def get_artist_tracks(self, ircMsg):
    """Gets the selected user track, returns an IRCMessage"""
    m = IRCMessage(user=ircMsg.user, channel=ircMsg.channel)
    artist_s = ircMsg.msg.split(' ')[2]
    artist = self.last.get_artist(artist_s)
    logging.info("Getting last.fm artist {0}".format(artist_s))
    try:
      similar_artists = artist.get_similar()
    except:
      m.msg = "No artist with that name"
      return m
    
    similar_artists_s = ", ".join(map(lambda a: a.get_name(), similar_artists))
    
    m.msg = u"Artists similar to {0} are: {1}".format(artist_s, similar_artists_s)
    
    return m
    

  def get_user_track(self, ircMsg):
    """Gets the selected user track, returns an IRCMessage"""
    m = IRCMessage(user=ircMsg.user, channel=ircMsg.channel)
    user_s = ircMsg.msg.split(' ')[2]
    user = self.last.get_user(user_s)    
    logging.info("Getting last.fm user {0}".format(user_s))
    try:
      recent_tracks = user.get_recent_tracks()
    except:
      m.msg = "No user with that name"
      return m

    try:
      last_track = recent_tracks[0].track
    except:
      m.msg = "No tracks avaliable for that username"
      return m

    m.msg = u'User {0} is listening to: {1} - {2}'.format(user_s, last_track.title, last_track.artist.name)
    return m

  def execute(self, ircMsg, userRole, *args, **kwargs):
    command_s = ircMsg.msg.split(' ')[1]
    try:
      func = self.function_dict[command_s]
      return func(ircMsg)
    except:
      ircMsg.msg = "Incorrect last.fm command."
      return ircMsg