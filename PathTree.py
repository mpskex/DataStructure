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
    def SetChild(self, child_list):
        self.child = child_list
    def AddChild(self, child):
        self.child.append(child)
    def NodePrint(self):
        return str(self.data) + " child:", self.child

class PathTree(object):

    #   Init function
    #   --------------------------------------------
    #   paras:
    #       None
    def __init__(self):
        self.Tree = []
        pass

    #   Tree Creation
    #   --------------------------------------------
    #   paras:
    #       parent:   parent node
    #       child_list:   child node list
    #       lastleaf:   last leaf to be fill
    def CreateTreeList(self, parent, child_list, lastleaf):
        if child_list == []:
            return [parent, lastleaf]
        return_child_list = []
        for n in child_list:
            temp_child_list = copy.deepcopy(child_list)
            temp_child_list.remove(n)
            return_child_list.append(self.CreateTree(n, temp_child_list, lastleaf))
        print node.NodePrint()
        self.Tree = [parent, return_child_list]
        return self.Tree

    #   Tree Creation
    #   --------------------------------------------
    #   paras:
    #       parent:   parent node
    #       child_list:   child node list
    #       lastleaf:   last leaf to be fill
    def CreateTree(self, parent, child_list, lastleaf):
        node = TreeNode(parent)
        if child_list == []:
            return [parent, lastleaf]
        return_child_list = []
        for n in child_list:
            temp_child_list = copy.deepcopy(child_list)
            temp_child_list.remove(n)
            node.AddChild(n)
            print "--"
            return_child_list.append(self.CreateTree(n, temp_child_list, lastleaf))
        print node.NodePrint()
        self.Tree = [parent, return_child_list]
        return node

if __name__ == '__main__':
    pt = PathTree()
    #print pt.CreateTree(0,[2,3,4], 5)[0]
    pt.CreateTree(0,[2,3,4], 5)