#!/usr/bin/env python
#coding: utf-8

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from urlparse import parse_qs
from urllib import unquote 
import json

from urlkeys import base62_encode as tokey
from urlkeys import base62_decode as fromkey
from urluni import url_uni
from urlhash import url_hash
from urldb import todb as url_to_db
from urldb import fromdb as url_from_db
from short_rewriter import real_url

html = open('taobb.html').read()

class TaobbHandler(BaseHTTPRequestHandler):
	
	def head(self):
		try:
			path = self.path.lstrip(' /')
			key = ''
			err = ''

			path = path.split('?')

			p = path[0].strip(' /')
			if len(p) > 0:
				return self.goto(url_from_db(fromkey(p)) or '/')	

			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()

			if len(path) > 1 :
				query = parse_qs(path[1])
				if query.has_key('url'):
					url = url_uni(unquote(query['url'][0]))
					if url:
						# 短路自己
						if url.startswith('http://tao.bb'):
							key = url[14:][:5] + ' '
						else:
							url = real_url(url)
							key = tokey(url_to_db(url_hash(url), url))
					else:
						err = '非法的URL'	

					return json.dumps({"key":key, "err":err});

		except Exception:
			return self.goto('/')	

	def goto(self, url):
		self.send_response(302)
		self.send_header('Location', url)
		self.end_headers()
		
	def do_HEAD(self):
		self.head()

	def do_POST(self):
		self.do_GET()

	def do_GET(self):
		self.wfile.write(self.head() or html)


def main():
	try:
		server = HTTPServer(('127.0.0.1', 8008), TaobbHandler)
		print 'Tao.bb ok ...'
		server.serve_forever()
	except KeyboardInterrupt:
		server.socket.close()

if __name__ == '__main__':
	main()

