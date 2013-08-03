 from plugins.baseactionplugin import BaseActionPlugin
from ircmessage import IRCMessage
import sqlite3
import logging
import random

class Votacion(BaseActionPlugin):

  # DB based plugins should have self.synchronous set as False.
  def __init__(self):
    BaseActionPlugin.__init__(self)
    self.synchronous = False

  def execute(self, ircMsg, userRole, *args, **kwargs):
    user = ircMsg.user
    m = IRCMessage()
    conn = kwargs["connection"]
    m.msg = unicode()
    all_rows = conn.execute("select * from users").fetchall()
    choice = random.choice(all_rows)
    m.msg = "The selected user is {0}".format(choice[0])

    m.channel = ircMsg.channel
    m.user = user
    m.directed = True
    return m
  
  def votar( conn, nick_votante, nick_votado ):
    #obtener eleccion activa
    
    #buscar nick_votado en candidatos

    #buscar voto realizado

    #realizar voto

  def postular( conn, nick, candidato, motivo ):
    #obtener eleccion activa

    #buscar si existen nick candidatos

    #buscar si candidatura ya existe

    #insertar cada candidato y registra candidatura

  def insertar_candidato( conn, id_candidato, motivo, id_votacion_eleccion ):
    #inserción de candidatura
    query = 'INSERT INTO VOTACION_CANDIDATO(id_candidato, motivo, id_votacion_eleccion) VALUES( ?, ?, ? )'    
    conn.execute( query )

    #inserción de candidatos relacionados
    query = 'INSERT INTO VOTACION_CANDIDATO_USERS( votacion_candidato_id_candidato, users_nick ) VALUES( ?, ? )'    
    conn.execute( query )
    return 'Marica postulado exitósamente'

  def buscar_user( conn, nick ):
    query = 'SELECT * FROM USERS WHERE NICK = ?'
    rows = conn.execute( query )
    if len( rows ) > 0 :
      return true
    else:
      return false

  def insertar_voto( conn, nick, votacion_candidato_id, valor, fecha ):
    query = 'INSERT INTO VOTACION_VOTO( id_voto, nick, votacion_candidato_id, valor, fecha ) VALUES ( ?, ?, ?, ?, ? )'
    conn.execute( query )
    return 'voto registrado'

  def buscar_candidato_eleccion( conn, id_eleccion ):
    query = 'SELECT * FROM VOTACION_CANDIDATO WHERE votacion_eleccion_id_eleccion = ?'
    rows = conn.execute( query )
    return rows

  def buscar_candidato_user_eleccion( conn, nick, candidatos ):
    query = 'SELECT * FROM VOTACION_CANDIDATO ' + 
    'JOIN VOTACION CANDIDATO_USERS ' +
    'ON id_candidato = votacion_candidato_id_candidato ' +
    'WHERE votacion_eleccion_id_eleccion = ? '
    rows = conn.execute( query )
    return rows

  def buscar_voto_realizado( conn, nick, id_candidato ):
    query = 'SELECT * FROM VOTACION_VOTO WHERE nick = ? AND votacion_candidato_id_candidato = ?'
    rows = conn.execute( query )
    return rows


  

    
    
