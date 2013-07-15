import sqlite3
import sys

class DatabaseManager:

    def __init__(self, db_name):
        try:
            self.db_name = db_name
            self.conn = sqlite3.connect(self.db_name, check_same_thread = False)
            self.conn.row_factory = sqlite3.Row
            self.c = self.conn.cursor()
        except:
            print "Error", sys.exc_info()

    def execute(self, query):
        return self.c.execute(query)




