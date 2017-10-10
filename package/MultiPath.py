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
        self.INFINITE = 9999

    def RemovePoints(self):
        self.keypoints = []
        self.waypoints = []

    def PrintStatus(self):
        print "KeyPoints:"
        for n in self.keypoints:
            print "\t", n.data, "\n\tcost : ", n.cost, "\n\tcost limit : ", n.cost_limit
        print "WayPoints:"
        for n in self.waypoints:
            print "\t", n.data, "\n\tcost : ", n.cost

    #   Add KeyPoint
    #   --------------------------------------------
    #   paras:
    #       point:      keypoint node number
    #       time_cost:  time cost this node limited
    def AddKeyPoint(self, point, time_cost):
        #   Add node to keypoints list
        #   check if the point is in the waypoint list or keypoint list
        for n in self.waypoints:
            if n.data == point:
                return False
        for n in self.keypoints:
            if n.data == point:
                return False
        #   Invalid time cost
        if time_cost<=0:
            return False
        #   over the map
        if point > self.singlepath.map_size:
            return False
        p = PathTree.TreeNode(int(point))
        p.cost = 0
        p.cost_limit = int(time_cost)
        self.keypoints.append(p)
        return True

    
    #   Add WayPoint
    #   --------------------------------------------
    #   paras:
    #       point:      keypoint node number
    #       time_cost:  time cost this node limited
    def AddWayPoint(self, point):
        #   Add node to waypoints list
        #   check if the point is in the waypoint list or keypoint list
        for n in self.waypoints:
            if n.data == point:
                return False
        for n in self.keypoints:
            if n.data == point:
                return False
        #   over the map
        if point > self.singlepath.map_size:
            return False
        self.waypoints.append(PathTree.TreeNode(point))
        return True

        
    #   Output a best Macro-route according current strategy
    #   use recurrent method
    #   --------------------------------------------
    #   paras:
    #       root:       root node of PathTree
    #       lastleaf:   last leaf node in PathTree
    def __Macro_Path_Out__(self, root, lastleaf, way_nodes):
        #   current strategy is to select first path
        min = self.singlepath.INFINITE
        node_cur = root
        node_last = node_cur
        temp_path = []
        while node_cur.child!=[]:
            temp_path.insert(0, node_cur.data)
            node_last = node_cur
            node_cur = node_cur.child[0]
            #   check if the waypoint is included by the macro path
            for n in range(len(way_nodes)):
                if node_cur.data == way_nodes[n].data:
                    print "[!]Repeated[!] ", way_nodes[n].data
                    del way_nodes[n]
        temp_path.insert(0, node_cur.data)
        temp_path.insert(0, lastleaf.data)
        return temp_path
    
    #   Output a best Micro-route according current strategy
    #   use recurrent method
    #   --------------------------------------------
    #   paras:
    #       root:       root node of PathTree
    #       lastleaf:   last leaf node in PathTree
    def __Micro_Path_Out__(self, root, lastleaf):
        #   current strategy is to select first path
        min = self.singlepath.INFINITE
        node_cur = root
        node_last = node_cur
        temp_path = []
        while node_cur.child!=[]:
            temp_path.insert(0, node_cur.data)
            node_last = node_cur
            node_cur = node_cur.child[0]
        temp_path.insert(0, node_cur.data)
        temp_path.insert(0, lastleaf.data)

    #   MultiPath
    #   --------------------------------------------
    #   paras:
    #       node_i:     start point
    def CalcMultiPath(self, point_i):
        #   Do the Path Tree Iterations
        if self.waypoints!=[] and self.keypoints!=[]:
            #   DO
            path = []
            key_nodes = copy.deepcopy(self.keypoints)
            #   insert source node to key_nodes list
            key_nodes.insert(0, PathTree.TreeNode(point_i))
            #   Node should be sort by time stamp
            pathtrees = []
            #   Macro Path list
            macro_path = []
            #   for every key point with limited time
            while len(key_nodes) > 1:
                #   set source and destination
                node_src = key_nodes[0]
                node_dst = key_nodes[1]
                way_nodes = copy.deepcopy(self.waypoints)
                print "to ", node_dst.data, " from ", node_src.data
                #   Build Path Tree
                ptree = PathTree.PathTree(node_dst, way_nodes, node_src)
                #   Update all cost on each nodes
                ptree.UpdateCost(ptree.NodeTree, self.singlepath.dist)
                ptree.Print()
                ptree.ReduceTree(ptree.NodeTree, self.singlepath.dist, node_dst.cost_limit)
                ptree.Print()
                ptree.SortTree(ptree.NodeTree)
                ptree.Print()
                macro_path.append(self.__Macro_Path_Out__(ptree.NodeTree, node_src, way_nodes))
                #   code here
                del key_nodes[0]

            #   if the way node is still not empty 
            #   after the keynode iteration
            if way_nodes!=[]:
                #   Choose the nearest way point from the last key point
                node_src = key_nodes[0]
                node_cur = node_src
                print "[!]  Remained way point : "
                for i in way_nodes:
                    print "\t\t", i.data
                print "\t from key point : ", node_src.data
                temp_path = [key_nodes[0].data]
                temp_min_node_num = 0
                temp_min_dist = self.INFINITE
                while len(way_nodes)>1:
                    for n in range(len(way_nodes)):
                        if self.singlepath.dist[node_cur.data][way_nodes[n].data] < temp_min_dist:
                            temp_min_node_num = n
                            temp_min_dist = self.singlepath.dist[node_cur.data][way_nodes[n].data]
                    temp_path.append(way_nodes[temp_min_node_num].data)
                    node_cur = copy.deepcopy(way_nodes[temp_min_node_num])
                    del way_nodes[temp_min_node_num]
                temp_path.append(way_nodes[0].data)
                macro_path.append(temp_path)
            print macro_path

            #   concenate the path pieces into continuos path sequence
            mid_path = []
            for n in macro_path:
                for m in n[1:]:
                    mid_path.append(m)
            mid_path.insert(0, macro_path[0][0])
            print "Macro Path is :\t", mid_path

            #   get list of single paths
            micro_path_p = []
            while len(mid_path)>1:
                point_src = mid_path[0]
                point_dst = mid_path[1]
                micro_path_p.append(self.singlepath.SSSP_Floyd(point_src, point_dst)[1])
                del mid_path[0]
                
            #   get micro path
            micro_path = []
            for n in micro_path_p:
                for m in n[1:]:
                    micro_path.append(m)
            micro_path.insert(0, micro_path_p[0][0])
            return micro_path


if __name__ == '__main__':
    g = MultiPath("map_data.npy")
    g.AddKeyPoint(2, 10)
    #g.AddKeyPoint(4, 15)
    g.AddWayPoint(1)
    g.AddWayPoint(3)
    g.PrintStatus()
    print "Final result:\t", g.CalcMultiPath(0)