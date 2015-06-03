import socket
import json
import sys
from util import read_json, send_json, es_primo
import time

if __name__ == '__main__':

	if len(sys.argv) == 3:
		bufer = ''
		
		request = socket.socket(
			socket.AF_INET,
			socket.SOCK_STREAM
		)
		request.connect(
			(
				sys.argv[1],
				int(sys.argv[2])
			)
		)

		data, bufer = read_json(bufer, request)
		print (data)
		if not data['primos']:
			print ('\nCalculando primos')
			for i in range(data['ini'], data['fin']):
				if es_primo(i):
					print ("primo encontrado: {0}".format(i))
					data['primos'].append(i)
			send_json(
                data,
                request
            )
			print ("Primos enviados :)")

			data, bufer = read_json(bufer, request)

		if not data["semiprimos"]:
			print ('\nCalculando semiprimos')
			time.sleep(2)
		request.close()