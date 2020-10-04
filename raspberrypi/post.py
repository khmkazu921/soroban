import urllib
import urllib2


try:
	params = {
		"id": "12345",
		}
	url = "https://productive-rayon.glitch.me"
	data = urllib.urlencode(params)
	req = urllib2.Request(url, data)
	#req.add_header('Content-Type', 'application/x-www-form-urlencoded')
	with  urllib2.urlopen(req) as res:
		r = res.read()
		print(r)

except:
	import traceback
	traceback.print_exc()
	pass
