#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import sys
import requests
import json
import traceback
import time
import ty_conf
import conf
from qcloud_cos import UploadFileRequest, CosClient, Auth

import sys
sys.path.append('/home/ubuntu/GoHome')
from model.get_people_list import GetPoepleList
from model.accept_match_people import AcceptMatchPeople


class YouTuAPI(object):

    host = 'service.image.myqcloud.com'

    def __init__(self):
        self.app_id = ty_conf.APP_ID
        self.secret_id = ty_conf.SECRET_ID
        self.secret_key = ty_conf.SECRET_KEY
        self.region = ty_conf.REGION
        self.bucket = unicode(ty_conf.BUCKET)
        self.cos_client = CosClient(
            int(self.app_id),
            self.secret_id, 
            self.secret_key, 
            self.region
        )
        self.auth = Auth(self.cos_client.get_cred())

    def _assemble_url(self, path):
        return 'http://%s%s' % (self.host, path)

    def _get_sign(self):
        return self.auth.sign_more(self.bucket, '', int(time.time()+30))

    def upload_picture(self, local, remote):
        print 'local:',local
        request = UploadFileRequest(self.bucket, unicode(remote), unicode(local), insert_only=0)
        result = self.cos_client.upload_file(request)
        data = result.get('data', None)
        if data:
            return data.get('source_url', None)
        else:
            return None

    def face_identify(self, cur_url):
        team_once = 10
        offset = 0
        result_list = []
        person_info = {}
        obj = GetPoepleList()
        tmp_list = obj.GetPeople(offset, team_once)
        result_list = result_list + tmp_list
        while tmp_list:
            offset += team_once
            tmp_list = obj.GetPeople(team_once, offset)
            result_list += tmp_list

        self.face_detect(cur_url)

        max_value = 0.0
        max_info = {}
        for dict_item in result_list:
            pic_id = str(dict_item['userid'])
            file_path = dict_item['local_url']
            photo_url = dict_item['photoUrl']

            self.face_detect(photo_url)
            score = self.face_compare(cur_url, photo_url)
            if score > max_value:
                max_value = score
                max_info['userid'] = str(dict_item['userid'])
                max_info['local_url'] = dict_item['local_url']
                max_info['photourl'] = dict_item['photoUrl']
                max_info['score'] = int(max_value)
                max_info['userloc'] = str(dict_item['userloc'])

        accept_match_people_obj = AcceptMatchPeople(max_info)
        accept_match_people_obj.Insert()
        return max_info


    def face_detect(self, picture_url):
        url = self._assemble_url('/face/detect')
        sign = self._get_sign()
        headers = {
            'Host': 'service.image.myqcloud.com',
            'Content-Type': 'application/json',
            'Authorization': sign
        }
        data = {
            "appid": str(self.cos_client.get_cred().get_appid()),
            "bucket": self.bucket,
            "mode": 1,
            "url": picture_url
        }
        response = requests.post(url, data=json.dumps(data), headers=headers)
        response_data = json.loads(response.text)
        if response_data.get('code', None) == 0:
            data = response_data.get('data')
            face = data.get('face')[0]
            age = face.get('age')
            gender = face.get('gender')
            sex = 0 if gender < 50 else 1
            return {'sex': sex, 'age': age}
        else:
            print data
            return None

    def face_compare(self, picture_url, another_picture_url):
        url = self._assemble_url('/face/compare')
        sign = self._get_sign()
        headers = {
            'Host': 'service.image.myqcloud.com',
            'Content-Type': 'application/json',
            'Authorization': sign
        }
        data = {
            "appid": str(self.cos_client.get_cred().get_appid()),
            "bucket": self.bucket,
            "urlA": picture_url,
            "urlB": another_picture_url,
        }
        response = requests.post(url, data=json.dumps(data), headers=headers)
        response_data = json.loads(response.text)
        score = response_data['data']['similarity']
        print 'score:', score
        if score > ty_conf.FACE_COMPARE_THRESHOLD:
            return score
        return 0.0


if __name__ == '__main__':
    youtu = YouTuAPI()
    local_pic_path = 'http://ac-jmvij1bt.clouddn.com/fdf5f4750925581d0edb'
    result = youtu.face_identify(local_pic_path)
    print '============='
    print result
    print '============='
    #remote_pic_path = '/temp/js6.jpg'
    #js1_url = youtu.upload_picture(local_pic_path, remote_pic_path)
    #print js1_url

    #j1url = 'http://ac-jmvij1bt.clouddn.com/ca8d8e94ebdde412d3b8'
    #j2url = 'http://ac-jmvij1bt.clouddn.com/ca8d8e94ebdde412d3b8'
    #j3url = 'http://ac-jmvij1bt.clouddn.com/ca8d8e94ebdde412d3b8'
    #youtu.face_detect(j1url)
    #youtu.face_detect(j2url)
    #youtu.face_detect(j3url)

    #print youtu.face_compare(j1url, j2url)

"""youtu = YouTu(APP_ID, SECRET_ID, SECRET_KEY, REGION, 'hackthon')
js1_url = youtu.upload_picture('/Users/sean/Documents/js1.jpeg', '/temp/js1.jpeg')
js2_url = youtu.upload_picture('/Users/sean/Documents/js2.jpeg', '/temp/js2.jpeg')
tank_url = youtu.upload_picture('/Users/sean/Documents/tank.jpeg', '/temp/tank.jpeg')
youtu.face_detect(tank_url)
youtu.face_detect(js1_url)
youtu.face_detect(js2_url)
print youtu.face_compare(js1_url, js2_url)
print youtu.face_compare(js1_url, tank_url)"""
