#!/usr/bin/python
#   coding: utf-8

import os
import numpy as np


def main():
	print "Please input the size of map data:"
	size = int(raw_input())
	print "size of the data is :", size
	print "Please input data with space between them"
	array = []
	for i in range(size):
		string = raw_input()
		array_row = string.split(' ')
		if len(array_row) != size:
			print "Mismatch in size of matrix"
			return -1
		for n in range(len(array_row)):
			array_row[n] = float(array_row[n])
		array.append(array_row)
	map_data = np.matrix(array)
	np.save("map_data", map_data)
	print map_data
	print np.load("map_data.npy")[0][0]
	return 0

if __name__ == '__main__':
	main()