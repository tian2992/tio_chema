
class IRCMessage():
  """Defines an IRC message."""

  def __init__(self, channel = "", msg = "", user = "", directed = False):
    ##TODO Convert to setters
    #if not channel.startswith("#"):
    #  self.channel = "#" + channel
    #else:
    self.channel = channel

    self.msg = msg
    self.user = user

    # Directed defines if the message should be directed to a username when rendered or not.
    self.directed = directed

  def __eq__(self, other):
    if not isinstance(other, IRCMessage):
      return False
    if other.channel != self.channel or other.msg != self.msg or \
    other.user != self.user or other.directed != self.directed:
       return False
    return True

  def is_initialized(self):
    """Checks if the message is ready to be sent"""
    if self.channel == "#" or self.msg == "":
      return False
    if self.directed and self.user == "":
      return False
    return True


  def render(self):
    """Returns a user facing representation of the message"""
    if self.directed:
      return u"{0}: {1}".format(unicode(self.user.decode('utf-8')), unicode(self.msg.decode('utf-8')))
    else:
      return self.msg