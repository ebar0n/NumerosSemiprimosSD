import socket
import json

data = {
	'messaje': 'Numero primos',
}

for i in range(0, 1000):
	data['{0}'.format(i)] = i

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 13373))
s.send(bytes(json.dumps(data), 'UTF-8'))

data = s.recv(2024).decode('UTF-8')

if data:
	result = json.loads( data )
	print(result)
else:
	print ("result: None")
s.close()
