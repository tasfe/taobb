import urllib2

BLACK_LIST = (
	'http://sinaurl.cn',
	'http://url.cn',
	'http://goo.gl',
	'http://bit.ly',
)


class HeadRequest(urllib2.Request):
	def get_method(self):
		return "HEAD"

def head(url):
	response = urllib2.urlopen(HeadRequest(url))
	print response.getcode()
	return response.geturl() if True else url

def real_url(url):
	if url.startswith(BLACK_LIST):
		return head(url)
	else:
		return url

