#!/usr/bin/python
#coding:utf-8

import os
import socket
import time
import base64
import hashlib
import Comm
import json

'''   
#   请求JSON包
-   UID(base64)
    -   Hashed Hardware ID
-   SessonID(base64)
-   QRContent(base64)
    -   URL or other
-   DataType(base64)
    -   Gambling/Fishing/Porn/Malicious/None(For Sending the Content)

#   应答JSON包
##  结构设计
-   Status(base64)
    -   Responce Code
-   DataType(base64)
    -   Describe
-   Data
    -   Gambling
        -   Status
            -   Avaliable ss/ Not Avaliable
        -   Data Field 
            -   (could be empty)
    -   Fishing
    -   Porn
    -   Malicious
    
PResp
    200   （成功）  服务器已成功处理了请求。 通常，这表示服务器提供了请求的网页。 

    400   （错误请求） 服务器不理解请求的语法。 
    403   （禁止） 服务器拒绝请求。 
    404   （未找到） 服务器找不到请求。 
    405   （方法禁用） 禁用请求中指定的方法。 
    406   （不接受） 无法使用请求的内容特性响应请求的网页。  
    408   （请求超时）  服务器等候请求时发生超时。 
'''   
def PReq(uid, Content, DataType):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('127.0.0.1', 65529))
        Req = Comm.Request(uid=uid, content=Content, datatype=DataType)
        Req.Print()
        msg = json.dumps(Req.fromData())
        sock.sendall(msg)
        data = sock.recv(1024)
        print data
        Resp = Comm.Responce()
        status, Datatype, Data = Resp.toData(json.loads(data))
        Resp.Print()
        print 'Data Finished!'
        sock.close()


if __name__ == '__main__':
    uid = 'CommTest'
    Content = 'http://www.baidu.com/'
    DataType = 'None'
    PReq(uid, Content, DataType)
