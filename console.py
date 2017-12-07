#!/usr/bin/python
# coding: utf-8

#	mpsk
#	Beijing University of Technology
#	Copyright 2017

import os
import sys
import math
import time
from package import *
from package import MultiPath


trans_name=[
    u'走路',
    u'自行车',
    u'自驾车'
]

point_name=[
    u'宿舍',
    u'美食园',
    u'图书馆',
    u'逸夫图书馆',
    u'科学楼',
    u'信息楼',
    u'人文楼',
    u'软件楼',
    u'奥运场馆',
	u'三教'
	]
mp = MultiPath.MultiPath(
        ["map/walk_map.npy", 
        "map/bike_map.npy", 
        "map/car_map.npy"])

def console():
    while(True):
        print u"===  路径规划  ==="
        print "mpsk - Liu Fangrui Beijing University of Technology"
        print "\t\tCopyright 2017"
        print u"以下是可选的路径点: "
        for n in point_name:
            print '\t', n
        print u"以下是可选出行方式："
        for n in trans_name:
            print '\t', n
        start_name = ""
        while start_name not in point_name:
            print u"请输入起始路径点名称:"
            start_name = raw_input().decode(sys.stdin.encoding)
        start_i = point_name.index(start_name)
        print point_name[start_i], u" 为起始点"

        input = "a"
        while input != "exit" and input != "end":
            print u"请输入一个路径点:（输入end结束输入，输入exit退出）"
            input = raw_input().decode(sys.stdin.encoding)
            if input not in point_name:
                print "Input name is not in the list"
                continue
            i = point_name.index(input)
            while input!="keypoint" and input !="waypoint": 
                print u"keypoint or waypoint ? (从两种类型名中挑选其一)"
                input = raw_input()
            _type = input
            while input not in trans_name:
                print u"请输入该点出行方式"
                input = raw_input().decode(sys.stdin.encoding)
            trans_i = trans_name.index(input)
            cost_limit = 9999
            input = ""
            if _type=="keypoint":
                while not input.isdigit():
                    print u"请输入时间要求（一个整数）："
                    input = raw_input()
                cost_limit = int(input)
                mp.AddKeyPoint(i, cost_limit, _type_=trans_i)
            elif _type=="waypoint":
                mp.AddWayPoint(i, _type_=trans_i)
            else:
                print u"错误！非法参数"
        if input == "exit":
            return
        #
        if not mp.AddKeyPoint(start_i, 9999):
			print "[!!]\tFailed to create dst node!\t[!!]"
        path, ool_flag = mp.CalcMultiPath(start_i, depth=3)
        if ool_flag:
            print u"====   警告   ===="
            print u"\t超出时间要求！"
            print u"\t使用更宽松的时间要求来消除此警告" 
        _str = ""
        for n in path:
            if n[0] < len(point_name):
                _str += point_name[n[0]] + " -> "
            else:
                _str += u"[中继节点]" + " -> "
        _str += point_name[path[-1][1]]
        print u"抽象路径\t", path
        print u"可读路径:\t", _str
        input = raw_input("continue?(y/n)")
        #   Clear all inputs
        mp.RemovePoints()
        if input == "n":
            return

if __name__ == '__main__':
    console()
