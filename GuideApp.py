#!/usr/bin/python
#coding: utf-8

#	mpsk
#	Beijing University of Technology
#	Copyright 2017

import sqlite3
from flask import Flask, request, url_for, render_template
from package import *


app = Flask(__name__)
DATABASE = 'database.db'

#url_for('static', filename='style.css')

@app.route('/')
@app.route('/index')
def helloworld():
    return render_template('index.html')
    
'''
@app.route('/VidToday')
def videos(vid_src='vid/Koe-no-Katachi_CNSub.mp4'):
    return render_template('VidToday.html', vid_src = url_for('static', filename=vid_src))
'''

def connect_db():
    return sqlite3.connect(DATABASE)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)