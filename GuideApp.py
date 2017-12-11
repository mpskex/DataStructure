#!/usr/bin/python
#coding: utf-8

#	mpsk
#	Beijing University of Technology
#	Copyright 2017

#   POST TYPE
#       node type:   keynode/waynode
#       node name:  <nodenum>
#       cost limit: <costlimit>
#       &type=keynode&node=1

import sqlite3
from flask import Flask, request, url_for, render_template, make_response
from flask import abort, redirect
from package import *

#   Global Variable
DATABASE = 'database.db'

#   Initialize the objects
app = Flask(__name__)
mp = MultiPath.MultiPath(
        ["map/walk_map.npy", 
        "map/bike_map.npy", 
        "map/car_map.npy"])

#	The coordinates is for
#	generating the path using svg
point_cord=[
	"491 99",
    "418 412",
    "377 139",
    "329 305",
    "331 493",
    "243 355",
    "420 540",
    "712 428",
    "495 515",
	"416 250",
	"461 240",
	"361 426",
	"475 429",
	"606 389",
	"331 245"
	]
#	The name is for 
# 	string in sidebar
point_name=[
    u'宿舍',
    u'美食园',
    u'图书馆',
    u'逸夫图书馆',
    u'科学楼',
    u'信息楼',
    u'人文楼',
    u'软件楼',
    u'奥运场馆',
	u'三教'
	]
node_str = []
path_str = ""
begin_node = ''

@app.route('/')
@app.route('/index', methods = ['POST', 'GET'])
def index():
	"""
	Index
	"""
	if request.method == 'GET':
		s = ""
		for n in node_str:
			s += n[1]
		return render_template('index.html', nodes=s)
	else:
		return make_response('Error')

@app.route('/remove', methods = ['POST'])
def Remove():
	"""
	Remove single point
	"""
	if request.method == 'POST':
		num = request.form.get('node_num_r')
		if not mp.RemovePoint(int(num)):
			if len(node_str)>1:
				abort(503)
		print "[!]\tCleared ", num, " node"
		for n in range(len(node_str)):
			if node_str[n][0] == num:
				del node_str[n]
				#	注意要break！不然range会超
				break
		s = ""
		for n in node_str:
			s += n[1]
		print node_str
		return redirect(url_for('index'))

@app.route('/showpath', methods = ['POST'])
def ShowPath():
	"""
	Calculate & show the path
	"""
	if len(node_str)>1:
		depth = request.form.get('path_depth')
		print "[*]\tpath depth is \t", depth
		print "[*]\tnodes\t\n", "\tkeypoints: ",mp.keypoints, "\n\twaypoints: ",mp.waypoints 
		print "[*]\tstart with node ", node_str[0][0]
		mp.PrintStatus()
		if len(node_str)<=1:
			abort(505)
		k, outflag = mp.CalcMultiPath(int(node_str[0][0]), int(depth))
		if k == False or k == None:
			abort(505)
		print "[*]\tpath is :", k
		ns = ""
		for n in node_str:
			ns += n[1]
		ps = ""
		for n in k:
			ps += PathToHtml(n[0], n[1], u'green')
		#	judge whether the procedure 
		#	trigger the "out of limit" flag
		if outflag:
			return render_template('showpath.html', nodes=ns, path=ps, TipsFlag="")
		else:
			#	if the flag is not on
			#	the hide the tip
			return render_template('showpath.html', nodes=ns, path=ps, TipsFlag="hidden")
	else:
		abort(502)

@app.route('/removeall', methods = ['GET'])
def RemoveAll():
	"""
	Clean all
	"""
	mp.RemovePoints()
	node_str[:]=[]
	print "[!]\tCleared all points"
	return redirect(url_for('index'))

