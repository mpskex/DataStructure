#!/usr/bin/python
#coding: utf-8

#	mpsk
#	Beijing University of Technology
#	Copyright 2017

from package import *
from package import MultiPath

if __name__ == '__main__':
    g = MultiPath.MultiPath(["map/map_data.npy"])
    g.AddKeyPoint(2, 76)
    g.AddKeyPoint(1, 61)
    g.AddWayPoint(5)
    g.AddWayPoint(7)
    g.AddWayPoint(6)
    g.AddWayPoint(4)
    g.PrintStatus()
    print "Final result:\t", g.CalcMultiPath(0, depth=2)