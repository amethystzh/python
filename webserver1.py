#!/usr/bin/env python
# encoding: utf-8

"""

@author:  amethystzh

@contact: amethystzh@msn.com

@software: IntelliJ IDEA

@file: webserver1.py

@time: 2018/7/19 10:47

@desc: for self trial

"""

import logging
import os
import socket

FILE_NAME = os.path.basename(__file__)
FILENAME = os.path.splitext(FILE_NAME)[0]
LOG_NAME = FILENAME + '.log'

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

    HOST, PORT = '', 8080

    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind((HOST, PORT))
    listen_socket.listen(1)

    logging.info('Serving HTTP on port %s ...' % PORT)
    while True:
        client_connection, client_address = listen_socket.accept()
        request = client_connection.recv(1024)
        logging.info('incoming request is: %s' % request)

        http_response = """
        HTTP/1.1 200 OK
    
        Hello, World!
        """

        client_connection.sendall(http_response)
        client_connection.close()
