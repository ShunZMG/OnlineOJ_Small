# -*- coding:UTF-8 -*-
import pymysql
from test import Test


class DBManager(Test):
    def __init__(self, dbname, dbpsd, host, user):
        Test.__init__(self)
        self.__dbName = dbname
        self.__dbPsd = dbpsd
        self.__dbHost = host
        self.__dbUser = user
        self.__dbHandle = None
        self.__dbCursor = None
        self.__dbTable = None
        self.m_connect()

    def m_useTable(self, tablename):
        self.__dbTable = tablename

    def m_connect(self):
        if not self.__dbHandle:
            self.__dbHandle = pymysql.connect(self.__dbHost, self.__dbUser, self.__dbPsd, self.__dbName, charset='utf8')
            self.__dbCursor = self.__dbHandle.cursor()

    def m_createTable(self, tablename, li_dbitem, primarykey):
        create_command = 'CREATE TABLE IF NOT EXISTS %s (' % tablename
        for item in li_dbitem:
            name = item[0]
            type = item[1]
            create_command += '%s %s ' % (name, type)
            if primarykey == name:
                create_command += 'PRIMARY KEY'
            create_command += ','
        create_command = create_command[:len(create_command)-1]
        create_command += ');'

        self.log(create_command)

    def execute(self, command):
        global flag
        flag = False
        if not self.__dbCursor:
            self.m_connect()
            flag = True
        self.__dbCursor.execute(command)
        self.__dbHandle.commit()
        if flag:
            self.m_close()
        return self.__dbCursor.fetchall()

    def m_selectItem(self, li_name="*", where=""):
        command = 'SELECT '
        for name in li_name:
            command += name + ","
        command = command[:len(command)-1]
        command += ' FROM %s ' % self.__dbTable
        if not where == "":
            command += 'WHERE %s' % where
        command += ';'
        self.log(command)
        return self.execute(command)

    def m_insertItem(self, li_value):
        command = 'INSERT INTO %s VALUES(' % self.__dbTable
        for value in li_value:
            if type(value) == str:
                value = r'"%s"' % value
                #print('value:', value)
            command += '%s ,' % value
        command = command[:len(command)-1] + ');'
        self.log(command)
        self.execute(command)

    def m_itemExists(self, li_value, where):
        rst = self.m_selectItem(li_value, where)
        if not rst:
            return False
        return True

    def m_deleteItem(self, where=""):
        command = "DELETE FROM %s" % self.__dbTable
        if not where == "":
            command += " WHERE %s" % where
        command += ';'
        self.log(command)
        self.execute(command)

    def m_updateItem(self, name, value, where=""):
        command = "UPDATE %s SET %s=%s" % (self.__dbTable, name, value)
        if not where == "":
            command += " WHERE %s" % where
        command += ';'
        self.log(command)
        self.execute(command)

    def m_close(self):
        if self.__dbHandle:
            self.__dbHandle.close()
        self.__dbHandle = None
        self.__dbCursor = None


if __name__ == '__main__':
    print("这个模块是给数据库读写，创建设计的")