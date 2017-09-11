#!/usr/bin/python
#coding:utf-8

import socket
import time
import SocketServer
import json
import base64
import threading

#   mpskex@Github
#   General Purpose Server Format
#   Beijing University of Technology
#   Copyright 2017

'''   
#   请求JSON包
-   UID(base64)
    -   Hashed Hardware ID
-   SessonID(base64)
-   Data(base64)
-   DataType(base64)

#   应答JSON包
##  结构设计
-   Status(base64)
    -   Responce Code
-   DataType(base64)
    -   Describe
-   Data
    -   Binary file support Encryption Extension

    200   （成功）  服务器已成功处理了请求。 通常，这表示服务器提供了请求的网页。 

    400   （错误请求） 服务器不理解请求的语法。 
    403   （禁止） 服务器拒绝请求。 
    404   （未找到） 服务器找不到请求。 
    405   （方法禁用） 禁用请求中指定的方法。 
    406   （不接受） 无法使用请求的内容特性响应请求的网页。  
    408   （请求超时）  服务器等候请求时发生超时。 
''' 

class Responce(object):
    def __init__(self, status='', datatype='', data=''):
        self.status = status 
        self.datatype = datatype
        self.data = data
    def fromData(self):
        if self.status!='' and self.datatype!='':
            return {'Status': base64.b64encode(self.status),
                    'DataType': base64.b64encode(self.datatype),
                    'Data': self.data}
    def toData(self, datadict):
        self.status = base64.b64decode(datadict['Status'])
        self.datatype = base64.b64decode(datadict['DataType'])
        self.data = datadict['Data']
        return self.status, self.datatype, self.data
    def Print(self):
        print '=====================================\n'
        print 'Type:    Responce'
        print 'Status:\t' + self.status
        print 'DataType:\t' + self.datatype
        print 'Data:\t' , self.data , '\n'
        print '\n=====================================\n'

class Request(object):
    def __init__(self, uid='', content='', datatype=''):
        self.uid = base64.b64encode(str(hash(uid)))
        self.sid = str(int(time.time()))
        self.content = content
        self.datatype = datatype
    def fromData(self):
        if self.uid!='' and self.sid!='' and self.content!='' and self.datatype!='':
            return {'UID': base64.b64encode(self.uid),
                    'SID': base64.b64encode(self.sid),
                    'Content': base64.b64encode(self.content),
                    'DataType': base64.b64encode(self.datatype)}
    def toData(self, datadict):
        self.uid = base64.b64decode(datadict['UID'])
        self.sid = base64.b64decode(datadict['SID'])
        self.content = base64.b64decode(datadict['Content'])
        self.datatype = base64.b64decode(datadict['DataType'])
        return self.uid, self.sid, self.content, self.datatype
    def Print(self):
        print '=====================================\n'
        print 'Type:    Request'
        print 'UID:\t' + self.uid
        print 'SID:\t' + self.sid
        print 'Content:\t' + self.content 
        print 'Datatype:\t' + self.datatype + '\n'
        print '\n=====================================\n'


class server(object):
    def __init__(self, ip, port, timeout=500):
        self.__quitflag__ = False
        self.ip = ip
        self.port = port
        self.__capability__ = 100
        self.timeout = timeout
        #   UDP Based By Default
        self.sockc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockc.bind((self.ip, self.port))
    def __proc__(self, conn, addr):
        #   This part is the code u have to do yourself
        '''
        TO-DO:
        Code Need To Fill Here
        '''
        pass
    def listenc(self):
        try:
            self.sockc.listen(self.__capability__)
            while True:
                conn,addr=self.sockc.accept() 
                print'Connected by',addr    
                t = threading.Thread(target = self.__proc__, args = (conn, addr, ))
                t.start()
                if self.__quitflag__:
                    break
        except Exception, e:
            print e
        finally:
            self.sockc.close()

if __name__ == '__main__':
    s = server('127.0.0.1', 65529)
    s.listenc()