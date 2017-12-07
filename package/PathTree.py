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
    """
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
    """
    def __init__(self, root, child_list, lastleaf):
        """
        #   Init function
        #   --------------------------------------------
        #   paras:
        #       root
        #       child_list
        #       lastleaf
        #   only key nodes
        """
        self.straight_dist = 0
        if child_list == []:
            self.NodeTree = root
            self.lastleaf = lastleaf
        else:
            self.NodeTree = self.CreateTree(root, child_list)
            self.lastleaf = lastleaf
        self.INFINITE = 9999

    def CreateTree(self, parent, child_list):
        """
        #   Tree Creation
        #   --------------------------------------------
        #   paras:
        #       parent:   parent node
        #       child_list:   child node list
        #       lastleaf:   last leaf to be fill
        """
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
            p.parent = parent
            parent.AddChild(p)
            #print parent.child
            self.CreateTree(p, temp_child_list)
        self.NodeTree = parent
        return parent

    def UpdateCost(self, root, spath_obj, num=1):
        """
        #   update the cost
        #   --------------------------------------------
        #   paras:
        #       node:   root node in sub tree
        #       num:    count num start
        """
        for i in root.child:
            i.cost = root.cost + spath_obj[i._type_].dist[i.data][root.data]
            i.depth = num
            self.UpdateCost(i, spath_obj, num+1)
        if num==1:
            self.straight_dist = spath_obj[self.lastleaf._type_].dist[self.lastleaf.data][root.data]

    def ReduceTree(self, root, spath_obj, cost_limit, depth, num=1):
        """
        #   cut the branch which mismatch the limit of cost
        #   --------------------------------------------
        #   paras:
        #       node:   root node in sub tree
        #       num:    count num start
        """
        for i in root.child[:]:
            total_cost = i.cost + spath_obj[self.lastleaf._type_].dist[self.lastleaf.data][i.data]
            print "to ", i.data, " path length is ", total_cost, " limit is : ", cost_limit
            if total_cost > cost_limit or num >= depth:
                root.child.remove(i)
            else:
                self.ReduceTree(i, spath_obj, cost_limit, num=num+1, depth=depth)

    def SortTree(self, root):
        """
        #   sort the path tree
        #   --------------------------------------------
        #   paras:
        #       root:   root node of the path tree
        """
        for i in root.child[:]:
            self.SortTree(i)
        for n in range(len(root.child)):
            if n == 0:
                continue
            for m in range(0, n):
                if root.child[m].cost < root.child[n].cost:
                    root.child.insert(m, root.child[n])
                    del root.child[n+1]
                    break

    def FindPath(self, node):
        """
        #   Shortest Path finder
        #   --------------------------------------------
        #   paras:
        #       node:   root node in sub tree
        """
        stack = []
        min_cost = self.INFINITE
        #   if it is straght-to
        #   then return the straight-to dist
        min_cost_r = self.straight_dist
        min_node = node
        #   Push the Item into a stack
        if node.child == []:
            min_node = node
        for i in range(0,len(node.child)):
            stack.append(node.child[i])
        #   while stack is not empty
        while(stack):
            #   if it has child
            #   other word the tree is not empty
            #   then get the smallest dist
            min_cost_r = self.INFINITE
            #   pop a item
            cur_node = stack[-1]
            del stack[-1]
            if cur_node.child==[]:
                if cur_node.cost < min_cost:
                    min_node = cur_node
                    min_cost = min_node.cost
                continue
            min_cost_r = min_cost
            for i in range(0,len(cur_node.child)):
                stack.append(cur_node.child[i])
        return min_node, min_cost_r

    def tLR(self, node, num=1):
        """
        #   pre-order traveler
        #   --------------------------------------------
        #   paras:
        #       node:   root node in sub tree
        #       num:    count num start
        """
        print "|| lv.", num-1, " : ", node.data, "| cost is :", node.cost, "||"
        if node.child!=[]:
            for i in node.child:
                self.tLR(i, num+1)

    def Print(self):
        """
        #   pre-order printer
        #   --------------------------------------------
        #   paras:
        #       None
        """
        print "---*******Path Tree*******---"
        self.tLR(self.NodeTree)
        print "---*******Tree Ends*******---\n"

if __name__ == '__main__':
    pt = PathTree(TreeNode(0),[TreeNode(2),TreeNode(3),TreeNode(4)], TreeNode(5))
    pt.Print()