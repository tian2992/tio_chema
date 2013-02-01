from yapsy.IPlugin import IPlugin

class IRCPlugin(IPlugin):

  def __init__(self):
    """
    Args:
      synchronous: If the plugin can be executed without blocking, syncrhonous can be set to true, to speed up execution. Please use with care.
    """
    self.synchronous = False

  def split_args(message):
    return message.msg.strip().split()

  def getTrigger(message):
    args_list = split_args(message)
    return args_list[0]
