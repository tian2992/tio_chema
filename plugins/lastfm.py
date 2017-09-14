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
                          "tag_artists": self.get_tag_artists,
                          "tag_albums": self.get_tag_albums,
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


  def get_artist_tracks(self, ircMsg):
    """Gets the selected user track, returns an IRCMessage"""
    m = IRCMessage(user=ircMsg.user, channel=ircMsg.channel)
    artist_s = " ".join(ircMsg.msg.split(' ')[2::])
    artist = self.last.get_artist(artist_s)
    logging.info("Getting last.fm artist {0}".format(artist_s))
    try:
      similar_artists = artist.get_similar(limit = 5)
    except:
      m.msg = "No artist with that name."
      return m
    similar_artists_s = u", ".join(map(lambda a: a[0].get_name(), similar_artists))
    m.msg = u"Artists similar to {0} are: {1}".format(artist.get_name().decode("utf-8"), similar_artists_s)
    return m

  def get_user_track(self, ircMsg):
    """Gets the selected user track, returns an IRCMessage."""
    m = IRCMessage(user=ircMsg.user, channel=ircMsg.channel)
    user_fm = ircMsg.tokens[-1]
    user = self.last.get_user(user_s)
    logging.info("Getting last.fm user {0}".format(user_fm))
    try:
      recent_tracks = user.get_recent_tracks()
    except:
      m.msg = "No user with that name."
      return m

    try:
      last_track = user.get_now_playing()
      if not last_track:
        last_track = recent_tracks[0].track
    except:
      m.msg = "No tracks avaliable for that username."
      return m

    tags_string =  u" , ".join([tag[0].name for tag in last_track.get_top_tags(4)])

    m.msg = u'User {0} is listening to: {1} - {2}: tags [ {3} ]'.format(user_s, last_track.title,
      last_track.artist.name, tags_string)
    return m


  def get_tag_artists(self, ircMsg):
    """Gets the artists that match the tag, returns an IRCMessage"""
    m = IRCMessage(user=ircMsg.user, channel=ircMsg.channel)
    tag_s = " ".join(ircMsg.msg.split(' ')[2::])
    tag = self.last.get_tag(tag_s)
    logging.info("Getting last.fm tag {0}".format(tag_s))
    try:
      tag_artists = tag.get_top_artists()[:4:]
    except:
      m.msg = "No tag with that name"
      return m
    tag_artists_s = u", ".join(map(lambda a: a[0].get_name(), tag_artists))
    m.msg = u"Artists that match the tag {0} are: {1}".format(tag.get_name().decode("utf-8"), tag_artists_s)
    return m


  def get_tag_albums(self, ircMsg):
    """Gets the artists that match the tag, returns an IRCMessage."""
    m = IRCMessage(user=ircMsg.user, channel=ircMsg.channel)
    tag_s = " ".join(ircMsg.msg.split(' ')[2::])
    tag = self.last.get_tag(tag_s)
    logging.info("Getting last.fm tag {0}".format(tag_s))
    try:
      tag_albums = tag.get_top_albums()[:4:]
    except:
      m.msg = "No tag with that name"
      return m
    tag_albums_s = u", ".join(map(lambda a: a[0].get_name(), tag_albums))
    m.msg = u"Albums that match the tag {0} are: {1}".format(tag.get_name().decode("utf-8"), tag_albums_s)
    return m


  def execute(self, ircMsg, userRole, *args, **kwargs):
    command_s = ircMsg.msg.split(' ')[1]
    try:
        if command_s in self.function_dict:
            func = self.function_dict[command_s]
            return func(ircMsg)
        else:
            return self.get_user_track(ircMsg)
    except:
      logging.exception("Exception in last.fm command.")
      ircMsg.msg = "Incorrect last.fm command."
      return ircMsg
