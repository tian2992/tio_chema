# vim: ai ts=4 sts=4 et sw=4
# vim: set fileencoding=utf8
#
# Copyright (c) 2013 Fernando Larrazábal <cflm@intelnett.com>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#
import urllib
import logging
from plugins.baseactionplugin import BaseActionPlugin
from ircmessage import IRCMessage
from xml.dom import minidom
from random import randint

class diagonalpunto(BaseActionPlugin):
  """
  carga los artículos de slashdot desde su RSS
  """
  def __init__(self):
    BaseActionPlugin.__init__(self)

  def devolver_lista_de(self, url_hueco):
    diagonalpunto=minidom.parse(urllib.urlopen(url_hueco))
    historias=diagonalpunto.getElementsByTagName('item')
    articulos=[]
    for nodos in historias:
      lista=nodos.childNodes
      art=[]
      for subnodos in lista:
        art.append(subnodos.childNodes[0].nodeValue)
      articulos.append(art)
    return articulos

  def execute(self, ircMsg, userRole, *args, **kwargs):
    user = ircMsg.user
    m = IRCMessage()
    message = ' '.join(ircMsg.msg.split())
    lista_articulos = self.devolver_lista_de('http://rss.slashdot.org/Slashdot/slashdot')
    hp=randint(0,len(lista_articulos)-1)
    m.msg=''+lista_articulos[hp][2][:228] + '...... publicado el: ' + lista_articulos[hp][3] + ' en la seccion ' + lista_articulos[hp][9]
    m.channel = ircMsg.channel
    m.user = user
    m.directed = True
    return m
