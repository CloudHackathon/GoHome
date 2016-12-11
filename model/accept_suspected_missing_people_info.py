#!/usr/bin/python
# -*- coding:utf-8 -*-

import MySQLdb
import MySQLdb.cursors
from datetime import *
import time
from base_db_model import BaseDataModel
from json import *

class AcceptSuspectedMissingPeopleInfo(object):
    def __init__(self, info):
        self.model = BaseDataModel()
        #self.json_req = json_req
        self.info = info

    def Insert(self):
        #info = JSONDecoder().decode(self.json_req)
        info = self.info
        sql = "insert into SuspectMissingPeople (userid, userloc, useruploadtime, photoUrl, localurl ) values (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\" );"
        sql = sql % ( info["userid"], info["userloc"], info["useruploadtime"], info["photoUrl"], info["localurl"] )
        print "-="*5    
        print sql
        self.model.execute( sql )
	
    


if __name__=='__main__':
    obj = AcceptMissingPeopleInfo(json_req)
