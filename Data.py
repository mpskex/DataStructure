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

#   This class is to storage the data
#   of the neighbour table
#   For a weighted graph G, every distance
#   is saved in the matrix M(i,j) for position
#   row i and column j
class MapGuide(object):

	#   the init proc is to create the 
	#   neighbour table with numpy
	#	------------------------------------------------
	#	paras:
	#       node_num:   number of node
	#		map_path:	path to map data
	def __init__(self, map_path):
		#	define the infinite value in storage structure
		self.INIFINITE = 9999
		#   first load the map data from file or database
		#   then copy each path distance to the path data
		self.dist_map = self.__LoadMap__(map_path)
		self.neigh_map = self.__GenPath__(self.dist_map)
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
				if map[i][j] ==self.INIFINITE:
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
		dist, path = self.SGT_Floyd_Update()
		
		return dist[node_src][node_dst]



	#	Single Source Shortest Path
	#	Algorithm of Dijstra
	#	------------------------------------------------
	#	Feature:
	#		node
	#	method to get the shortest source for the 
	#	specific source node of this graph
	#	------------------------------------------------
	#	paras:
	#		node_src:	name(num) of the source node 
	#		node_dst:	name(num) of the destination node
	def SSSP_Dijstra(self, node_src, node_dst):
		#	list contains the node which the routine passed
		path = []
		#	initiate the distance vector which storage the distances
		#	to the neigboured nodes
		dist_vec = []
		for i in range(self.dist_map.shape[0]):
			#	fill with infinite
			dist_vec.append(self.INIFINITE)
		dist_vec[node_src] = 0
		#	set the current node to source
		node_cur = node_src
		#	temp dist set to 0
		temp_dist = 0
		while(node_cur != node_dst):
			#	set min equals to infinite(pre-defined)
			min = self.INIFINITE
			#	set node_next to infinite
			node_next = self.INIFINITE
			#	for every neighbour of the node_cur
			#	Caculate the nearest node
			for i in range(self.dist_map.shape[1]):
				#	avoid self pointing zero distance
				if i != node_src:
					if dist_vec[i] == self.INIFINITE and self.dist_map[node_cur][i] != self.INIFINITE:
						dist_vec = self.dist_map[node_cur][i] + temp_dist
					else:
						#	nearest neighbour
						if self.dist_map[node_cur][i] + temp_dist >= dist_vec[i]:
							#	set the distance to vector
							dist_vec[i] = self.dist_map[node_cur][i] + temp_dist
							
		
						
			
		
		

if __name__ == '__main__':
	g = MapGuide("map_data.npy")
	print "The map of Guide is:\n", g.dist_map
	print "The generated path is:\n", g.neigh_map
	print "The dist matrix of the Guide is:\n", g.SGT_Floyd_Update()[0], "\n", g.SGT_Floyd_Update()[1]
	print "The distance from node 0 to node 3 is:\n", g.SSSP_Floyd(0,3)