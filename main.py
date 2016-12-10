#!/usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, jsonify
from flask import make_response
#from model.dataAccess import DataInfo
#from flask.ext.cors import CORS
import time
from json import *
import json
import model.get_missing_people_list
from model.get_missing_people_list import GetMissingPeopleList
app = Flask(__name__)
from OpenSSL import SSL
#CORS(app)


class LocConvert():
    Latitude = ""
    Longitude = ""

    strLoc = ""

    def AssembleLoc(self,Longitude,Latitude): 
        return Longitude + "," + Latitude        

    def DisassembleLoc(self,strLoc):
        locList = strLoc.split(',',1)
        Longitude = locList[0]
        Latitude = locList[1]
        return Longitude , Latitude


class MissingInfo():
    name = ""
    age = ""
    sex = ""
    birth = ""
    losCity = ""
    misTime = ""
    photoUrl = ""
    parentName = ""
    parentPhone = ""
    Latitude = ""
    Longitude = ""
    
    def ToDict(self):
        missingDict = {
            "name":self.name,
            "age":self.age,
            "sex":self.sex,
            "birth":self.birth,
            "losCity":self.losCity,
            "misTime":self.misTime,
            "Latitude":self.Latitude,
            "Longitude":self.Longitude,
            "photoUrl":self.photoUrl,
            "parentName":self.parentName,
            "parentPhon":self.parentPhone
        }
        return missingDict
        
    def ConverMissInfo(self,missInfo):
        self.name = missInfo["missing_name"]
        self.age = missInfo["missing_age"]
        self.sex = missInfo["missing_sex"]
        self.losCity = missInfo["missing_city"]
        self.misTime = missInfo["missing_date"]
        oLocConvert = LocConvert()
        Longitude , Latitude = oLocConvert.DisassembleLoc(missInfo["userLoc"])
        self.Longitude = Longitude
        self.Latitude = Latitude
        self.photoUrl = missInfo["photoUrl"]
        self.parentName = missInfo["userid"]
        self.parentPhone = missInfo["userphone"]
                
    



class PhotoDict():
    photoCnt = 0
    photoDicts = {
            "photoCnt":0,
        }

    def AddDict(self, missInfoDict):
        self.photoDicts[self.photoCnt] = missInfoDict
        self.photoCnt = self.photoCnt + 1
        return True 
    def ToJson(self):
        self.photoDicts["photoCnt"] = self.photoCnt
        return JSONEncoder().encode(self.photoDicts)        
    


@app.route('/',methods=['GET'])
def get_index0():
    return 'GoHome'

@app.route('/GetMissingPeopleList',methods=['GET'])
def getMissingPeopleList():
    oGetMissingPeopleList = GetMissingPeopleList()
    dictTemp = oGetMissingPeopleList.Select()
    print dictTemp
    oMissingInfo = MissingInfo()
    oPhotoDict = PhotoDict()   
    for missInfo in dictTemp:
        oMissingInfo.ConverMissInfo(missInfo) 
        oPhotoDict.AddDict(oMissingInfo.ToDict())

    #oMissingInfo = MissingInfo()
    #oMissingInfo.name = "tom"
    #oPhotoDict = PhotoDict()   
    #oPhotoDict.AddDict(oMissingInfo.ToDict())
    #oPhotoDict.AddDict(oMissingInfo.ToDict())    
    return oPhotoDict.ToJson()

@app.route('/GetPulicMissingInfoByUserId/<userId>',methods=['GET'])
def getPulicMissingInfoByUserId(userId):
    
    oMissingInfo = MissingInfo()
    oMissingInfo.name = "tom"
    oPhotoDict = PhotoDict()   
    oPhotoDict.AddDict(oMissingInfo.ToDict())
    return oPhotoDict.ToJson() 
    
@app.route('/AcceptMissingPeople',methods=['POST'])
def AcceptMissingPeople():
    print request
    return '/AcceptMissingPeople'

@app.route('/AcceptSuspectedMissingPeopleInfo',methods=['POST'])
def get_index2():
    return '/AcceptSuspectedMissingPeopleInfo'

@app.route('/GetMissingPeopleInfo',methods=['POST'])
def get_index3():
    return '/GetMissingPeopleInfo'
	
@app.route('/PushMissingPeopleInfo',methods=['POST'])
def get_index4():
    return '/PushMissingPeopleInfo'

@app.route('/Admin',methods=['GET'])
def get_index5():
    return 'Hello World'

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    context = ('m.gohometencent-hackathon.club.crt', 'm.gohometencent-hackathon.club.key')
    app.run(host='10.135.155.67',port=443, debug=True, threaded=True, ssl_context=context)
