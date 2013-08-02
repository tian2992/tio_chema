import requests
import types
import re
import json
import random
from plugins.baseactionplugin import BaseActionPlugin
from ircmessage import IRCMessage
from plugins.lengua import _

class Preguntar(BaseActionPlugin):
  def __init_(self):
    BaseActionPlugin.__init__(self)
    self.synchronous = False
    self.appid = 'D7KT0yvV34Fwo1YDnWKdCQibOdWcK9VzBHjut.3Y8wDrlfZKSluzcGje3wkGw3eE4CAjf65aTZs3xLd8DszXSdtFrYlyUiQ-'
    self.region = 'e1'
    self.url = 'http://answers.yahooapis.com/AnswersService/V1/questionSearch'
    self.output = 'json'

  def get_question( self, topic ):
    self.appid = 'D7KT0yvV34Fwo1YDnWKdCQibOdWcK9VzBHjut.3Y8wDrlfZKSluzcGje3wkGw3eE4CAjf65aTZs3xLd8DszXSdtFrYlyUiQ-'
    self.region = 'e1'
    self.url = 'http://answers.yahooapis.com/AnswersService/V1/questionSearch'
    self.output = 'json'
    payload = { 'query' : topic, 'appid' :  self.appid, 'region' : self.region, 'output' : self.output }
    f = requests.get( self.url, params=payload )
    data = json.loads(f.text)
    preguntas = data['all']
    if len( preguntas ) == 0 :
      return 'Ese termino cerote no tiene respuesta'.encode( 'utf8' )

    question = random.choice( preguntas['questions'] )

    return u'Pregunta: ' + question['Subject'] + ' | Respuesta ' + question['ChosenAnswer'][:250] + ' | Link: ' + question['Link']

  def execute(self, ircMsg, userRole, *args, **kwargs):
      user = ircMsg.user
      m = IRCMessage()
      definiciones = []
      message = ' '.join(ircMsg.msg.split())
      topic = re.sub('^!preguntar ', '', message)

      respuesta = self.get_question( topic  )

      m.msg = respuesta
      m.channel = ircMsg.channel
      m.user = user
      m.directed = True
      return m

