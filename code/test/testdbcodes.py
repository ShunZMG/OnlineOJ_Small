from dbcodes import DBManager

if __name__ == '__main__':
    manager = DBManager('testDB', 'ComPro32API', 'localhost', 'root')
    manager.logOn()
    manager.m_createTable('testnewtable', [['li1', 'CHAR(20)'],
                                           ['li2', 'INT']], 'li1')
    manager.m_useTable('testTable')
    print(manager.m_selectItem(['key1']))
    manager.m_insertItem(['value4', 987])
    print(manager.m_selectItem())
    print(manager.m_itemExists(['key1', 'key2'], 'key1="zhazha" AND key2=321'))
    manager.m_close()
