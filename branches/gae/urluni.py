#!/usr/bin/env python

from urlparse import urlsplit
from urlparse import parse_qsl
from urllib import urlencode
from urllib import quote
import re

httpre = re.compile("https?:\/\/", re.IGNORECASE)

def url_uni(url):
	url = url.strip()
	if not httpre.match(url):
		if url.find('://') > 0:
			return None
		else:
			url = 'http://' + url
		
	url = urlsplit(url)

	scheme = url.scheme

	netloc = url.netloc
	if netloc:

		try:
			port = url.port
			username = url.username
			password = url.password
			hostname = url.hostname.decode('utf-8').encode('idna')
		except:
			return None

		netloc = hostname
		if username or password:
			netloc = '@' + netloc	
			if password:
				netloc = ':' + password + netloc
			netloc = username + netloc

		if port:
			if scheme == 'http':
				port = '' if port == 80 else port
			elif scheme == 'https':
				port = '' if port == 443 else port
			netloc += ':' + str(port)
		
		path = netloc.lower() + re.sub('/+','/',url.path)
	else:
		return None


	query = parse_qsl(url.query, True)
	query.sort()
	query = urlencode(query)

	fragment = url.fragment

	return (('%s://%s?%s#%s' % (scheme, quote(path), query, quote(fragment))).rstrip('?#/ '))
