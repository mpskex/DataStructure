#   coding: utf-8

#	mpsk
#	Beijing University of Technology
#	Copyright 2017

import os
import numpy as np

INFINITE = 9999

def main():
	print "==	Multiply map by constant =="
	print "File to be load:"
	_file = raw_input()
	_in = np.load("../map/" + _file)
	print "Loaded!"
	print _in
	return 0

if __name__ == '__main__':
	main()