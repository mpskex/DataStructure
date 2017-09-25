#!/usr/bin/python
#coding: utf-8

import os
import re
import numpy as np
import SinglePath

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
class Multipath(object):

    #   the init function is to create floyd map for
    #   the specified graph G.
    #   --------------------------------------------
    #   paras:
    #       map_path:   path to map data
    def __init__(self, map_path):
        #   create single path control path
        self.singlepath = SinglePath.SinglePath(map_path)
        #   create 2D key point list
        #   *   first dimension choose the list
        #   *   second choose the keypoint
        empty = []
        self.keypoints = []
        for i in range(1,2):
            self.keypoints.append(empty)
        #   create the waypoint list
        self.waypoints = []

    #   Add KeyPoint
    #   --------------------------------------------
    #   paras:
    #       node:       keypoint node number
    #       time_cost:  time cost this node limited
    def AddKeyPoint(self, node, time_cost):
        #   Add node to keypoints list
        self.keypoints[0].append(node)
        self.keypoints[1].append(time_cost)
    
    #   Add WayPoint
    #   --------------------------------------------
    #   paras:
    #       node:       keypoint node number
    #       time_cost:  time cost this node limited
    def AddKeyPoint(self, node):
        #   Add node to waypoints list
        self.waypoints.append(node)

    #   MultiPath
    #   --------------------------------------------
    #   paras:
    #       node:       keypoint node number
    #       time_cost:  time cost this node limited
    def CalcMultiPath(self,)