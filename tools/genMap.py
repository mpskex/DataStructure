#!/usr/bin/python
#   coding: utf-8

#	mpsk
#	Beijing University of Technology
#	Copyright 2017

import os
import numpy as np

INFINITE = 9999

def main():
	print "Please input the size of map data:"
	size = int(raw_input())
	print "size of the data is :", size
	print "Please input data with space between them"
	i = 1
	array = np.zeros((size, size), np.uint16)
	array.fill(INFINITE)
	for n in range(size-1):
		string = raw_input()
		array_row = string.split(' ')
		if len(array_row) != size - i:
			print "Mismatch in size of matrix"
			return -1
		array[n][n] = 0
		for m in range(i, size):
			if array_row[m-i]!="n":
				array[n][m] = array_row[m-i]
				array[m][n] = array_row[m-i]
		i += 1
	array[size-1][size-1] = 0
	map_data = array
	np.save("map_data", array)
	print map_data
	print "Loaded Map is "
	print np.load("map_data.npy")
	return 0

if __name__ == '__main__':
	main()