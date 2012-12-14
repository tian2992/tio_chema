class IrcMessage():
  """Defines an IRC message."""
  
  def __init__(self, channel=None, msg=None, user=None):
    if channel is None:
      self.channel = ""
    else:
      self.channel = channel
    if msg is None:
      self.msg = ""
    else:
      self.msg = msg
    if user is None:
      self.user = ""
    else:
      self.user = user
            