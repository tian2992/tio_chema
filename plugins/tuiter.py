import sys
import logging
from ConfigParser import SafeConfigParser

from ircmessage import IRCMessage
from twython import Twython

from plugins.baseactionplugin import BaseActionPlugin

class Tuiter(BaseActionPlugin):

    def __init__(self):
        BaseActionPlugin.__init__(self)
        self.synchronous = False

        tuiter_conf = self.get_configuration('plugins/tuiter.yapsy-plugin',
                                             [
                                                 {
                                                     "section" : "Auth",
                                                     "conf" : "app_key"
                                                 },
                                                 {
                                                     "section" : "Auth",
                                                     "conf" :"app_secret"
                                                 }
                                             ])


        self.api = Twython(tuiter_conf.get("app_key"),
                           tuiter_conf.get("app_secret"))

        self.func_dict = {
            "pull" : self.pull,
            "help" : self.help
        }

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

    def help(self, command_list):
        command_name = None
        help_dict = {
            "pull" : "Usage: tuiter pull <nick> [twit number] e.g: tuiter pull pepito 1 will return the last twit of pepito", 
            "general" : "It seems you don't know how to use the plugin, please run tuiter help commands",
            "commands" : "pull help"
        }

        if command_list is None:
            command_name = "general"
        else:
            if command_list[2] is not None:
                command_name = command_list[2]
            else:
                command_name = "general"

        return help_dict.get(command_name)

    def pull(self, command_list):

        user = None
        if len(command_list) > 2:
            user = command_list[2]
            if user is None:
                return self.help("pull")

        twit_index = 0
        if len(command_list) == 4:
            if command_list[3] != " ":
                try:
                    twit_index = int(command_list[3]) - 1
                except:
                    twit_index = 0

        try:
            twit = self.api.get_user_timeline(screen_name = user,
                                      count = twit_index + 1)[twit_index]

            if twit is not None:
                return u"En tuiter %(user_name)s dijo: %(twit)s " % {
                    "user_name" : user,
                    "twit" : twit.get("text").replace("\n", " ")
                }
            else:
                return u"Parece que el usuario tiene candadito (en el culo) o hubo un error"
        except:
            return u"Parece que el usuario tiene candadito (en el culo) o hubo un error"

    def execute(self, ircMsg, userRole, *args, **kwargs):

        command = ircMsg.msg.split(' ')
        command_type = command[1]

        irc_msg = IRCMessage()
        irc_msg.channel = ircMsg.channel
        irc_msg.user = ircMsg.user
        irc_msg.directed = True

        try:

            func = self.func_dict[command_type]
            irc_msg.msg = func(command)

        except:
            irc_msg.msg = self.help(None)
            logging.error("Error processing commands")
            logging.debug(sys.exc_info()[1])
        return irc_msg
