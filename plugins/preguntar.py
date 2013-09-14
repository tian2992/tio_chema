import requests
import types
import re
import json
import random
import os, sys
from plugins.baseactionplugin import BaseActionPlugin
from ircmessage import IRCMessage
from plugins.lengua import _
import logging

class Preguntar(BaseActionPlugin):
  def __init__(self):
    BaseActionPlugin.__init__(self)
    self.synchronous = False
    self.appid = 'D7KT0yvV34Fwo1YDnWKdCQibOdWcK9VzBHjut.3Y8wDrlfZKSluzcGje3wkGw3eE4CAjf65aTZs3xLd8DszXSdtFrYlyUiQ-'
    self.region = 'e1'
    self.url = 'http://answers.yahooapis.com/AnswersService/V1/questionSearch'
    self.output = 'json'

  def get_question(self, topic):
    payload = { 'query' : topic, 'appid' :  self.appid, 'region' : self.region, 'output' : self.output }
    f = requests.get(self.url, params=payload)
    # Something bad happened.
    if f.status_code != 200:
      logging.debug("HTTP error in preguntar plugin.")
      return "[http-error]"

    try:
      data = json.loads(f.text)
      preguntas = data['all']
      if len(preguntas) == 0 :
        return u"Ese termino no tiene respuesta."
      question = random.choice(preguntas['questions'])
      return u"Pregunta: {0} | Respuesta: {1} | Link {2}".format(
        question['Subject'],
        ''.join(question['ChosenAnswer'].split('\n'))[:250],
        question['Link'])
    except:
      return "Error en preguntar"

  def execute(self, ircMsg, userRole, *args, **kwargs):
      user = ircMsg.user
      m = IRCMessage()
      definiciones = []
      message = ' '.join(ircMsg.msg.split())
      topic = re.sub('^!preguntar ', '', message)

      respuesta = self.get_question(topic)

      m.msg = respuesta
      m.channel = ircMsg.channel
      m.user = user
      m.directed = True
      return m

