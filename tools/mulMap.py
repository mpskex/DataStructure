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
	_out = np.zeros(_in.shape)
	print "Loaded!"
	print _in
	print "input a float"
	_c = float(raw_input())
	print "Multipyl by ", _c, " type", type(_c)
	for n in range(_in.shape[0]):
		for m in range(_in.shape[1]):
			if _in[m][n] != 9999:
				_out[m][n] = _c * _in[m][n]
			else:
				_out[m][n] = _in[m][n]
	print _out
	np.save("../map/" + _file, _out)
	return 0

if __name__ == '__main__':
	main()