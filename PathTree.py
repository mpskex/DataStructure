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
        self.NodeTree = self.CreateTree(root, child_list, lastleaf)

    #   Tree Creation
    #   --------------------------------------------
    #   paras:
    #       parent:   parent node
    #       child_list:   child node list
    #       lastleaf:   last leaf to be fill
    def CreateTree(self, parent, child_list, lastleaf):
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
            self.CreateTree(p, temp_child_list, lastleaf)
        self.NodeTree = parent
        return parent

    #   update the cost
    #   --------------------------------------------
    #   paras:
    #       node:   root node in sub tree
    #       num:    count num start
    def UpdateCost(self, node, dist_matrix, depth, num=1):
        if node.child!=[]:
            for i in node.child:
                i.cost = node.cost + dist_matrix[i.data][node.data]
                self.UpdateCost(i, dist_matrix, depth, num+1)

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
        self.tLR(self.NodeTree)

if __name__ == '__main__':
    pt = PathTree(TreeNode(0),[TreeNode(2),TreeNode(3),TreeNode(4)], TreeNode(5))
    pt.Print()