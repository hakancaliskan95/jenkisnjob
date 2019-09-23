import sqlite3


class Database:

    def __init__(self,dbName):
        self.database = sqlite3.connect(dbName)

    def createTable(self, name, columns = {}):
        cols = ''
        for key, value in columns.items():
            cols += key + ' ' + value + ', '
        cols = cols[:-2]
        sql = "CREATE TABLE %s (%s)" % (name, cols)
        return self.execute(sql)

    def query(self, *args, **kwargs):
        cursor = self.database.execute(*args, **kwargs)
        return cursor

    def execute(self, *args, **kwargs):
        self.database.execute(*args, **kwargs)
        self.database.commit()

    def close(self):
        self.database.close()