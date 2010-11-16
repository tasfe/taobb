import urllib2

BLACK_LIST = (
	'http://sinaurl.cn',
	'http://url.cn',
	'http://goo.gl',
	'http://bit.ly',
	'http://snipr.com',
	'http://chilp.it',
	'http://bit.ly',
	'http://short.to',
	'http://tr.im',
	'http://twurl.nl',
	'http://buk.me',
	'http://fon.gs',
	'http://ub0.cc',
	'http://fwd4.me',
	'http://xr.com',
	'http://short.ie',
	'http://sandbox.com',
	'http://burnurl.com',
	'http://digg.com',
	'http://a.gd',
	'http://hurl.ws',
	'http://snurl.com',
	'http://kl.am',
	'http://to.ly',
	'http://hex.io',
	'http://budurl.com',
	'http://cli.gs',
	'http://urlborg.com',
	'http://is.gd',
	'http://sn.im',
	'http://ur1.ca',
	'http://tweetburner.com',
	'http://x.bb',
	'http://tinyurl.com',
	'http://snipurl.com',
)


class HeadRequest(urllib2.Request):
	def get_method(self):
		return "HEAD"

def head(url):
	""" from https://github.com/joshthecoder/shorty-python/blob/master/shorty.py """
	class StopRedirectHandler(urllib2.HTTPRedirectHandler):
		def http_error_301(self, req, fp, code, smg, headers):
			return None
		def http_error_302(self, req, fp, code, smg, headers):
			return None
	o = urllib2.build_opener(StopRedirectHandler())
	try:
		o.open(url)
	except urllib2.HTTPError as e:
		if e.code == 301 or e.code == 302:
			return e.headers['Location']
	return url

def real_url(url):
	if url.startswith(BLACK_LIST):
		return real_url(head(url))
	else:
		return url

