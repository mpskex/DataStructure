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
        #   create the waypoint list
        self.keypoints = []
        self.waypoints = []

    #   Add KeyPoint
    #   --------------------------------------------
    #   paras:
    #       point:      keypoint node number
    #       time_cost:  time cost this node limited
    def AddKeyPoint(self, point, time_cost):
        #   Add node to keypoints list
        p = PathTree.TreeNode(point)
        p.cost = 0
        p.cost_limit = time_cost
        self.keypoints.append(p)

    
    #   Add WayPoint
    #   --------------------------------------------
    #   paras:
    #       point:      keypoint node number
    #       time_cost:  time cost this node limited
    def AddWayPoint(self, point):
        #   Add node to waypoints list
        self.waypoints.append(PathTree.TreeNode(point))

    #   MultiPath
    #   --------------------------------------------
    #   paras:
    #       node_i:     start point
    def CalcMultiPath(self, point_i):
        node_src = PathTree.TreeNode(point_i)
        if self.waypoints!=[] and self.keypoints!=[]:
            #   DO
            path = []
            key_nodes = copy.deepcopy(self.keypoints)
            #   Node should be sort by time stamp
            pathtrees = []
            #   for every key point with limited time
            while len(key_nodes) > 1:
                node_dst = key_nodes[0]
                way_nodes = copy.deepcopy(self.waypoints)
                print "to ", node_dst.data, " from ", node_src.data
                #   Build Path Tree
                ptree = PathTree.PathTree(node_dst, way_nodes, node_src)
                #   Update all cost on each nodes
                ptree.UpdateCost(ptree.NodeTree, self.singlepath.dist)
                ptree.ReduceTree(ptree.NodeTree, self.singlepath.dist, key_nodes[0].cost_limit)
                ptree.Print()
                #   code here
                node_src = node_dst
                node_dst = key_nodes[1]
                del key_nodes[0]

if __name__ == '__main__':
    g = MultiPath("map_data.npy")
    g.AddKeyPoint(2, 10)
    g.AddKeyPoint(4, 15)
    g.AddWayPoint(1)
    g.AddWayPoint(3)
    g.CalcMultiPath(0)