import subprocess
from plugins.baseactionplugin import BaseActionPlugin
from ircmessage import IRCMessage
from plugins.lengua import _
from random import randint

class Calendar(BaseActionPlugin):
  def __init_(self):
    BaseActionPlugin.__init__(self)
    self.synchronous = False

  def execute(self, ircMsg, userRole, *args, **kwargs):
      user = ircMsg.user
      m = IRCMessage()
      definiciones = []
      message = ' '.join(ircMsg.msg.split())
      
      cal = subprocess.Popen( [ 'calendar' ], stdout=subprocess.PIPE )
      wc = subprocess.Popen( [ 'wc', '-l' ], stdin=cal.stdout, stdout=subprocess.PIPE )
      num = wc.communicate()
      numero = int( num[0] )
      numero = randint( 0, numero )
      cal = subprocess.Popen( [ 'calendar'], stdout=subprocess.PIPE )
      head = subprocess.Popen( [ 'head', '-' + str( numero ) ], stdin=cal.stdout, stdout=subprocess.PIPE )
      tail = subprocess.Popen( [ 'tail', '-1' ], stdin=head.stdout, stdout=subprocess.PIPE )
      resp = tail.communicate();
      if len( resp ) > 0 :
        respuesta = resp[ 0 ]
      else:
        respuesta = ''
      #calendar | wc -l ; calendar | head -rand | tail -1
      m.msg = '' + respuesta
      m.channel = ircMsg.channel
      m.user = user
      m.directed = True
      return m



          

      
