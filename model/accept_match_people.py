#!/usr/bin/python
# -*- coding:utf-8 -*-

import MySQLdb
import MySQLdb.cursors
from datetime import *
import time
from base_db_model import BaseDataModel
from json import *

class AcceptMatchPeople(object):
    def __init__(self, info):
        self.model = BaseDataModel()
        self.info = info

    def Insert(self):
        info = self.info
        sql = "insert into DetectResult(userid, photourl, score, userloc ) values (\"%s\", \"%s\", %d, \"%s\");"
        sql = sql % (info["userid"].decode('utf8'), info["photourl"], info["score"], info["userloc"])
        print sql
        self.model.execute( sql )
	
    


if __name__=='__main__':
    obj = AcceptMatchPeople(info)
