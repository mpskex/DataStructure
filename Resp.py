#!/usr/bin/python
#coding:utf-8

import os
import socket
import time
import json
import Comm
  
class Resp(Comm.server):
    def __init__(self, ip, port, timeout = 500):
        super(Resp, self).__init__(ip, port, timeout)
    def __proc__(self, conn, addr):
        try:
            #   Set the timeout config
            conn.settimeout(self.timeout)
            #   Get the recv data
            recv = conn.recv(1024)
            Req = Comm.Request()
            uid, sid, Content, DataType  = Req.toData(json.loads(recv))

            #   Preserved backdoor 
            #   Good Night~
            if sid == 'Gute Nacht!':
                self.__quitflag__ = True
            #   ATTENTION:  Should be removed in Deploy Version

            Req.Print()
            #   Here we just use the DataType and Data section

        except Exception, e:
            print e.message
        finally:
            conn.close()

if __name__ == '__main__':
    s = Resp('localhost', 65529)
    s.listenc()