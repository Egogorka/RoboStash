from interfaces.IParser import IParser, IEntry
from typing import List

from model.Entry import Entry


class ParserPlug(IParser):

	def parse(self, path: str) -> List[IEntry]:
		print("Plugging your pipes hehe")
		return [
			Entry(
				'15.74.45.114', '-', '-', '2023-01-05', '00:00:03', '+0300', 'DELETE', '/usr/admin',
				'HTTP/1.0', '304', '5016', '-',
				'Mozilla/5.0 (Linux; Android 10; ONEPLUS A6000) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36',
				'4533'
			),
			Entry(
				'122.239.116.246', '-', '-', '2023-01-05', '00:00:05', '+0300', 'GET', '/usr/login', 'HTTP/1.0', '200',
				'4973', 'http://www.gonzalez.info/explore/explorehome.jsp',
				'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
				'3144'
			),
			Entry(
				'139.31.190.36', '-', '-', '2023-01-05', '00:00:10', '+0300', 'GET', '/usr/admin/developer',
				'HTTP/1.0', '403', '5087', '-',
				'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
				'4437'
			),
			Entry(
				'196.241.201.130', '-', '-', '2023-01-05', '00:00:12', '+0300', 'PUT', '/usr/admin/developer',
				'HTTP/1.0', '404', '4989', 'http://www.gonzalez.info/explore/explorehome.jsp',
				'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
				'4445'
			)
		]