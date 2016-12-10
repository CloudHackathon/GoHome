#!/usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, jsonify
from flask import make_response
from dataAccess import DataInfo
#from flask.ext.cors import CORS
import time

app = Flask(__name__)
#CORS(app)

@app.route('/bosstest/flaskcgi/testCGI', methods=['GET'])
def get_tasks():
    return 'start ' + str(time.time())

@app.route('/bosstest/flaskcgi/batch', methods=['GET'])
def get_batchs():
    data = DataInfo()
    batchs = data.get_emoji_batch()
    result = jsonify({'batchs': batchs})
    return result

@app.route('/',methods=['GET'])
def get_index():
    return 'GoHome'

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(host='10.135.155.67',port=5000, debug=True, threaded=True)
