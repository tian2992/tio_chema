from plugins.texttriggerplugin import TextTriggerPlugin
from ConfigParser import SafeConfigParser
from ircmessage import IRCMessage

import tweepy
import re
import logging


class TwitterTextPlugin(TextTriggerPlugin):

  def __init__(self):
    self.trigger = re.compile(
      """((http|https)://(twitter.com|identi.ca)/(([A-Za-z0-9_]{1,15})/status|notice)/([\d]*))""",
      re.IGNORECASE)

    conf_vals = self.get_configuration('plugins/twitterText.yapsy-plugin', [
                                       {"section": "Auth", "conf": "consumer_token"},
                                       {"section": "Auth", "conf": "consumer_secret"},
                                       {"section": "Auth", "conf": "access_key"},
                                       {"section": "Auth", "conf": "access_secret"},
                                       ])

    self.consumer_token = conf_vals.get('consumer_token')
    self.consumer_secret = conf_vals.get('consumer_secret')
    self.access_key = conf_vals.get('access_key')
    self.access_secret = conf_vals.get("access_secret")

    auth = tweepy.OAuthHandler(self.consumer_token, self.consumer_secret)
    auth.set_access_token(self.access_key, self.access_secret)

    self.api = tweepy.API(auth)

  def get_configuration(self, config_file_string, attribute_dict_list = [{}]):
    """
    Gets the configuration from a config file.

    Args:
      config_file_string: the string of the file to configure
      attribute_dict_list: a list of dictionaries with keys "section" and "conf" with the section of
        the conf file and the value of it.

    Returns: a dictionary with keys as attribute_dict_list's "conf"s.
    """

    conf_results = {}

    try:
      parser = SafeConfigParser()
      parser.read(config_file_string)

      for di in attribute_dict_list:
        conf_results[di["conf"]] = parser.get(di["section"], di["conf"])

    except Exception as e:
      logging.error("Error when parsing identica plugin info.", exc_info=e)

    return conf_results

  def execute(self, ircMsg, userRole, regex_group):
    m = IRCMessage()
    m.channel = ircMsg.channel
    r_group = regex_group[0]

    status = self.api.get_status(r_group[-1])
    if r_group[-2]:
      author = r_group[-2]
    else:
      author = status.author.screen_name
    m.msg = u"@{0}: {1}".format(author, status.text)
    m.user = ircMsg.user
    return m
