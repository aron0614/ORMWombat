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

    def _genInsertValue(self):
        if self.fieldType == "Text":
            if self.lenght != None:
                fieldType = f"VARCHAR({self.lenght})"
            else:
                fieldType = "TEXT"
            genSql = f"'{self.name}' {fieldType} NOT NULL"
        
        return genSql

class TextField(Field):
    fieldType = "Text"
    
class Table:
    name : str
    fields : list[Field]
    
    def __init__(self, name : str, fields : list[Field] = None) -> None:
        self.name = name
        self.fields = []
        if fields != None:
            for f in fields:
                if not self.addField(f):
                    raise Exception("Can't Add A Field That Already Exists In Table: ", f.name)
    
    def addField(self, field : Field):
        if self.fieldInTable(field):
            return False
        
        self.fields.append(field)
        return True
    
    def fieldInTable(self, field : Field):
        match = False
        for f in self.fields:
            if f.name == field.name:
                match = True
                break
        
        return match

class Automation:
    pass

class Migration:
    pass

class DatabaseHandler:
    #connection vars
    host : str
    port : int
    user : str
    passwd : str
    database : str
    
    def __init__(self, host : str, user : str, passwd : str, database : str, port : int = None) -> None:
        self.host = host
        self.user = user
        self.passwd = passwd
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
    
    def setupNewDB(self):
        sql = "CREATE TABLE `WombatORM_Tables` (`TableName` TEXT NOT NULL , `Structure` TEXT NOT NULL , PRIMARY KEY (`TableName`)) ENGINE = InnoDB;"
        self.execute(sql)
        
class Wombat:
    """The main handler of WombatORM"""
    #ORM stuff
    tables : list[Table]
    
    def __init__(self, host : str, user : str, passwd : str, database : str, port : int = None) -> None:
        pass

    def checkTableExists(self, table : str):
        match = False
        for t in self.tables:
            if t.name == table.name:
                match = True
                break
        
        return match
    
    def on_setup(self):
        pass