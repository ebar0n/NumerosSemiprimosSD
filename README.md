# NumerosSemiprimosSD
Este sera un proyecto simple que busca calcular los números semiprimos menores o iguales a un numero dado, este calculo se hará de manera distribuida, servirá como aplicación cliente servidor,  debería iniciarse un servidor que se anunciara y n clientes podrán conectarse, una vez conectados el servidor podrá distribuir la carga de calculo entre todos los clientes conectados. se deben tomar las precauciones necesarias para evitar perdida de información y redistribución de trabajo cuando un cliente se desconecta.

#Ejecutar servidor
python3 program/server.py 5555

# Ejecutar cliente
python3 program/client.py 127.0.0.1 5555