from abc import ABC, abstractmethod

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


class IEntry(ABC):

	#  This approach makes big script files,
	#  probably needs to be reworked

	@property
	@abstractmethod
	def ip(self):
		pass

	@property
	@abstractmethod
	def remote_name(self):
		pass

	@property
	@abstractmethod
	def user_id(self):
		pass

	@property
	@abstractmethod
	def date(self):
		pass

	@property
	@abstractmethod
	def request_time(self):
		pass

	@property
	@abstractmethod
	def time_zone(self):
		pass

	@property
	@abstractmethod
	def request_type(self):
		pass

	@property
	@abstractmethod
	def api(self):
		pass

	@property
	@abstractmethod
	def protocol(self):
		pass

	@property
	@abstractmethod
	def status_code(self):
		pass

	@property
	@abstractmethod
	def bytes_amount(self):
		pass

	@property
	@abstractmethod
	def sources(self):
		pass

	# TODO probably needs UA as well
	@property
	@abstractmethod
	def ua_string_raw(self):
		pass

	@property
	@abstractmethod
	def response_time(self):
		pass

	@abstractmethod
	def __repr__(self):
		pass
