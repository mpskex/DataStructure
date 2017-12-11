#!/usr/bin/python
# coding: utf-8

#	mpsk
#	Beijing University of Technology
#	Copyright 2017

import os
import math
import time
from package import *
from package import MultiPath


def Test_OOL():
    """
    "Out of limit" test
    """
    g = MultiPath.MultiPath(["map/test_data.npy"])
    g.AddKeyPoint(2, 1)
    path, ool_flag = g.CalcMultiPath(0, depth=3)
    if ool_flag:
        print "====   warning   ===="
        print "Out Of Limitation!"
    print "Final result:\t", path


def Test():
    """
    Regular test
    """
    g = MultiPath.MultiPath(["map/test_data.npy"])
    #g.AddKeyPoint(2, 10)
    g.AddKeyPoint(2, 30)
    #g.AddKeyPoint(1, 7)
    g.AddWayPoint(4)
    g.AddWayPoint(3)
    # g.AddWayPoint(6)
    # g.AddWayPoint(4)
    # g.PrintStatus()
    path, ool_flag = g.CalcMultiPath(0, depth=3)
    if ool_flag:
        print "====   warning   ===="
        print "Out Of Limitation!"
    print "Final result:\t", path


if __name__ == '__main__':
    sum = 0
    a = time.time()
    Test()
    #Test_OOL()
    b = time.time()
    eval = math.floor((b - a) * 100000) / 100
    sum += eval
    print "Cost: ", eval, " ms."
    print "=============Result============="
    print "Average cost:\t", sum / 100, " ms."
