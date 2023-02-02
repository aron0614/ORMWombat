import pymysql
import pymysql.cursors

class Field:
    name : str
    fieldType : str
    lenght : int
    
    _isLenghtAble : bool = True
    
    def __init__(self, name : str, lenght : int = None) -> None:
        self.name = name
        self.lenght = lenght

    def _genInsert(self):
        pass
    
class Table:
    pass

class Automation:
    pass


class Wombat:
    """The main handler of WombatORM"""
    
    #connection vars
    host : str
    port : int
    user : str
    passwd : str
    database : str
    
    def __init__(self, host : str, user : str, passwd : str, database : str, port : int = None) -> None:
        self.host = host
        self.user = user
        self. passwd = passwd
        self.database = database
        
        if port:
            self.port = port
        
    def connect(self):
        return pymysql.connect(host=self.host, user=self.user, password=self.passwd, db=self.database, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    
    def execute(self, sql, params=None):
        connection = self.connect()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
            connection.commit()
        finally:
            connection.close()
    
    def fetch(self, sql, params=None):
        connection = self.connect()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
                result = cursor.fetchall()
        finally:
            connection.close()
        return result

    def checkTableExists(self, tableName):
        sql = "SHOW TABLES LIKE %s;"
        res = self.fetch(sql, (str(tableName)))
        if type(res) == tuple or type(res) == list:
            return True
        else:
            return False
    
