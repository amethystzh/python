#!/usr/bin/env python
# encoding: utf-8

"""

@author:  zcb 

@license: (C) Copyright 2017-2018, JD.com

@contact: zhanchibing@jd.com

@software: IntelliJ IDEA

@file: tryJsonSchema.py

@time: 2018/8/6 15:38

@desc:

"""

import logging
import os
import jsonschema

FILE_NAME = os.path.basename(__file__)
FILENAME = os.path.splitext(FILE_NAME)[0]
LOG_NAME = FILENAME + '.log'

schema = {
    "title": "testServiceAPIrequest",
    "description": "POST request coming in test service API",
    "type": "object",
    "properties": {
        "processid": {
            "description": "The unique identifier for a process",
            "type": "integer",
            "minimum": 0
        },
        "ops_user": {
            "description": "The user's email address for this operation",
            "type": "string",
            "format": "email"
        },
        "ops_time": {
            "description": "The date/time for this operation",
            "type": "string",
            "format": "date-time"
        },
        "ops": {
            "description": "The operation",
            "type": "string",
            "enum": ["new", "goon", "fail", "pass", "skip"]
        },
        "result": {
            "description": "The result reference of test",
            "type": "string",
        },
        "note": {
            "description": "The note for the operation",
            "type": "string"
        }
    },
    "required": ["processid", "ops_user", "ops_time", "ops"]
}


def validate_json(input_json, template):
    try:
        jsonschema.validate(input_json, template)
        msg = "input json is valid"
        return 0, msg
    except jsonschema.ValidationError as ex:
        msg = "input json is invalid: (%s)" % ex
        return 1, msg


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
    
    req1 = {"processid": 3, "ops_user": "Henry", "ops_time": "2018-08-06 15:09:49", "ops": "new", "result": "http://jfactory.jd.com", "note": "Fiana"}
    req2 = {"processid": 1, "ops_user": "Jerry", "ops_time": "2018-08-06 16:49:49", "ops": "pass", "result": "http://jfactory.jd.com", "note": "test skipped"}
    req3 = {"processid": 1, "ops_user": "Jerry", "ops_time": "2018-08-03 16:49:49", "ops": "unst", "result": "http://jfactory.jd.com", "note": "regression skipped"}

    return_code, return_msg = validate_json(req1, schema)
    if return_code:
        logging.error(return_msg)
    else:
        logging.info(return_msg)

    return_code, return_msg = validate_json(req2, schema)
    if return_code:
        logging.error(return_msg)
    else:
        logging.info(return_msg)

    return_code, return_msg = validate_json(req3, schema)
    if return_code:
        logging.error(return_msg)
    else:
        logging.info(return_msg)

