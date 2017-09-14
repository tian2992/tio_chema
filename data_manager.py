import sqlite3
import sys
import logging

class DatabaseManager:

    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def __init__(self, db_name):
        try:
            self.db_name = db_name
            self.conn = sqlite3.connect(self.db_name, check_same_thread = False)
            self.conn.row_factory = sqlite3.Row
            # self.conn.row_factory = dict_factory
            self.conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
            self.c = self.conn.cursor()
        except:
            print "Error", sys.exc_info()

    def execute(self, query):
        return self.c.execute(query)



class Factoider():

    dbman = DatabaseManager("./db.sql3")

    def __init__(self):
        Factoider.dbman.c.execute("create table if not exists logping(user, d);")

    def put(self, key, data):
        cmd = "INSERT INTO logping(user, d) VALUES (? , ?);"
        logging.info("cmd {cmd} + {key} : {data}".format(cmd=cmd, key=key, data=data))
        try:
            with Factoider.dbman.conn:
                Factoider.dbman.conn.execute(cmd, (key, data))
        except sqlite3.IntegrityError:
            logging.error("HALP")
        #curs.execute(cmd, (name, id))
