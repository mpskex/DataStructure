#!/usr/bin/python
#coding: utf-8

#	mpsk
#	Beijing University of Technology
#	Copyright 2017

import sqlite3
from flask import Flask, request, url_for, render_template, make_response
from flask import abort, redirect
from package import *

#   Global Variable
DATABASE = 'database.db'

#   Initialize the objects
app = Flask(__name__)
mp = MultiPath.MultiPath("map/map_data.npy")
point_name=[u'宿舍', u'礼堂', u'图书馆']
node_str = []

#url_for('static', filename='style.css')

#   POST TYPE
#       node type:   keynode/waynode
#       node name:  <nodenum>
#       cost limit: <costlimit>
#       &type=keynode&node=1

@app.route('/')
@app.route('/index', methods = ['POST', 'GET'])
def index():
	if request.method == "GET":
		s = ""
		for n in node_str:
			s += n[1]
		return render_template('index.html', nodes=s)
	else:
		print "wrong method"
		return make_response('Error')

@app.route('/removeall', methods = ['GET'])
def RemoveAll():
	mp.RemovePoints()
	node_str=[]
	print "[!]Cleared all points"
	s = ""
	for n in node_str:
		s += n[1]
	return render_template('index.html', nodes=s)

@app.route('/addpoint', methods = ['POST'])
def AddWayPoint():
	node_type = request.form.get('node_type')
	print "[*]Recieved Post"
	print "\tPosted Node Number is : ", request.form.get('node_num')
	print "\tPosted Node Cost Limit is : ", request.form.get('cost_limit')
	if node_type == 'keynode':
		node_num = request.form.get('node_num')
		cost_limit = request.form.get('cost_limit')
		if not (node_num.isdigit() and cost_limit.isdigit()):
			abort(501)
		if mp.AddKeyPoint(int(node_num), int(cost_limit)):
			print "Add Key Node ", node_num, " cost limit: ", cost_limit
			node_str.append((node_num, PointToHtml(int(node_num), node_type, cost_limit)))
			s = ""
			for n in node_str:
				s += n[1]
			return render_template('index.html', nodes=s)
		else:
			abort(501)
	elif node_type == 'waynode':
		node_num = request.form.get('node_num')
		if not node_num.isdigit():
			abort(501)
		if mp.AddWayPoint(int(node_num)):
			print "Add Way Node ", node_num
			resp = make_response(render_template('index.html'))
			node_str.append((node_num, PointToHtml(int(node_num), node_type, 0)))
			s = ""
			for n in node_str:
				s += n[1]
			return render_template('index.html', nodes=s)
		else:
			abort(501)
	else:
		abort(502)

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/test')
def test():
	return render_template('test.html')

@app.errorhandler(400)
def page_not_found(error):
	return render_template('error.html', resp)

@app.errorhandler(501)
def internal_error(error):
	return render_template('error.html', resp_code='501', error_message="Failed to create the point!!>_<", \
	reason='perhaps you input the point repeatly!'), 501

@app.errorhandler(502)
def internal_error(error):
	return render_template('error.html', resp_code='502', error_message="Incomplete input!!>_<"), 502

def connect_db():
	return sqlite3.connect(DATABASE)

def PointToHtml(num, typ, limit):
	s = u'<div class="sidebar_element" style="font-size:12px">'
	if num>=len(point_name):
		s += u'未知'
	else:
		s += point_name[num]
	s += u','
	if typ==u'keynode':
		s += u'带时间限制的路径点'
		s += u'<br>'
		s += u'限制：'
		s += str(limit)
	elif typ==u'waynode':
		s += u'普通路径点'
		s += u'<br>'
		s += u'限制: 无'
	else:
		return False
	s += u'</div>'
	return s
	

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=True, threaded=True)