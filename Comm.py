#!/usr/bin/python
#coding:utf-8
'''
Author:     mpsk
Date:       2017-05-04
Function:   Server for 
            Remote Connection via Proxy Server in TCP/IP Socket
Version:    1.0.5
'''
import socket
import time
import SocketServer
import json

class Data(object):
    def __init__(self, flag, idict):
        self.flag = flag
        self.obj = idict
    def toJson(self):
        return json.dumps(self.obj)
    def fromJson(self, jdata):
        return json.loads(jdata)

class target(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

class server(object):
    def __init__(self, target, timeout=500):
        self.target = target
        self.timeout = timeout
        self.msglist = ['null']
        self.sockc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockc.bind((self.target.ip, self.target.port))
    def listenc(self):
        self.sockc.listen(5)
        while (True):
            conn,addr=self.sockc.accept() 
            print'Connected by',addr    
            try:
                conn.settimeout(self.timeout)
                data=conn.recv(1024)
                return data
            except:
                print(e)
                conn.close()
                break
            conn.close()
        self.closec()
    def closec(self):
        self.sockc.close()

if __name__ == '__main__':
    d = Data(True, {"that":1,"this":2})
    print d.toJson()
    print d.fromJson(d.toJson())