#!/usr/bin/python
# -*- coding:utf-8 -*-

import MySQLdb
import MySQLdb.cursors
from datetime import *
import time
from base_db_model import BaseDataModel
from json import *

class AcceptMissingPeopleInfo(object):
    def __init__(self, json_req):
        self.model = BaseDataModel()
        self.json_req = json_req

    def Insert(self):
        info = JSONDecoder().decode(self.json_req)
        sql = "insert into MissingPeople (userid, userphone, userloc, photocnt, missing_name, missing_age, missing_sex, missing_city, missing_date, missing_desc, photoUrl ) values (\"%s\", \"%s\", \"%s\", %d, \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\" );"
        sql = sql % (info["userid"], info["userphone"], info["userloc"], info["photocnt"], info["missing_name"], info["missing_age"], info["missing_sex"],info["missing_city"], info["missing_date"], info["missing_desc"], info["photoUrl"])

        self.model.execute( sql )
	
    


if __name__=='__main__':
    obj = AcceptMissingPeopleInfo(json_req)
