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

class PathTree(object):
    def __init__(self):
        pass

    #   Tree Creation
    #   --------------------------------------------
    #   paras:
    #       parent:   parent node
    #       child_list:   child node list
    #       lastleaf:   last leaf to be fill
    def CreateTree(self, parent, child_list, lastleaf):
        if child_list == []:
            return [parent, lastleaf]
        return_child_list = []
        for n in child_list:
            temp_child_list = copy.deepcopy(child_list)
            temp_child_list.remove(n)
            return_child_list.append(self.CreateTree(n, temp_child_list, lastleaf))
        return [parent, return_child_list]