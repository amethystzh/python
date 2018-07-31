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
from flask import Flask, request

FILE_NAME = os.path.basename(__file__)
FILENAME = os.path.splitext(FILE_NAME)[0]
LOG_NAME = FILENAME + '.log'

app = Flask(__name__)


@app.route('/')
def root_url():
    return 'this root url should not be accessed'


@app.route('/help')
def about():
    return 'supported API: host/test, POST and GET'


@app.route('/test', methods=['GET', 'POST'])
def testCheckingService():
    if request.method == 'POST':
        json_obj = request.get_json()
        logging.info(json_obj)
        return 'this is test input dealt: %s' % json_obj
    else:
        return 'this is test module GET return'


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
