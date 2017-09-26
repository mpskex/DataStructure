#!/usr/bin/python
#coding: utf-8

import os
import re
import copy
import numpy as np
import SinglePath
import PathTree

#	mpsk
#	Beijing University of Technology
#	Copyright 2017

#   For every keypoint i, we choose the BEST path
#   (depends on strategy), less time/more effciency 
#   while passing as many nodes as possible in limited 
#   time
#   If there are still plenty time left, we would consider
#   including more nodes to path
#   Two point type:
#       keypoint:   limited time
#       waypoint:   don't care about time
class MultiPath(object):

    #   the init function is to create floyd map for
    #   the specified graph G.
    #   --------------------------------------------
    #   paras:
    #       map_path:   path to map data
    def __init__(self, map_path):
        #   create single path control path
        self.singlepath = SinglePath.SinglePath(map_path)
        #   create 2D key point list
        #   keypoints[index][node_num/time_limit]
        self.keypoints = []
        #   create the waypoint list
        self.waypoints = []

    #   Add KeyPoint
    #   --------------------------------------------
    #   paras:
    #       node:       keypoint node number
    #       time_cost:  time cost this node limited
    def AddKeyPoint(self, node, time_cost):
        #   Add node to keypoints list
        self.keypoints.append((node, time_cost))
    
    #   Add WayPoint
    #   --------------------------------------------
    #   paras:
    #       node:       keypoint node number
    #       time_cost:  time cost this node limited
    def AddWayPoint(self, node):
        #   Add node to waypoints list
        self.waypoints.append(node)

    #   MultiPath
    #   --------------------------------------------
    #   paras:
    #       node_i:     start point
    def CalcMultiPath(self, node_i):
        if self.waypoints!=[] and self.keypoints!=[]:
            #   DO
            path = []
            waypoint_list = self.waypoints
            pathtrees = []
            #   for every key point with limited time
            for i in range(len(self.keypoints)):
                ptree = PathTree.PathTree()
                pathtrees.append(ptree.CreateTree(i, waypoint_list, node_i))
                print ptree.Tree

if __name__ == '__main__':
    g = MultiPath("map_data.npy")
    g.AddKeyPoint(2, 10)
    g.AddKeyPoint(4, 15)
    g.AddWayPoint(1)
    g.AddWayPoint(3)
    g.CalcMultiPath(0)