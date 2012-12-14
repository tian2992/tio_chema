
class IRCMessage():
  """Defines an IRC message."""
  
  def __init__(self, channel, msg, user=None):
    if not channel.startswith("#"):
      self.channel = "#" + channel
    else:
      self.channel = channel
    
    self.msg = msg
    self.user = user
    
    # Directed defines if the message should be directed to a username when renderedor not.
    self.directed = False