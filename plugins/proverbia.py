# coding=utf-8
import requests
from bs4 import BeautifulSoup
import random

from plugins.baseactionplugin import BaseActionPlugin
from ircmessage import IRCMessage
import logging

class ProverbiaPlugin(BaseActionPlugin):

  # This constructor is optional
  def __init__(self):
    BaseActionPlugin.__init__(self)
    self.synchronous = True

  def execute(self, ircMsg, userRole, *args, **kwargs):
    m = IRCMessage()
    # Genera URL de letras
    letrarandom = lambda : 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[random.randint(0,25)]
    # Parsea html de una URL
    sopa = lambda url: BeautifulSoup(requests.get(url).content, 'html.parser')# , from_encoding="utf-8")
    # URL random para encontrar autores
    urlautoresrandom = "http://www.proverbia.net/citasautores.asp?letra="+letrarandom()
    # Sopa de autores
    sopa_de_autores = sopa(urlautoresrandom)
    # Hacer la link al autor
    links_de_autores = sopa_de_autores.find(id='citasautores').find_all('a')
    hrefs_de_autores = map(lambda l: l.get('href'), links_de_autores)
    link_a_autor = "http://www.proverbia.net/"+hrefs_de_autores[random.randint(0,len(hrefs_de_autores)-1)]

    logging.debug("Link a autor: {0}".format(link_a_autor))

    # Cuentas mas de una pagina el autor? Formar la URL
    numero_de_paginas = len(sopa(link_a_autor).find(id="paginas").find_all("a"))
    link_a_pagina = link_a_autor

    if numero_de_paginas > 1:
        npage_random = random.randint(1,numero_de_paginas)

        ## Encontrar pagina
        link_a_pagina = link_a_autor + "&page=" + unicode(npage_random)
        logging.debug("Link a pagina: %s" % link_a_pagina)

    # Con la URL de la pagina, formarla
    sopa_de_citas = sopa(link_a_pagina)
    citas = sopa_de_citas.find_all('blockquote')
    cita = citas[random.randint(0,len(citas)-1)].text.strip()
    autor = sopa_de_citas.find('h1').text.strip()
    profesion = sopa_de_citas.find(id='bio').text.strip()
    texto = u"« {cita} » - {autor} : {profesion}".format(cita=cita, autor=autor, profesion=profesion)
    m.channel = ircMsg.channel
    m.user = ircMsg.user
    m.directed = True
    logging.debug(u"Proverbia: {0}".format(texto))
    m.msg = texto
    return m
