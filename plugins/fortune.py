import subprocess
from plugins.baseactionplugin import BaseActionPlugin
from ircmessage import IRCMessage
from plugins.lengua import _


class Fortune(BaseActionPlugin):
  def __init_(self):
    BaseActionPlugin.__init__(self)
    self.synchronous = False

  def execute(self, ircMsg, userRole, *args, **kwargs):
      user = ircMsg.user
      m = IRCMessage()
      definiciones = []
      message = ' '.join(ircMsg.msg.split())
      
      p = subprocess.Popen(["fortune", "-a", "-n", "160", "-s"], stdout=subprocess.PIPE)
      output, err = p.communicate()
      #TODO manejar err
      m.msg = output
      m.channel = ircMsg.channel
      m.user = user
      m.directed = True
      return m



          

      
