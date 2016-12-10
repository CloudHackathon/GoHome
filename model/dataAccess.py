#!/usr/bin/python
# -*- coding:utf-8 -*-

import MySQLdb
import MySQLdb.cursors
from datetime import *
import time

class DataInfo(object):
    def __init__(self):
        self.db = MySQLdb.connect("10.135.155.67", "root", "Gohome2016", "gohome", port=3306, 
        cursorclass=MySQLdb.cursors.DictCursor, charset='utf8')
        self.cursor = self.db.cursor()

    def close_mysql(self):
        self.db.close()

    def get_emoji_batch(self):
        self.cursor.execute('select * from t_search_emoji_batch')
        batchs = self.cursor.fetchall()
        ret_data = []
        if not batchs:
            return ret_data
        for one in batchs:
            ret_data.append(one)
        return ret_data


if __name__=='__main__':
    info = DataInfo()
    list = info.get_emoji_batch()
    print list
    info.close_mysql()
