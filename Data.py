#   coding: utf-8
import os
import re
import numpy as np

#	mpsk
#	Beijing University of Technology
#	Copyright 2017

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
		#	define the infinite value in storage structure
		self.INIFINITE = 9999
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
		pass

	#   method to set data with a manifactured
	#   matrix
	#       paras:
	#       data:   matrix data
	def setData(self, data):
		pass
	
	#   Single Source Shortest Path
	#   method to get the best routine in graph G
	#       paras:
	#       node_src:   source of the routine
	#       node_dst:   destination of the routine
	def SSSP(self, node_src, node_dst):
		dist = self.map.copy()
		path = np.zeros(dist.shape, np.int)
		for i in range(dist.shape[0]):
			for j in range(dist.shape[0]):
				for k in range(dist.shape[0]):
					if dist[i][j] + dist[j][k] < dist[i][k]:
						dist[i][k] = dist[i][j] + dist[j][k]
		return dist, path

if __name__ == '__main__':
	g = MapGuide("map_data.npy")
	print "The map of Guide is:\n", g.map
	print "The dist matrix of the Guide is:\n", g.SSSP(0,0)[0], "\n", g.SSSP(0,0)[1]