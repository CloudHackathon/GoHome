#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import conf
import youtu
import ty_conf
sys.path.append('/home/ubuntu/GoHome')
from model.get_people_list import GetPoepleList

def face_identify(local_file):
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

    end_point = conf.API_YOUTU_END_POINT
    youtu_obj = youtu.YouTu(
        ty_conf.YOUTU_APP_ID,
        ty_conf.YOUTU_SECRET_ID,
        ty_conf.YOUTU_SECRET_KEY,
        ty_conf.YOUTU_USER_ID,
        end_point
    )
    group_ids = [u'gohome']

    for dict_item in result_list:
        print dict_item
        pic_id = str(dict_item['id'])
        file_path = dict_item['local_url']
        photo_url = dict_item['photoUrl']
         
        if not os.path.exists(file_path):
            print file_path + " is not exists!"
            continue
        person_id = 'missingpeople_' + str(pic_id)
        image_path = file_path
        #image_path = './js1.jpg'
        ret = youtu_obj.NewPerson(person_id, image_path, group_ids)
        print ret
        if ret['errorcode'] != 0:
            print "NewPerson fail! Local Path is %s" % file_path

    print 'group_ids:', group_ids
    ret = youtu_obj.FaceIdentify(group_ids, local_file)
    print '===== start'
    print '400:', youtu_obj.GetPersonIds([u'gohome'])
    print youtu_obj.GetGroupIds()['group_ids']
    print youtu_obj.GetGroupIds()
    print '===== end'
    return ret


if __name__ == '__main__':
    local = '/home/ubuntu/GoHome/photos/b7cefdf87ac71818267d'
    ret = face_identify(local)
    print ret
