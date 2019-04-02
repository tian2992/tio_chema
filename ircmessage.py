import datetime


class IRCMessage():
  """Defines an IRC message."""

  def __init__(self, channel = "", msg = "", user = "", directed = False):
    ##TODO Convert to setters
    #if not channel.startswith("#"):
    #  self.channel = "#" + channel
    #else:
    self.t = datetime.datetime.now()
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

  def __str__(self):
    return "<IRCMessage:= channel: {0}, msg: {1}, user: {2}, directed: {3}>".format(
                          self.channel, self.msg, self.user, self.directed)

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
      usr = self.user.decode('utf-8').split("!")[0]
      return u"{0}: {1}".format(unicode(usr), unicode(self.msg))
    else:
      return unicode(self.msg)

  @property
  def tokens(self):
    return self.msg.split()

  @property
  def arguments(self):
    split_message = self.msg.split()
    return split_message[1::]
