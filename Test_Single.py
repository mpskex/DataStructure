#!/usr/bin/python
#coding: utf-8

#	mpsk
#	Beijing University of Technology
#	Copyright 2017

from package import *

if __name__ == '__main__':
    g = SinglePath.SinglePath("map/map_data.npy")
    print "The map size is:\n", g.map_size, "\nThe map of Guide is:\n", g.dist_map
    print "The generated path is:\n", g.neigh_map
    print "The dist matrix of the Guide is:\n", g.SGT_Floyd_Update()[0], "\n", g.SGT_Floyd_Update()[1]
    print "Path is : ", g.SSSP_Floyd(3,6)[1]