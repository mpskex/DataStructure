#!/usr/bin/python
#coding: utf-8

#	mpsk
#	Beijing University of Technology
#	Copyright 2017

from package import *
from package import MultiPath

if __name__ == '__main__':
    g = MultiPath.MultiPath(["map/test_data.npy"])
    #g.AddKeyPoint(2, 10)
    g.AddKeyPoint(2, 30)
    #g.AddKeyPoint(1, 7)
    g.AddWayPoint(4)
    g.AddWayPoint(3)
    #g.AddWayPoint(6)
    #g.AddWayPoint(4)
    #g.PrintStatus()
    print "Final result:\t", g.CalcMultiPath(0, depth=3)