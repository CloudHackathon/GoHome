#!/usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, jsonify
from flask import request, redirect, url_for
import os
from flask import make_response
#from flask.ext.cors import CORS
import time
from json import *
import json
import model.get_missing_people_list
from model.get_missing_people_list import GetMissingPeopleList
from model.get_missing_info_by_userid import GetMissingInfoByUserId
from OpenSSL import SSL
from model.accept_suspected_missing_people_info import AcceptSuspectedMissingPeopleInfo
from model.accept_missing_people_info import AcceptMissingPeopleInfo
from model.get_match_people import GetMatchPeople
import datetime
import wget
from lib.TencentYoutuyun.youtuapi import YouTuAPI

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import hashlib
app = Flask(__name__)
#CORS(app)


PhotoPath = "/home/ubuntu/GoHome/photos"



#经纬度转换
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

#后台与前段失踪人员信息的转换
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
        self.misTime = str(missInfo["missing_date"])
        oLocConvert = LocConvert()
        Longitude , Latitude = oLocConvert.DisassembleLoc(missInfo["userloc"])
        self.Longitude = Longitude
        self.Latitude = Latitude
        self.photoUrl = missInfo["photoUrl"]
        self.parentName = missInfo["userid"]
        self.parentPhone = missInfo["userphone"]
                
    

    
    






#突出失踪人员信息到前端
class PhotoDict():
    photoCnt = 0
    photoDicts = {
            
        }

    def AddDict(self, missInfoDict):
        self.photoDicts[self.photoCnt] = missInfoDict
        self.photoCnt = self.photoCnt + 1
        return True 
    def ToJson(self):
        #self.photoDicts["photoCnt"] = self.photoCnt
        return JSONEncoder().encode(self.photoDicts)        
    



@app.route('/',methods=['GET'])
def get_index0():
    return 'GoHome'



@app.route('/PullPossibleList/<usrId>',methods=['GET'])
def pullPossobleList(usrId):
    print "="*100
    m2 = hashlib.md5() 
    m2.update(usrId)
    usrId = str(m2.hexdigest())
   
    obj = GetMatchPeople()
    matchData = obj.Select(usrId)
    if matchData: 
        matchData = matchData[0]
        print "-"*100
        print matchData
        obj = LocConvert()
        print matchData["userloc"]
        if str(matchData["userloc"]):
            longi,lat = obj.DisassembleLoc(str(matchData["userloc"]))
            matchData["Latitude"]  = longi
            matchData["Longitude"] = lat
        else:
            matchData["Latitude"] = ""
            matchData["Longitude"] = ""
        print "?"*100
        print matchData
    return JSONEncoder().encode(matchData)


@app.route('/AcceptMissInfo',methods=['POST'])
def acceptMissInfo():
    
    misInfo = {}
    for item in request.form:
        item = eval(item)
        m2 = hashlib.md5()  
        m2.update(str(item["userInfo"]["nickName"]) )   
        misInfo["userid"] = str(m2.hexdigest()) 
        misInfo["userphone"] = "110"
        misInfo["missing_name"] = "mikedeng"
        misInfo["missing_age"] = "24"
        misInfo["missing_sex"] = str(item["userInfo"]["gender"])
        misInfo["missing_city"] = str(item["userInfo"]["city"])
        misInfo["missing_date"] = "20161211"
        misInfo["missing_desc"] = "GoHome"
        misInfo["userloc"] = str(item["position"]["longitude"]) + "," + str(item["position"]["latitude"])   
        misInfo["photoUrl"] = str(item["uploadFindPeopleUrl"])  
        filename = wget.download(misInfo["photoUrl"],PhotoPath)
        misInfo["local_url"] = filename 
        break; 
    ob = AcceptMissingPeopleInfo(misInfo)
    ob.Insert()
    

    youtu = YouTuAPI()
    local_pic_path = misInfo["photoUrl"]
    result = youtu.face_identify(local_pic_path) 
    print result 
    return "success"

@app.route('/AcceptInfo',methods=['POST'])
def acceptInfo():

    misInfo = {}
    for item in request.form:
        #print item
        #print type(item)
        item = eval(item)
        m2 = hashlib.md5()  
        m2.update(str(item["userInfo"]["nickName"]) )   
        misInfo["userid"] = str(m2.hexdigest()) 
        #misInfo["userid"] = str(item["userInfo"]["nickName"]) 
        misInfo["userloc"] = str(item["position"]["longitude"]) + "," + str(item["position"]["latitude"])   
        misInfo["useruploadtime"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        misInfo["photoUrl"] = str(item["uploadImageURL"])   
        filename = wget.download(misInfo["photoUrl"],PhotoPath)
        misInfo["localurl"] = filename 
        break; 
    ob = AcceptSuspectedMissingPeopleInfo(misInfo)
    ob.Insert()
        

    #youtu = YouTuAPI()
    #local_pic_path = filename
    #fields = filename.split('/')
    #remote_pic_path = fields[-1]+".jpg"
    #print local_pic_path
    #print remote_pic_path
    #print  youtu.upload_picture(local_pic_path, remote_pic_path)
    #filename = wget.download(misInfo["photoUrl"],PhotoPath)
    #print filename
    return "success"


@app.route('/GetMissingPeopleList',methods=['GET'])
def getMissingPeopleList():
    oGetMissingPeopleList = GetMissingPeopleList()
    dictTemp = oGetMissingPeopleList.Select()
    print "==-="*100
    print dictTemp
    print "==-="*100
    
    oMissingInfo = MissingInfo()
    oPhotoDict = PhotoDict()   
    for missInfo in dictTemp:
        oMissingInfo.ConverMissInfo(missInfo) 
        oPhotoDict.AddDict(oMissingInfo.ToDict())
    return oPhotoDict.ToJson()

@app.route('/GetMissingInfoByUserId/<userId>',methods=['GET'])
def getMissingInfoByUserId(userId):
    print userId 
    oGetMissingInfoByUserId = GetMissingInfoByUserId()
    m2 = hashlib.md5()  
    m2.update(userId)
    userId = m2.hexdigest()   
    dictTemp = oGetMissingInfoByUserId.Select(userId) 
    print dictTemp
    oMissingInfo = MissingInfo()
    oPhotoDict = PhotoDict()   
    for missInfo in dictTemp:
        oMissingInfo.ConverMissInfo(missInfo) 
        oPhotoDict.AddDict(oMissingInfo.ToDict())
    return oPhotoDict.ToJson()
    
@app.route('/AcceptMissingPeople',methods=['POST'])
def AcceptMissingPeople():
    return "upload OK"
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file.save("/home/ubuntu/GoHome/", filename)
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

    #print "="*100
    #print request.form
    #print "="*100
    #return "1" #'/AcceptMissingPeople'

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
    context = ('m.gohomehackathon.club.crt', 'm.gohomehackathon.club.key')
    app.run(host='10.135.155.67',port=443, debug=True, threaded=True, ssl_context=context)
