#!/usr/bin/env python
#coding: utf-8
# vim :set ts=4 sw=4 sts=4 et :

from bottle import route, run, static_file, request ,abort, redirect
from bottle_sqlite import SQLitePlugin

from sqlite3 import OperationalError

from base62 import base62_encode, base62_decode
from hashlib import md5
from url_uniq import url_uniq

#MAX = 62 ** 5
MAX = 916132832

def hashto62(url):
	m = md5()
	m.update(url)
	return int(m.hexdigest(), 16) % MAX

sqlite_plugin = SQLitePlugin(dbfile='url.db')

@route('/')
def index():
    return static_file('taobb.html', root='.')

@route('/favicon.ico')
def notfound():
    abort(404, "NOT FOUND")

@route('/<key>', apply=[sqlite_plugin])
def url(key, db):
    if len(request.query) == 0 and len(key) >= 5:
        code = base62_decode(key[:5])
        try:
	    c = db.execute("SELECT `url` FROM `urls` WHERE id = ?", ( code, ))
	    row = c.fetchone()
	    if row:
	        redirect(row['url'])
	except OperationalError:
	    pass

    redirect('/')


@route('/d/save', method='POST', apply=[sqlite_plugin])
def action(db):
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

if __name__ == '__main__':
    run(host='localhost', port=8008)
