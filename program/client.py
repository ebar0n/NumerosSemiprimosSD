import socket
import json
import sys
from util import read_json, send_json, es_primo, calcular_semiprimos
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

		while True:
			data, bufer = read_json(bufer, request)
			print (data)
			if 'primos' in data:
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

			if 'semiprimos' in data:
				if not data["semiprimos"]:
					print ('\nCalculando semiprimos')
					data["semiprimos"] = calcular_semiprimos(data)
					send_json(
		                data,
		                request
		            )
					time.sleep(2)
		request.close()