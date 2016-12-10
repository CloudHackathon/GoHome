#!/usr/bin/python
# -*- coding:utf-8 -*-

import MySQLdb
import MySQLdb.cursors
from datetime import *
import time
from base_db_model import BaseDataModel
from json import *

class AcceptMissingPeopleInfo(object):
    def __init__(self, info):
        self.model = BaseDataModel()
        #self.json_req = json_req
        self.info = info

    def Insert(self):
        #info = JSONDecoder().decode(self.json_req)
        info = self.info
        sql = "insert into MissingPeople (userid, userphone, userloc, missing_name, missing_age, missing_sex, missing_city, missing_date, missing_desc, photoUrl ) values (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\" );"
        sql = sql % (info["userid"], info["userphone"], info["userloc"], info["missing_name"], info["missing_age"], info["missing_sex"],info["missing_city"], info["missing_date"], info["missing_desc"], info["photoUrl"])

        self.model.execute( sql )
	
    


if __name__=='__main__':
    obj = AcceptMissingPeopleInfo(json_req)
