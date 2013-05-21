#!/usr/bin/env python2
# Python interface to cgminer's API


import json
import socket
import time
import pprint
import sys


def api_request (command, host='127.0.0.1', port=4028):
	s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)

	try:
		s.connect ((host, port))
		s.send ('{"command": "%s"}' % command)

		response = ""
		start = time.clock ()

		while True:
			data = s.recv (2048)

			if data is not None:
				response += data

			if '\x00' in response:
				break

			if time.clock () - start > 1.0:
				return None
		s.close ()
	except socket.error, e:
		return None
	
	return json.loads (response[:response.find ('\x00')])


if __name__ == '__main__':
	pprint.PrettyPrinter ().pprint (api_request (sys.argv[1]))
