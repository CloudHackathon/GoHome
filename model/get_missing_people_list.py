#!/usr/bin/python
# -*- coding:utf-8 -*-

import MySQLdb
import MySQLdb.cursors
from datetime import *
import time
from base_db_model import BaseDataModel
from json import *

class GetMissingPeopleList(object):
    def __init__(self):
        self.model = BaseDataModel()

    def Select(self):
        return self.model.select_rand();
    


if __name__=='__main__':
    obj = GetMissingPeopleList()
