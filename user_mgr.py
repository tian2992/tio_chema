from user import user

class user_mgr:

    def __init__(self, dbmgr):
        self.dbmgr = dbmgr

    def get_user(self, nick ):
        query = 'SELECT * FROM users WHERE nick like \'{0}\''.format(nick)
        print query
        cur = self.dbmgr.execute(query)
        
        row = cur.fetchone()

        userg = user('','','','2012-01-01','',0,'',0)

        if row is not None :
            userg = user(row["nick"], row["seen"], row["command"], 
                             row["last"], row["perm"], row["karma"], 
                             row["pass"], row["pipianlvl"])

        return userg
        


