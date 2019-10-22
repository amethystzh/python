#!/usr/bin/env python
# encoding: utf-8

"""!
@file:
@author: zcb
@time: 2019/6/5 15:20
@desc: this contains the python implement of S3 compatible API, for doxygen usage comments
"""

import logging
import os
import socket
import mysql.connector
import boto3

FILE_NAME = os.path.basename(__file__)
FILENAME = os.path.splitext(FILE_NAME)[0]
LOG_NAME = FILENAME + '.log'
log_dir = os.getcwd() + '/log'

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s',
                    datefmt='%Y-%b-%d %H:%M:%S %a',
                    filename=log_dir + '/' + LOG_NAME,
                    filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)-s: %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


class S3API:
    """!
    this is the API implement class.
    this class contains methods of common usage
    @author AmethystZh
    @date 2019-10-22
    @version 1.1
    """
    # env config
    DEV_ENV = ('10.0.0.*', '10.1.0.*', '10.2.1.*', '10.3.4.5')  # PC, laptop, dev-vm
    TEST_ENV = ('192.168.1.1', '172.168.1.1')  # HuangCun jenkins, HuaDong jenkins
    ONLINE_ENV = ('10.166.166.166', '10.88.88.88')  # online jenkins, online API server

    # mysql config
    DEV_DB = {
        'user': 'root',
        'password': 'root',
        'host': '10.0.0.15',
        'port': '3306',
        'database': 'test',
        'use_unicode': True,
    }

    # DEV_DB = {
    #     'user': 'root',
    #     'password': 'root',
    #     'host': '10.2.1.4',
    #     'port': '3306',
    #     'database': 'test',
    #     'use_unicode': True,
    # }

    TEST_DB = {
        'user': 'root',
        'password': 'root',
        'host': '172.168.1.3',
        'port': '8306',
        'database': 'test',
        'use_unicode': True,
    }

    ONLINE_DB = {
        'user': 'root',
        'password': 'root',
        'host': '10.88.88.88',
        'port': '3306',
        'database': 'test',
        'use_unicode': True,
    }

    db_config = None
    db_connection = None

    def __init__(self):
        """!
        this is the initial of class object.
        """
        host_ip = self.get_host_ip()
        logging.debug('local ip is: %s', host_ip)
        self.db_config = self.get_env(host_ip)
        logging.debug('use db as: %s', self.db_config['host'])

    @staticmethod
    def get_host_ip():
        """!
        retrieve local host ip address.
        """
        s = socket.socket()
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip

    @staticmethod
    def get_env(host_ip):
        """!
        assign env var according to local ip.
        @param host_ip the ip address of host
        @return the corresponding db environment configure can be used in dev/test
        """
        local_host_ip = host_ip
        logging.debug('host ip is: %s', local_host_ip)
        if local_host_ip in S3API.ONLINE_ENV:
            env_db = S3API.ONLINE_DB
        elif local_host_ip in S3API.TEST_ENV:
            env_db = S3API.TEST_DB
        else:
            env_db = S3API.DEV_DB
        return env_db

    def connect_db(self, db_config):
        """!
        this function is used to connect to mysql db using db_config.
        @param db_config database configure file
        @return void
        """
        mysql_host = db_config['host']
        mysql_db = db_config['database']
        logging.debug('connecting to mysql %s', mysql_host)
        # open mysql connection
        self.db_connection = mysql.connector.connect(**db_config)
        logging.debug('connected and use db %s', mysql_db)

    def close_db(self):
        """!
        this function is used to release db connection after used mysql.
        """
        self.db_connection.close()
        logging.debug('mysql connection closed')


if __name__ == '__main__':
    obj = S3API()
    # obj.connect_db(obj.db_config)
    # obj.close_db()

    AK = '446FBB1C8616B811A6EE3FB5B0E4357E'
    SK = '2EC52EEB9A3298DDB102A0C7311EB11C'

    s3 = boto3.client('s3', aws_access_key_id=AK, aws_secret_access_key=SK,
                      endpoint_url='https://s3.cn-north-1.jdcloud-oss.com')

    rsp = s3.list_buckets()
    logging.info(rsp)
    logging.info(rsp['Buckets'])
    for each_bucket in rsp['Buckets']:
        logging.info(each_bucket)
        logging.info(each_bucket['Name'])

    bucket_name = 'openapi-north-1'
    rsp = s3.list_objects(Bucket=bucket_name)
    logging.info(rsp)

    filename = 'README.md'
    rsp = s3.upload_file(filename, bucket_name, 'test.txt')
    logging.info(rsp)

    # rsp = s3.download_file(bucket_name, 'test.log', 'test-reports/s3_obj.xml')
    rsp = s3.download_file(bucket_name, 'test.txt', 'test.log')
    logging.info(rsp)
