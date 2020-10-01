"__sqlite.py: Database manipulation."
__author__ = "Muhammad Usman Naeem"
__license__ = "GPL-3"
__version__ = "1.0.0"
__maintainer__ = "Muhammad Usman Naeem"
__email__ = "usman.naeem2212@gmail.com"
__status__ = "Developed"

import sqlite3
valid_data_types = ('NULL', 'INTEGER', 'INT', 'TINYINT', 'SMALLINT', 'MEDIUMINT', 'BIGINT, UNSIGNED BIG INT', 'INT2', 'INT8' , 'TEXT', 'CHARACTER(20)', 'CHARACTER',
                      'VARCHAR(255)', 'VARCHAR', 'VARYING CHARACTER(255)', 'VARYING CHARACTER', 'NCHAR(55)', 'NCHAR', 'NATIVE CHARACTER(70)', 'NATIVE CHARACTER', 'NVARCHAR(100)',
                      'NVARCHAR', 'CLOB' , 'REAL', 'DOUBLE', 'DOUBLE PRECISION', 'FLOAT' , 'NUMERIC', 'DECIMAL', 'BOOL', 'BOOLEAN', 'BOOLEAN(10,5)' 'DATE', 'DATETIME')


class _sqlite:
    db_name = db = ""
    conn = cur = None

    @staticmethod
    def conn(config):
        '''
        Establishes Connection with class and Database
        Args:
            Cinfiguration of database
        Returns:
            class
        Raises:
            None.
        '''
        _sqlite.db_name = config['db_name']
        _sqlite.db = config
        _sqlite.conn = sqlite3.connect(_sqlite.db_name + ".sqlite")
        _sqlite.cur = _sqlite.conn.cursor()
        return _sqlite

    @staticmethod
    def create_tables():
        '''
        Creates tables in database Database
        Args:
            None
        Returns:
            None
        Raises:
            None.
        '''
        tabl = _sqlite.db['tables']
        for tab in tabl:
            k = list(tabl[tab]['fields'].keys())
            v = list(tabl[tab]['fields'].values())

            sql = "CREATE TABLE IF NOT EXISTS " + tabl[tab]['name'] + "  ("

            sql += "id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,"

            for i in range(len(k)):
                if v[i].upper() not in valid_data_types:
                    print(v[i].upper(), "is not a valid Data Type of table:", tabl[tab]['name'])
                    continue
                sql += "'" + k[i] + "' " + v[i] + ","

            sql = sql[0: len(sql) - 1]
            sql += ");"

            _sqlite.cur.executescript(sql)
            print(tabl[tab]['name'], "Table Created.")

    @staticmethod
    def getCur():
        '''
        Establishes Connection with class and returns cursor
        Args:
            None
        Returns:
            class cursor
        Raises:
            None.
        '''
        return _sqlite.cur

    @staticmethod
    def insert_one(table, file) :
        '''
        Inserts one element in table of Database
        Args:
            table: Name of Table
            file: file name to be inserted
        Returns:
            None
        Raises:
            None.
        '''
        sql = "INSERT INTO " + table + " (date) VALUES ('" + file + "')"
        try:
            _sqlite.cur.execute(sql)
        except:
            print("Error")
        _sqlite.conn.commit()

    @staticmethod
    def insert(table, data):
        '''
        Inserts data in table of Database
        Args:
            table: Name of Table
            data: dictionary of file names to be inserted
        Returns:
            Bool: True/False
        Raises:
            None.
        '''
        fields = tuple(data.keys())
        values = tuple(data.values())
        if len(fields) != len(values):
           return False
        if len(values) > 1:
            vals = str(tuple("?") * len(values)).replace("'", "")
        else:
            vals = str(tuple("?") * len(values))[0: len(values) - 3].replace("'", "") + ")"
        sql = "INSERT INTO " + table + " " + str(fields)[0:len(str(fields))-2].replace("'", "") + ")"
        sql += " VALUES " + vals + ";"
        try:
            _sqlite.cur.execute(sql, values)
        except:
            print("Error")
        _sqlite.conn.commit()
        return True

    @staticmethod
    def get_last(table, where=None):
        '''
        Gets the last element from table of Database
        Args:
            table: Name of Table
            where: field name to look at
        Returns:
            last Element found in Table
        Raises:
            None.
        '''
        sql = "SELECT * FROM " + table
        if where is not None:
            sql += " WHERE " + where['field'] + " = " + where['value']
        sql += " ORDER BY id DESC LIMIT 1 ;"
        try:
            _sqlite.cur.execute(sql, ())
            return _sqlite.cur
        except:
            return False

    @staticmethod
    def get(table, where=None):
        '''
        gets elements from table of Database
        Args:
            table: Name of Table
            where: field name to look at
        Returns:
            List to elements parsed
        Raises:
            None.
        '''
        sql = "SELECT * FROM " + table
        if where is not None:
            sql += " WHERE " + where['field'] + " = " + where['value']
        sql += ";"
        try:
            _sqlite.cur.execute(sql, ())
            return _sqlite.cur
        except:
            return False

    @staticmethod
    def delete(table, field, value):
        '''
        Deletes elements from table of Database
        Args:
            table: Name of Table
            field: field name to look at in table
            value: value to be deleted
        Returns:
            Bool: True/False
        Raises:
            None.
        '''
        sql = "DELETE FROM " + table + " WHERE " + field + " = ? ;"
        try:
            _sqlite.cur.execute(sql, (value,))
            return True
        except:
            return False
