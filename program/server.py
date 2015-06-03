import socketserver
import threading
import time
import sys
from util import read_json, send_json, return_rangos_primos, \
                 ping, return_rangos_semiprimos

global coun_connections
coun_connections = 0
global json_primos
json_primos = {}
global json_semiprimos
json_semiprimos = {
    'primos': []
}

global json_semiprimos_rangos
json_semiprimos_rangos = {
    'primos': []
}

class MyTCPServer(
    socketserver.ThreadingMixIn,
    socketserver.TCPServer):
    pass

class MyTCPServerHandler(socketserver.BaseRequestHandler):

    bufer = ''

    def display_coun_connections(self, num):
        global coun_connections
        coun_connections += num
        if num == 1:
            print ('\nCliente ADD')
        else:
            print ('\nCliente DEL')
        print ('Total {0}'.format(coun_connections))

    def handle(self):
        
        cur_thread = threading.current_thread()
        self.name = cur_thread.name
        self.display_coun_connections(1)
        
        try:
            global json_primos
            global json_semiprimos
            while True:
                if json_primos:
                    for rango in json_primos:
                        if not rango['asignado']:
                            self.rango = rango
                            self.rango['asignado'] = True
                            
                            send_json(
                                self.rango,
                                self.request
                            )
                            print ('Rango de primos asignado: {0}'.format(self.rango))
                            break
                    band = True
                    if hasattr(self, "rango"):
                        while True:
                            print ("Esperando resp")
                            data, bufer = read_json(
                                self.bufer, self.request
                            )
                            
                            if data:
                                # obteniendo resp de los primos
                                self.rango['primos'] = data['primos']
                                print ("Rango de primos encontrados: {0}".format(self.rango))

                                band = True
                                for rango in json_primos:
                                    if rango['primos']:
                                        if rango["procesado"] is False:
                                            json_semiprimos["primos"] += rango['primos']
                                            rango["procesado"] = True
                                    else:
                                        band = False

                                if band is False:
                                    for rango in json_primos:
                                        if not rango['asignado']:
                                            self.rango = rango
                                            self.rango['asignado'] = True
                                            
                                            send_json(
                                                self.rango,
                                                self.request
                                            )
                                            print ('Rango de primos asignado: {0}'.format(self.rango))
                                            break
                                else:
                                    break
                            time.sleep(2)
                    break
                else:
                    ping(self.request)
                    time.sleep(2)

            # Repartir carga de semiprimos
            print ("\n\nCalcular semiprimos")

            global json_semiprimos_rangos
            while True:
                if json_semiprimos_rangos:
                    for rango in json_semiprimos_rangos:
                        if not rango['asignado']:
                            self.rango = rango
                            self.rango['asignado'] = True
                            
                            send_json(
                                self.rango,
                                self.request
                            )
                            print ('Rango de primos asignado: {0}'.format(self.rango))

                            print ("Esperando semiprimos")
                            data, bufer = read_json(
                                self.bufer, self.request
                            )
                            print (data["semiprimos"])
                time.sleep(2)
            
        except Exception as e:
            #print('Exception wile receiving message: ', e)
            pass
            
        if hasattr(self, "rango"):
            if 'primos' in self.rango:
                if not self.rango["primos"]:
                    self.rango['asignado'] = False
                    print ("El rango: {0} sera reasignado".format(self.rango))
            if 'semiprimos' in self.rango:
                if not self.rango["semiprimos"]:
                    self.rango['asignado'] = False
                    print ("El rango: {0} sera reasignado".format(self.rango))

    def finish(self):
        self.display_coun_connections(-1)
        
if __name__ == '__main__':

    try:
        if len(sys.argv) == 2:
            server = MyTCPServer(
                ('0.0.0.0', int(sys.argv[1])),
                MyTCPServerHandler
            )
            server_thread = threading.Thread(
                target=server.serve_forever
            )
            
            server_thread.daemon = True
            server_thread.start()

            limite = int(input('Introduzca limite de semiprimos a calcular: '))
            while True:
                if coun_connections < 1:
                    print ('\nEsperando clientes...')
                    time.sleep(3)
                else:
                    break

            print ('\n{0} Clientes activos'.format(coun_connections))
            
            json_primos = return_rangos_primos(
                limite,
                coun_connections
            )

            while True:
                if coun_connections < 1:
                    print ('\nEsperando clientes...')
                    time.sleep(3)
                else:
                    break

            while True:
                if json_semiprimos["primos"]:

                    band = True
                    for rango in json_primos:
                        if not rango['primos']:
                            band = False

                    if band:
                        json_semiprimos["primos"].sort()
                        print ("\nPrimos calculados {0}".format(json_semiprimos["primos"]))

                        json_semiprimos_rangos = return_rangos_semiprimos(
                            json_semiprimos["primos"],
                            limite,
                            coun_connections,
                        )
                        
                        print ("\nRangos para calcular semiprimos {0}".format(json_semiprimos_rangos))
                        break
                time.sleep(3)

            print ("\nEsperando semiprimos:")
            while True:
                time.sleep(1)

    except KeyboardInterrupt:
        print ('Cierre todos los clientes conectado...')
        server.shutdown()