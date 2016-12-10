#!/usr/bin/python
# -*- coding:utf-8 -*-

import MySQLdb
import MySQLdb.cursors
from datetime import *
import time
from base_db_model import BaseDataModel
from json import *

class GetMissingInfoByUserId(object):
    def __init__(self):
        self.model = BaseDataModel()

    def Select(self, userid):
        return self.model.select(userid);
    


if __name__=='__main__':
    obj = GetMissingPeopleList()
