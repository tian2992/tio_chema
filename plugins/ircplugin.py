from yapsy.IPlugin import IPlugin

class IRCPlugin(IPlugin):

  def execute(self, ircMsg, userRole):
    raise NotImplementedError

  def split_args(message):
    return message.msg.strip().split(' ')

  def getTrigger(message):
    args_list = split_args(message)
    return args_list[0]
