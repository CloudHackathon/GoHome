#!/usr/bin/python
# -*- coding:utf-8 -*-

import MySQLdb
import MySQLdb.cursors
import time
import config
import datetime

class BaseDataModel(object):

    _table_name = ""

    def __init__(self, table_name=""):
        self.db = MySQLdb.connect(
			host=config.HOST, 
			user=config.DB_USER, 
			passwd=config.DB_PASSWD,
			db=config.DB_NAME, 
			port=config.DB_PORT,
			cursorclass=MySQLdb.cursors.DictCursor, 
			charset='utf8'
		)
        self.cursor = self.db.cursor()
        self._table_name = table_name

    def __del__(self):
        self.close_db()

    def select(self, fields=None, map_field=None):
        if not fields:
            query_field_str = '*'
        else:
            query_field_str = ",".join(fields)
        
        sql = "select " + query_field_str + " from " + self._table_name + self.map_query(map_field)
        self.cursor.execute(sql)
        batchs = self.cursor.fetchall()
        ret_data = []
        if not batchs:
            return ret_data
        for one in batchs:
            ret_data.append(one)
        return ret_data

    def select_rand(self):
        sql = "SELECT * FROM MissingPeople ORDER BY RAND() LIMIT 10"
        self.cursor.execute(sql)
        batchs = self.cursor.fetchall()
        ret_data = []
        if not batchs:
            return ret_data
        for one in batchs:
            ret_data.append(one)
        return ret_data
    
        
        

    def execute(self, sql):
        try:
            print sql
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
            return 0
        except Exception as e:
            print e
            print "FAIL" + sql
            # Rollback in case there is any error
            self.db.rollback()
            return config.ERR_SQL_EXECUTE_FAIL

    def map_query(self, map_field):
        if not map_field:
            return ''
        else:
            query_str = " where "
            for key, value in map_field:
                query_str += str(key) + " = " + str(value) + " and "
            return query_str[:-4]

    def close_db(self):
        print 'close db'
        self.db.close()

    def show_tables(self):
        self.cursor.execute('show tables;')
        batchs = self.cursor.fetchall()
        ret_data = []
        if not batchs:
            return ret_data
        for one in batchs:
            ret_data.append(one)
        return ret_data


if __name__=='__main__':
    table_name = 'MissingPeople'
    info = BaseDataModel(table_name)
    
    list = info.select()
    print list
