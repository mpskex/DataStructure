#   coding: utf-8
import os
import re
import numpy as np


#   This class is to storage the data
#   of the neighbour table
#   For a weighted graph G, every distance
#   is saved in the matrix M(i,j) for position
#   row i and column j
class MapGuide(object):

	#   the init proc is to create the 
	#   neighbour table with numpy
	#       paras:
	#       node_num:   number of node
	#		map_path:	path to map data
	def __init__(self, map_path):
		#   first load the map data from file or database
		#   then copy each path distance to the path data
		self.map = self.__LoadMap__(map_path)
		pass

	#   private method to load map data
	#       paras:
	#       map: map data of matrix format
	def __LoadMap__(self, map):
		return np.load(map)

	#   method to get data from object
	#       paras:
	#       none
	def getData(self):
		return self.data

	#   method to set data with a manifactured
	#   matrix
	#       paras:
	#       data:   matrix data
	def setData(self, data):
		self.path = path
	
	#   Single Source Shortest Path
	#   method to get the best routine in graph G
	#       paras:
	#       node_src:   source of the routine
	#       node_dst:   destination of the routine
	def SSSP(self, node_src, node_dst):
		
		return self.data

if __name__ == '__main__':
	g = MapGuide("map_data.npy")
	print g.map