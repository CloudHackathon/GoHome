#!/usr/bin/python
# -*- coding:utf-8 -*-

import MySQLdb
import MySQLdb.cursors
from datetime import *
import time
from base_db_model import BaseDataModel
from json import *

class GetPoepleList(object):
    def __init__(self):
        self.model = BaseDataModel()

    def GetPeople(self, offset, count ):
        sql = "SELECT id, userid, local_url, photoUrl, userloc from MissingPeople LIMIT %d,  %d;"
        sql = sql % ( offset, count )
        print sql
        return self.model.final_execute( sql )
	

if __name__=='__main__':
    obj = GetPoepleList()
    print obj.GetPeople(0,10)
