#!/usr/bin/python
#coding: utf-8

#	mpsk
#	Beijing University of Technology
#	Copyright 2017

import sqlite3
from flask import Flask, request, url_for, render_template, make_response
from package import *

#   Global Variable
DATABASE = 'database.db'

#   Initialize the objects
app = Flask(__name__)
mp = MultiPath.MultiPath("map/map_data.npy")

#url_for('static', filename='style.css')

#   POST TYPE
#       node type:   keynode/waynode
#       node name:  <nodenum>
#       cost limit: <costlimit>
#       &type=keynode&node=1

@app.route('/')
@app.route('/index', methods = ['POST', 'GET'])
def helloworld():
    if request.method == "GET":
        return render_template('index.html')
    else:
        print "wrong method"
        return make_response('Error')

@app.route('/addpoint', methods = ['POST'])
def AddWayPoint():
    node_type = request.form.get('node_type')
    if node_type == 'keynode':
        node_num = request.form.get('node_num')
        cost_limit = request.form.get('cost_limit')
        mp.AddKeyPoint(int(node_num), int(cost_limit))
        print "Add Key Node ", node_num, " cost limit: ", cost_limit
        resp = make_response(render_template('index.html'))
        return resp
    elif node_type == 'waynode':
        node_num = request.form.get('node_num')
        mp.AddWayPoint(int(node_num))
        print "Add Way Node ", node_num
        resp = make_response(render_template('index.html'))
        return resp
    else:
        return make_response(render_template('error.html'))

def connect_db():
    return sqlite3.connect(DATABASE)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)