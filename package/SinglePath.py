#   coding: utf-8
import os
import re
import numpy as np

#	Map Structure:
#	the dist_map[i][j] is the distance between node i and node j
#	the neigh_map[i][j] means that the 


#	mpsk
#	Beijing University of Technology
#	Copyright 2017

#   For a weighted graph G, every distance
#   is saved in the matrix M(i,j) for position
#   row i and column j
class SinglePath(object):

	#   the init proc is to create the 
	#   neighbour table with numpy
	#	------------------------------------------------
	#	paras:
	#		map_path:	path to map data
	def __init__(self, map_path):
		#	define the infinite value in storage structure
		self.INFINITE = 9999
		#   first load the map data from file or database
		#   then copy each path distance to the path data
		self.dist_map = self.__LoadMap__(map_path)
		self.neigh_map = self.__GenPath__(self.dist_map)
		#	update the floyd matrix
		self.dist, self.path = self.SGT_Floyd_Update()
		self.map_size = self.dist_map.shape[0]
		pass

	#   private method to load map data
	#	------------------------------------------------
	#	paras:
	#       path2map: path to a matrix format binary file
	def __LoadMap__(self, path2map):
		return np.load(path2map)

	#	private method to generate the neighbour table
	def __GenPath__(self, map):
		path = map.copy()
		for i in range(path.shape[0]):
			for j in range(path.shape[1]):
				#	node_i has no path to node_j
				if map[i][j] ==self.INFINITE:
					path[i][j] = -1
				#	node_i to node_j and the former neighbour is i
				else:
					path[i][j] = i
		return path

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
	
	#   Smallest Generated Tree
	#	Algorithm of Floyd
	#	------------------------------------------------
	#   method to generate the smallest generated tree 
	#	of this graph
	#	------------------------------------------------
	#	paras:
	#		NULL
	def SGT_Floyd_Update(self):
		dist = self.dist_map.copy()
		path = self.neigh_map.copy()
		for i in range(dist.shape[0]):
			for j in range(dist.shape[0]):
				for k in range(dist.shape[0]):
					#	avoid fake shortest path
					if dist[i][j] + dist[j][k] < dist[i][k]:
						dist[i][k] = dist[i][j] + dist[j][k]
						path[i][k] = path[j][k]
		return dist, path
	
	#	Single Source Shortest Path
	#	Algorithm of Floyd
	#	------------------------------------------------
	#	Feature:
	#		Find SSSP with a SGT struct
	#	method to get the shortest source for the 
	#	specific source node of this graph
	#	------------------------------------------------
	#	paras:
	#		node_src:	name(num) of the source node 
	#		node_dst:	name(num) of the destination node
	def SSSP_Floyd(self, node_src, node_dst):
		#	get the full path
		node_cur = node_dst
		temp_path = []
		while node_cur != node_src:
			temp_path.insert(0, int(self.path[node_src][node_cur]))
			node_cur = int(self.path[node_src][node_cur])
		temp_path.append(node_dst)
		print self.path[node_src][node_dst]
		return self.dist[node_src][node_dst], temp_path
							
if __name__ == '__main__':
	g = SinglePath("map_data.npy")
	print "The map size is:\n", g.map_size, "\nThe map of Guide is:\n", g.dist_map
	print "The generated path is:\n", g.neigh_map
	print "The dist matrix of the Guide is:\n", g.SGT_Floyd_Update()[0], "\n", g.SGT_Floyd_Update()[1]
	print "The distance from node 0 to node 1 is:\n", g.SSSP_Floyd(0,2)[0], "\nThe path is:\n", g.SSSP_Floyd(0,1)[1]