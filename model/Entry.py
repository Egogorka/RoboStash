# from interfaces.IEntry import IEntry
# problems of defining interface for Entry

from model.UserAgents import UserAgents

class Entry:
	"""
		tuple[0] — The IP address of the client that sent the request to the server\n
		tuple[1] — The remote name of the user making the request\n
		tuple[2] — ID of the user making the request\n
		tuple[3] — Date of request\n
		tuple[4] — Request time\n
		tuple[5] — UTC time zone\n
		tuple[6] — Request type: (GET, POST, PUT, DELETE) that the server received\n
		tuple[7] — The API of the website the request pertains to\n
		tuple[8] — The protocol used to connect to the server and its version\n
		tuple[9] — The status code that the server returned for the request\n
		tuple[10] — The amount of data in bytes sent back to the client\n
		tuple[11] — Sources from which the user was directed to the current website (referrer)\n
		tuple[12] — User agent string (UA-string), contains information about the browser and host device\n
		tuple[13] — The response time it took for the server to serve the request\n
	"""

	def __init__(self, *args):
		self.ip = args[0]
		self.remote_name = args[1]
		self.user_id = args[2]
		self.date = args[3]
		self.request_time = args[4]
		self.time_zone = args[5]
		self.request_type = args[6]
		self.api = args[7]
		self.protocol = args[8]
		self.status_code = args[9]
		self.bytes_amount = args[10]
		self.sources = args[11]
		self.ua_string_raw = args[12]
		self.response_time = args[13]
		self.all = args
		# self.validate()
		self.ua = None

	def set_ua(self, ua: UserAgents):
		self.ua = ua
		return self

	# def validate(self) -> bool:
	# 	pass

	def __repr__(self):
		return str(self.all)
