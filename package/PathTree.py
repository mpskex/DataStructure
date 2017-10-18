#!/usr/bin/python
#coding: utf-8

import os
import re
import copy
import numpy as np
import SinglePath

#	mpsk
#	Beijing University of Technology
#	Copyright 2017

#   We introduce a Tree Structure to storage
#   every path possible
#   hierarchy;
#       [parent, [child, child]]
#       T[0] is parent node
#       T[1:n] is child node
#   In this case we use structure which is 
#   introduce BELOW:
#   node structure:
#       (node number, current cost)

def Print(node):
    print node.data
    if node.child == []:
        return
    for i in node.child:
        Print(node)

class TreeNode(object):
    def __init__(self, data):
        self.child = []
        self.data = data
        self.cost = 0
        self.cost_limit = 0
        self.depth = 0
        #   walking = 0, ridding = 1, driving = 2
        #   default = 0
        self._type_ = 0
    def SetChilds(self, child_list):
        self.child = child_list
    def AddChild(self, child):
        self.child.append(child)
    def toString(self):
        return str(self.data)

class PathTree(object):

    #   Init function
    #   --------------------------------------------
    #   paras:
    #       root
    #       child_list
    #       lastleaf
    def __init__(self, root, child_list, lastleaf):
        self.NodeTree = self.CreateTree(root, child_list)
        self.lastleaf = lastleaf

    #   Tree Creation
    #   --------------------------------------------
    #   paras:
    #       parent:   parent node
    #       child_list:   child node list
    #       lastleaf:   last leaf to be fill
    def CreateTree(self, parent, child_list):
        if child_list == []:
            return 
        return_child_list = []
        for n in child_list:
            temp_child_list = copy.deepcopy(child_list)
            #print parent, "\t", parent.toString()
            for k in temp_child_list:
                if k.data==n.data:
                    temp_child_list.remove(k)
            #print temp_child_list
            p = TreeNode(n.data)
            parent.AddChild(p)
            #print parent.child
            self.CreateTree(p, temp_child_list)
        self.NodeTree = parent
        return parent

    #   update the cost
    #   --------------------------------------------
    #   paras:
    #       node:   root node in sub tree
    #       num:    count num start
    def UpdateCost(self, root, dist_matrix, num=1):
        for i in root.child:
            i.cost = root.cost + dist_matrix[i.data][root.data]
            i.depth = num
            self.UpdateCost(i, dist_matrix, num+1)

    #   update the cost
    #   --------------------------------------------
    #   paras:
    #       node:   root node in sub tree
    #       num:    count num start
    def ReduceTree(self, root, dist_matrix, cost_limit, num=1):
        for i in root.child[:]:
            total_cost = i.cost + dist_matrix[self.lastleaf.data][i.data]
            print "to ", i.data, " path length is ", total_cost, " limit is : ", cost_limit
            if total_cost > cost_limit:
                root.child.remove(i)
            else:
                self.ReduceTree(i, dist_matrix, cost_limit, num=num+1)

    #   sort the path tree
    #   --------------------------------------------
    #   paras:
    #       root:   root node of the path tree
    def SortTree(self, root):
        for i in root.child[:]:
            self.SortTree(i)
        for n in range(len(root.child)):
            if n == 0:
                continue
            for m in range(0, n):
                if root.child[m].cost > root.child[n].cost:
                    root.child.insert(m, root.child[n].cost)
                    del root.child[n+1]
                    break

    #   pre-order traveler
    #   --------------------------------------------
    #   paras:
    #       node:   root node in sub tree
    #       num:    count num start
    def tLR(self, node, num=1):
        print num, "\t: ", node.data, "cost is :", node.cost
        if node.child!=[]:
            for i in node.child:
                self.tLR(i, num+1)

    #   pre-order printer
    #   --------------------------------------------
    #   paras:
    #       None
    def Print(self):
        print "------------------Path Tree------------------"
        self.tLR(self.NodeTree)

if __name__ == '__main__':
    pt = PathTree(TreeNode(0),[TreeNode(2),TreeNode(3),TreeNode(4)], TreeNode(5))
    pt.Print()