@app.route('/addpoint', methods = ['POST','GET'])
def AddWayPoint():
	"""
	Add a point (keypoint/waypoint)
	"""
	if request.method == 'POST':
		#	get the post data
		node_num = request.form.get('node_num')
		node_type = request.form.get('node_type')
		node_trans = request.form.get('node_trans')
		cost_limit = request.form.get('cost_limit')
		#	print it
		print "[*]\tRecieved Post"
		print "\tPosted Node Number is : ", request.form.get('node_num')
		print "\tPosted Node Transport is : ", request.form.get('node_trans')
		print "\tPosted Node Cost Limit is : ", request.form.get('cost_limit')
		if not (node_num.isdigit() and cost_limit.isdigit()):
			#	invalid post
			abort(501)
		if len(node_str)==0:
			#	treat the first node as start node
			print "[*]\tNote\tThe first seen node will be the begin node!"
			begin_node = node_num
			print "[*]\tNote\t Begin with node ", begin_node
			#if mp.AddKeyPoint(int(node_num), 9999, _type_=int(node_trans)):
				#print "[!!]\tFailed to create dst node!\t[!!]"
			node_str.append((node_num, PointToHtml(int(node_num), u'begin', int(node_trans), cost_limit)))
			return redirect(url_for('index'))
		if node_type == 'keynode':
			node_num = request.form.get('node_num')
			cost_limit = request.form.get('cost_limit')
			if mp.AddKeyPoint(int(node_num), int(cost_limit), _type_=int(node_trans)):
				print "Add Key Node ", node_num, " cost limit: ", cost_limit
				node_str.append((node_num, PointToHtml(int(node_num), node_type, int(node_trans), cost_limit)))
				return redirect(url_for('index'))
			else:
				abort(501)
		elif node_type == 'waynode':
			node_num = request.form.get('node_num')
			if mp.AddWayPoint(int(node_num)):
				print "Add Way Node ", node_num
				resp = make_response(render_template('index.html'))
				node_str.append((node_num, PointToHtml(int(node_num), node_type, int(node_trans), 0)))
				return redirect(url_for('index'))
			else:
				abort(501)
		else:
			abort(502)
	else:
		return redirect(url_for('index'))

@app.route('/papers', methods = ['POST','GET'])
def papers():
	return render_template('paper.html')

@app.route('/help', methods = ['POST','GET'])
def help():
	return render_template('help.html')

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
	return render_template('error.html', resp_code='501', error_message=u'创建路径点失败>_<', \
	reason=u'可能是您输入重复～请您检查输入后再试'), 501

@app.errorhandler(502)
def internal_error(error):
	return render_template('error.html', resp_code='502', error_message=u'输入不完整>_<'), 502

@app.errorhandler(503)
def internal_error(error):
	return render_template('error.html', resp_code='503', error_message=u'无法删除您请求的路径点>_<'), 503

@app.errorhandler(505)
def internal_error(error):
	return render_template('error.html', resp_code='505', error_message=u'未知内部错误!>_<'), 505

def connect_db():
	return sqlite3.connect(DATABASE)

def PointToHtml(num, typ, trans, limit):
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
		s += u'&nbsp'
		if trans== 0:
			s += u'出行方式：走路'
		elif trans == 1:
			s += u'出行方式：自行车'
		elif trans == 2:
			s += u'出行方式：自驾车'
		else:
			return False
	elif typ==u'waynode':
		s += u'普通路径点'
		s += u'<br>'
		s += u'限制: 无'
		s += u'&nbsp'
		if trans== 0:
			s += u'出行方式：走路'
		elif trans == 1:
			s += u'出行方式：自行车'
		elif trans == 2:
			s += u'出行方式：自驾车'
		else:
			return False
	elif typ==u'begin':
		s += u'起点'
		s += u'<br>'
		s += u'限制：无'
		s += u'&nbsp'
		if trans== 0:
			s += u'出行方式：走路'
		elif trans == 1:
			s += u'出行方式：自行车'
		elif trans == 2:
			s += u'出行方式：自驾车'
		else:
			return False
	else:
		return False
	s += u'</div>'
	return s

def PathToHtml(n_a, n_b, color):
	s = u'<path d="M'
	s += point_cord[n_a]
	s += u' '
	s += point_cord[n_b]
	s += u'"style="fill:transparent;stroke:'
	s += color
	s += u';stroke-width:4;filter:url(#Gaussian_Blur)"/>'
	return s

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
