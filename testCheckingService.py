#!/usr/bin/env python
# encoding: utf-8

# this service depends on module flask, '# pip install Flask' if needed

"""

@author:  amethystzh

@contact: amethystzh@msn.com

@software: IntelliJ IDEA

@file: testCheckingService.py

@time: 2018/7/31 11:27

@desc:

"""

import logging
import os
# import mysql.connector
from flask import Flask, request


FILE_NAME = os.path.basename(__file__)
FILENAME = os.path.splitext(FILE_NAME)[0]
LOG_NAME = FILENAME + '.log'

# mysql config
DB_CONFIG = {
    'user': 'root',
    'password': 'root123',
    'host': '172.27.37.42',
    'port': '8306',
    'database': 'qoc',
    'use_unicode': True,
}

app = Flask(__name__)

details = []


# def connect_db(db_config):
#     logging.debug('connecting to mysql...')
#     # open mysql connection
#     db = mysql.connector.connect(**db_config)
#     logging.debug('connected')
#     return db
#
#
# def query(db_config, sql):
#     # connect to db
#     db = connect_db(db_config)
#
#     cursor = db.cursor()
#     result = []
#
#     try:
#         cursor.execute(sql)
#         rsp = cursor.fetchall()
#
#         for row in rsp:
#             line = []
#             for i in range(len(row)):
#                 line.append(row[i])
#             result.append(line)
#     except mysql.connector.Error as err:
#         logging.error('unable to query data due to %s' % err)
#
#     close_db(db)
#
#     return result
#
#
# def close_db(db):
#     db.close()


@app.route('/')
def root_url():
    return '<html><h1>this root url should not be accessed</h1></html>'


@app.route('/help')
def about():
    return '<html><a href="https://cf.jd.com/pages/viewpage.action?pageId=122140533">API documents</a></html>'


@app.route('/test', methods=['GET', 'POST'])
def testCheckingService():
    # curl -s -H "Content-Type:application/json" -X POST --data
    # '{"processid":10010, "ops_user":"zhanchibing", "ops_time":"2018-07-31 15:07:15", "ops": "new",
    # "result":null, "note":"ganna"}' http://127.0.0.1:5000/test
    if request.method == 'POST':
        json_obj = request.get_json()
        logging.info(json_obj)

        processid = json_obj['processid']
        ops_user = json_obj['ops_user']
        ops_time = json_obj['ops_time']
        ops = json_obj['ops']
        result = json_obj['result']
        note = json_obj['note']

        logging.info('process_id = %s' % processid)
        logging.info('ops_user = %s' % ops_user)
        logging.info('ops_time = %s' % ops_time)
        logging.info('ops = %s' % ops)
        logging.info('result =%s' % result)
        logging.info('note =%s' % note)

        if ops == 'new':
            if details:
                logging.info('this is a duplicated NEW ops')
            else:
                detail_item = dict(processid=processid, log_id=0, ops_user=ops_user, ops_time=ops_time, ops=ops,
                                   test_result=None, test_note='launch test')
                details.append(detail_item)
                detail_item = dict(processid=processid, log_id=1, ops_user=note, ops_time=ops_time, ops='goon',
                                   test_result=None, test_note='receive test request')
                details.append(detail_item)
        else:
            if details:
                i = len(details)
                detail_item = dict(processid=processid, log_id=i, ops_user=ops_user, ops_time=ops_time, ops=ops,
                                   test_result=result, test_note=note)
                details.append(detail_item)
            else:
                logging.warn('there is no existing records yet, should be a NEW ops first')

        return 'the result of POST method: %s' % details
    # curl -s http://127.0.0.1:5000/test
    elif request.method == 'GET':
        processid = request.args.get('processid')
        if processid == 'all':
            logging.info('get processid= all, actual=%s', processid)
        elif processid:
            logging.info('get processid=%s', processid)
        else:
            logging.info('not get processid')

        if details:
            for i in range(len(details)):
                logging.info('ops_user%d = %s, ops%d = %s' % (i, details[i]['ops_user'], i, details[i]['ops']))

        return 'the result of GET method: %s' % details
    else:
        return 'the result of methods other than POST or GET'


if __name__ == '__main__':

    os_alias = os.name
    if os_alias == 'nt':
        LOG_DIR = 'D:/temp/'
    else:
        LOG_DIR = os.getcwd()

    logging.basicConfig(level=logging.DEBUG,
                        format='[%(asctime)s] %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s',
                        datefmt='%Y-%b-%d %H:%M:%S %a',
                        filename=LOG_DIR + '/' + LOG_NAME,
                        filemode='w')

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)-s: %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    app.debug = True
    app.run(host='0.0.0.0')
