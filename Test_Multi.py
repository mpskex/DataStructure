#!/usr/bin/python
#coding: utf-8

#	mpsk
#	Beijing University of Technology
#	Copyright 2017

from package import *

if __name__ == '__main__':
    g = MultiPath.MultiPath(["map/map_data.npy"])
    g.AddKeyPoint(2, 10)
    g.AddKeyPoint(4, 15)
    #g.AddWayPoint(0)
    g.PrintStatus()
    print "Final result:\t", g.CalcMultiPath(0)