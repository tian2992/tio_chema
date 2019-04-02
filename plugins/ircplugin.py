from yapsy.IPlugin import IPlugin
import logging
from ConfigParser import SafeConfigParser

class IRCPlugin(IPlugin):

  def __init__(self):
    """
    Args:
      synchronous: If the plugin can be executed without blocking, syncrhonous can be set to true, to speed up execution. Please use with care.
    """
    self.synchronous = False

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
          logging.error("Error when parsing plugin info.", exc_info=e)

      return conf_results
