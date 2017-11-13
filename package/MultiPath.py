#!/usr/bin/python
#coding: utf-8

import copy
import numpy as np
import SinglePath
import PathTree

class MultiPath(object):
    """
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
    """

    def __init__(self, map_path_list):
        """
        #   the init function is to create floyd map for
        #   the specified graph G.
        #   --------------------------------------------
        #   paras:
        #       map_path:   path to map data
        """
        #   create single path control path
        self.singlepath_list = []
        for n in map_path_list:
            self.singlepath_list.append(SinglePath.SinglePath(n))
        #   create the waypoint list
        self.keypoints = []
        self.waypoints = []
        self.INFINITE = 9999

    def RemovePoints(self):
        self.keypoints = []
        self.waypoints = []
    
    def RemovePoint(self, num):
        print "Removing ", num, " node"
        for n in range(len(self.keypoints)):
            if num == self.keypoints[n].data:
                del self.keypoints[n]
                return True
        for n in range(len(self.waypoints)):
            if num == self.waypoints[n].data:
                del self.waypoints[n]
                return True
        print "[!]Remove Failed!"
        return False

    def PrintStatus(self):
        print "KeyPoints:"
        for n in self.keypoints:
            print "\t", n.data, "\n\tcost : ", n.cost, "\n\tcost limit : ", n.cost_limit
        print "WayPoints:"
        for n in self.waypoints:
            print "\t", n.data, "\n\tcost : ", n.cost

    def AddKeyPoint(self, point, time_cost, _type_=0):
        """
        #   Add KeyPoint
        #   --------------------------------------------
        #   paras:
        #       point:      keypoint node number
        #       time_cost:  time cost this node limited
        #   Add node to keypoints list
        #   check if the point is in the waypoint list or keypoint list
        """
        for n in self.waypoints:
            if n.data == point:
                print "[!!]\tWarning\tDetected Duplicated Point while create! Ignored!\t[!!]"
                return False
        for n in self.keypoints:
            if n.data == point:
                print "[!!]\tWarning\tDetected Duplicated Point while create! Ignored!\t[!!]"
                return False
        #   Invalid time cost
        if time_cost<=0:
            print "[!!]\tWarning\tInvalid Cost Input\t[!!]"
            return False
        #   over the map
        if point > self.singlepath_list[_type_].map_size:
            print "[!!]\tWarning\tPoint Index out of range\t[!!]"
            return False
        p = PathTree.TreeNode(int(point))
        p.cost = 0
        p.cost_limit = int(time_cost)
        self.keypoints.append(p)
        return True

    def AddWayPoint(self, point):
        """
        #   Add WayPoint
        #   --------------------------------------------
        #   paras:
        #       point:      keypoint node number
        #       time_cost:  time cost this node limited
        """
        #   Add node to waypoints list
        #   check if the point is in the waypoint list or keypoint list
        for n in self.waypoints:
            if n.data == point:
                return False
        for n in self.keypoints:
            if n.data == point:
                return False
        #   over the map
        if point > self.singlepath_list[0].map_size:
            return False
        self.waypoints.append(PathTree.TreeNode(point))
        return True

        
    def __Macro_Path_Out__(self, tree, lastleaf, way_nodes):
        """
        #   Output a best Macro-route according current strategy
        #   use recurrent method
        #   --------------------------------------------
        #   paras:
        #       root:       root node of PathTree
        #       lastleaf:   last leaf node in PathTree
        #   current strategy is to find the shortest path in pathtree
        """
        temp_path = []
        min_node = tree.FindPath(tree.NodeTree)
        node_cur = min_node
        while(node_cur!=tree.NodeTree):
            temp_path.insert(0, node_cur.data)
            #   check if the waypoint is included by the macro path
            for n in range(len(way_nodes)):
                if node_cur.data == way_nodes[n].data:
                    print "[!]Repeated[!] ", way_nodes[n].data
                    del way_nodes[n]
                    break
            node_cur = node_cur.parent
        temp_path.append(tree.NodeTree.data)
        temp_path.insert(0, lastleaf.data)
        print "[*]\tPath Tree Result is\t", temp_path
        return temp_path
    
    def __Micro_Path_Out__(self, root, lastleaf):
        """
        #   Output a best Micro-route according current strategy
        #   use recurrent method
        #   --------------------------------------------
        #   paras:
        #       root:       root node of PathTree
        #       lastleaf:   last leaf node in PathTree
        """
        #   current strategy is to select first path
        min = self.singlepath_list[0].INFINITE
        node_cur = root
        node_last = node_cur
        temp_path = []
        while node_cur.child!=[]:
            temp_path.insert(0, node_cur.data)
            node_last = node_cur
            node_cur = node_cur.child[0]
        temp_path.insert(0, node_cur.data)
        temp_path.insert(0, lastleaf.data)
        return temp_path

    def CalcMultiPath(self, point_i, depth):
        """
        #   MultiPath
        #   --------------------------------------------
        #   paras:
        #       node_i:     start point
        """
        #   Add the begin node to the key node list
        key_nodes = copy.deepcopy(self.keypoints)
        key_nodes.insert(0, PathTree.TreeNode(point_i))
        t_dst = PathTree.TreeNode(point_i)
        t_dst.cost_limit = self.INFINITE
        key_nodes.append(t_dst)
        way_nodes = copy.deepcopy(self.waypoints)
        macro_path = []
        if len(key_nodes)>1:
            print "\n[*] Stage 1 : Keynodes:", len(key_nodes), " Waynodes: ", len(way_nodes)
            #   DO
            path = []
            #   Node should be sort by time cost
            pathtrees = []
            #   Macro Path list
            macro_path = []
            #   Do the Path Tree Iterations
            #   for every key point with limited time
            while len(key_nodes) > 1 and len(way_nodes) > 0:
                #   set source and destination
                if len(key_nodes)>1:
                    node_src = key_nodes[0]
                    node_dst = key_nodes[1]
                elif len(key_nodes)<=1 and len(way_nodes)>0:
                    #   if the way node is still not empty 
                    node_src = key_nodes[0]
                    node_dst = PathTree.TreeNode(point_i)
                else:
                    return False
                if node_src.data == node_dst.data and node_src.data != point_i:
                    del key_nodes[0]
                    print "[!!]\tWarning\tDetected Duplicated Point! Ignored!\t[!!]"
                    continue
                #   Last point does't need limitation 
                if node_dst.data == point_i:
                    depth = self.INFINITE
                #way_nodes = copy.deepcopy(self.waypoints)
                print "to ", node_dst.data, " from ", node_src.data
                #   Build Path Tree
                ptree = PathTree.PathTree(node_dst, way_nodes, node_src)
                #   Update all cost on each nodes
                ptree.UpdateCost(ptree.NodeTree, self.singlepath_list[node_src._type_].dist)
                ptree.Print()
                print "[*]\tPath depth limit is ", depth
                ptree.ReduceTree(ptree.NodeTree, self.singlepath_list[node_src._type_].dist, node_dst.cost_limit, depth)
                ptree.Print()
                ptree.SortTree(ptree.NodeTree)
                ptree.Print()
                macro_path.append(self.__Macro_Path_Out__(ptree, node_src, way_nodes))
                del key_nodes[0]

        print macro_path

        #   concenate the path pieces into continuos path sequence
        mid_path = []
        for n in macro_path:
            for m in n[1:]:
                mid_path.append(m)
        mid_path.insert(0, macro_path[0][0])
        print "Macro Path is :\t", mid_path

        #   get list of single paths
        #   the point pair which describe the path
        micro_path_p = []
        while len(mid_path)>1:
            point_src = mid_path[0]
            point_dst = mid_path[1]
            micro_path_p.append(self.singlepath_list[node_src._type_].SSSP_Floyd(point_src, point_dst)[1])
            del mid_path[0]
            
        #   get micro path
        
        micro_path = []
        for n in micro_path_p:
            for m in n[1:]:
                micro_path.append(m)
        micro_path.insert(0, micro_path_p[0][0])
        
        tag_path = []
        while len(micro_path)>1:
            tag_temp = [micro_path[0],micro_path[1]]
            tag_path.append(tag_temp)
            del micro_path[0]

        return  tag_path


if __name__ == '__main__':
    g = MultiPath(["map_data.npy"])
    g.AddKeyPoint(2, 10)
    #g.AddKeyPoint(4, 15)
    g.AddWayPoint(1)
    g.AddWayPoint(3)
    g.PrintStatus()
    print "Final result:\t", g.CalcMultiPath(0)