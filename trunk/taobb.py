#!/usr/bin/env python
#coding: utf-8
# vim :set ts=4 sw=4 sts=4 et :

import sys
from bottle import route, run, static_file, request ,abort, redirect, response, error
from bottle_sqlite import SQLitePlugin

from sqlite3 import OperationalError

from base62 import base62_encode, base62_decode
from hashlib import md5
from url_uniq import url_uniq

from qrcode import make as makeqrcode
from StringIO import StringIO
from short_rewriter import real_url

#MAX = 62 ** 5
MAX = 916132832

def hashto62(url):
	m = md5()
	m.update(url)
	return int(m.hexdigest(), 16) % MAX

sqlite_plugin = SQLitePlugin(dbfile='url.db')

@error(404)
@route('/')
def index(error = None):
    return static_file('taobb.html', root='.')

@route('/favicon.ico')
def notfound():
    redirect('http://www.taobao.com/favicon.ico', 302)

def realurl(key, db):
    try:
        code = base62_decode(key)
        c = db.execute("SELECT `url` FROM `urls` WHERE id = ?", ( code, ))
        row = c.fetchone()
        if row:
	    return row['url']
    except:
        pass
	

@route('/<key>', apply=[sqlite_plugin])
def url(key, db):
    if request.get_header('Host' , 'tao.bb') != 'tao.bb':
	abort(404, "NOT FOUND")

    key = key.strip('/')
    if len(request.query) == 0 and len(key) == 5:
        url = realurl(key, db)
	if url:
	    redirect(url)

    abort(404, "NOT FOUND")


@route('/<key>/real', apply=[sqlite_plugin])
def qrcode(key, db):
    if len(request.query) == 0 and len(key) == 5:
        url = realurl(key, db)
	if url:
	    return url + "\n"

    abort(404, "NOT FOUND")

@route('/<key>/qrcode', apply=[sqlite_plugin])
@route('/<key>/qrcode.png', apply=[sqlite_plugin])
def qrcode(key, db):
    if len(request.query) == 0 and len(key) == 5:
        url = realurl(key, db)
	if url:
	    response.content_type = 'image/png'
	    img = makeqrcode(url)
	    output = StringIO()
	    img.save(output,'PNG')
	    contents = output.getvalue()
	    output.close()
	    return contents
	
    abort(404, "NOT FOUND")

@route('/d/save', method='POST', apply=[sqlite_plugin])
def save(db):
    key = None
    err = None

    url = request.forms['url']
    if url:
        url = url_uniq(url)
        if url:
	    code = hashto62(url)
	    try:
	        db.execute("REPLACE INTO `urls` VALUES (?, ?,datetime())" , (code, url))
		key = base62_encode(code)
	    except OperationalError:
	        err = '内部错误'
        else:
	    err = '请输入有效的 URL'

    else:
        err = '请输入URL'

    return {'key':key, 'err':err }

@route('/d/long', method='POST')
def longurl():
    wanted = request.forms['url']
    longurl = None
    if wanted and len(wanted) < 25:
        if not wanted.startswith('http://'):
	    wanted = 'http://' + wanted
	
	#longurl = real_url(wanted)

    return { 'wanted':wanted,  'long': longurl}

if __name__ == '__main__':
    debug = False
    if len(sys.argv) > 0:
        debug = True
    run(host='localhost', port=8008, debug=debug)
