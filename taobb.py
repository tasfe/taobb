#!/usr/bin/env python
#coding: utf-8

import string,cgi,time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from urlparse import parse_qs
from urllib import unquote 
import json

from urlkeys import base62_encode as tokey
from urlkeys import base62_decode as fromkey
from urluni import url_uni
from hash import hash
import urldb

html = open('taobb.html').read()

class MyHandler(BaseHTTPRequestHandler):
	
	def err(self):
		self.send_response(302)
		self.send_header('Location','/')
		self.end_headers()
		
	def do_HEAD(self):
		self.do_GET()

	def do_POST(self):
		self.do_GET()

	def do_GET(self):
		try:
			path = self.path.lstrip(' /')
			url = ''
			key = ''
			err = ''

			path = path.split('?')

			if len(path[0]) == 5:
				url = urldb.fromdb(fromkey(path[0]))
				if url:
					self.send_response(302)
					self.send_header('Location', url)
					self.end_headers()
					return

			elif path[0] !='':
				self.err()	
			elif len(path) > 1 :
				query = parse_qs(path[1])
				if query.has_key('url'):
					url = unquote(query['url'][0])
					url = url
					url = url_uni(url)
					if url:
						urldb.todb(hash(url), url)
						key = tokey(hash(url))
					else:
						err = '非法的URL'	
			else:
				pass

			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()

			if key != '' or err != '':
				self.wfile.write(json.dumps({"key":key, "err":err}))
			else:
				self.wfile.write(html)

			return
		except Exception as e:
			print e
			self.err()	



def main():
	try:
		server = HTTPServer(('', 8008), MyHandler)
		print 'ok...'
		server.serve_forever()
	except KeyboardInterrupt:
		server.socket.close()

if __name__ == '__main__':
	main()

