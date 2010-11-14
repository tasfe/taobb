#!/usr/bin/env python

from urlparse import urlsplit
from urlparse import parse_qsl
import re

httpre = re.compile("https?:\/\/", re.IGNORECASE)
#portre = re.compile(":\d+")

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
		netloc = netloc[:-3] if netloc.endswith(':80') else netloc
		path = netloc.lower() + re.sub('/+','/',url.path)
	else:
		return None


	query = parse_qsl(url.query, True)
	query.sort()
	query = '&'.join((i[0]+'='+i[1]).rstrip('=') for i in query)

	fragment = url.fragment

	return ('%s://%s?%s#%s' % (scheme, path, query, fragment)).rstrip('?# ')
