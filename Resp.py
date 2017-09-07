#!/usr/bin/python
#coding:utf-8

import os
import socket
import time
import json
import base64
import Comm
import threading

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
    -   ContentType
    -   Gambling
        -   Status
            -   Avaliable ss/ Not Avaliable
        -   Data Field 
            -   (could be empty)
    -   Fishing
    -   Porn
    -   Malicious
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
class Resp(Comm.server):
    def __init__(self, ip, port, timeout = 500):
        self.sessions = [('null', 0)]
        super(Resp, self).__init__(ip, port, timeout)
    def __proc__(self, conn, addr):
        try:
            conn.settimeout(self.timeout)
            recv = conn.recv(1024)
            Req = Comm.Request()
            uid, sid, Content, DataType  = Req.toData(json.loads(recv))
            if sid == 'Gute Nacht!':
                #   Good Night~
                self.__quitflag__ = True
            Req.Print()
            #   防止重复提交
            if int(sid) >= int(self.sessions[-1][1]) + 1:
                status = 'TODO'
                self.sessions.append((uid, sid, Content, status))
                Resp = Comm.Responce(status='200', datatype='Gambling', data=['0.1', '0.2'])
                conn.sendall(json.dumps(Resp.fromData()))
            else:
                Resp = Comm.Responce(status='403', datatype='NULL', data='NULL')
                conn.sendall(json.dumps(Resp.fromData()))
            #   Sorted by the SessionID
            self.sessions = sorted(self.sessions, key = lambda x : x[1], reverse = False)
            #print self.sessions

        except Exception, e:
            print e.message
        finally:
            conn.close()

if __name__ == '__main__':
    s = Resp('0.0.0.0', 65529)
    s.listenc()