from datetime import datetime
import urllib
import urllib2

class Payload:
        def __init__(self, url, host_id, keyboard_id, q_sheet, q_number, answer):
		self.url = url
                self.host_id = host_id
		self.keyboard_id = keyboard_id
                self.time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                self.q_sheet = q_sheet
		self.q_number = q_number
		self.answer = answer

	def send(self):
		try:
			params = {
					"host_id": self.host_id,
					"keyboard_id": self.keyboard_id,
					"time": self.time,
					"q_sheet": self.q_sheet,
					"q_number": self.q_number,
					"answer": self.answer
				}
		        data = urllib.urlencode(params)
		        req = urllib2.Request(self.url, data)
		        res = urllib2.urlopen(req)
              		r = res.read()
               		return r

		except:
			import traceback
			traceback.print_exc()
			return "data did not send"
			pass
