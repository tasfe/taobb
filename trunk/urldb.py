import sqlite3
import sys

conn = sqlite3.connect(sys.path[0] + '/url.db')
c = conn.cursor()

def fromdb(i):
	c.execute("select `url` from `urls` where id = %d" % i)
	url = c.fetchone()
	if url:
		url = url[0]
	return url

def todb(i, url):
	c.execute("""replace into `urls` values (%d,'%s',datetime())""" % (i, url))
	conn.commit()
	return i
