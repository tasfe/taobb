import sys
import hashlib

#MAX = 62 ** 5
MAX = 916132832

def url_hash(url):
	m = hashlib.md5()
	m.update(url)
	return int(m.hexdigest(), 16) % MAX

