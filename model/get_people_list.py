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

    def GetPeople(self, count, offset):
        sql = "SELECT local_url from MissingPeople LIMIT \"%d\",  \"%d\" );"
        sql = sql % ( offset, count )
        return self.model.execute( sql )
	

if __name__=='__main__':
    obj = GetPoepleList(json_req)
