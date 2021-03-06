import json
import time

def ping(request):
    # print ("Send ping")
    # print (type(request))
    request.send(
        ' '.encode('UTF-8')
    )

def read_json(bufer, request):
    while True:
        # hace ping
        ping(request)
        # =========
        bufer += request.recv(1024).decode('UTF-8')
        # print ("recv: {0}".format(bufer))
        if bufer.find('}') > 0:
            break
        time.sleep(1)

    bufer = bufer.split('}')
    resp = bufer[0] + '}'
    bufer_resp = ''
    for i in range(1, len(bufer)):
        bufer_resp += bufer[i]
    # print ("resp: {0}".format(resp))
    # print ("bufer: {0}".format(bufer))
    resp = json.loads( resp.strip() )
    return resp, bufer_resp

def send_json(bufer, request):
    # print ("Enviando {0}".format(bufer))
    request.sendall(
        json.dumps( bufer ).encode('UTF-8')
    )

def return_rangos_primos(numero, n):
    distancia = int(numero / n)
    ultimo = 0
    rangos = []
    for x in range(0, n):
        json = {
            "asignado": False,
            "primos": [],
            "procesado": False,
        }
        numero -= distancia
        if x == 0:
            json["ini"] = 2
            json["fin"] = distancia
        elif x == (n-1):
            if numero != 0:
                json["ini"] = ultimo + 1
                json["fin"] = ultimo + distancia + numero
            else:
                json["ini"] = ultimo + 1
                json["fin"] = ultimo + distancia
        else:
            json["ini"] = ultimo + 1
            json["fin"] = ultimo + distancia
        ultimo = json["fin"] 
        rangos.append(json)
    return rangos
	 
def es_primo(num):
    cont = 0
    for i in range(1, num + 1):
        if num % i == 0:
            cont += 1

    if cont == 2:
        return True
    else:
        return False

def return_rangos_semiprimos(primos, limite, n):
    primos_all = primos
    menor = primos[0]
    mayor = 0
    for x,num in enumerate(primos[1:]):
        if num*menor > limite:
            mayor = x+1
            break
    
    primos = primos[:mayor]
    ultimo = primos[mayor-1]
    rangos = []
    salto = n
    for x in range(0,n):
        json = {}
        json["ini"] = primos[::salto]
        json["primos_all"] = primos_all
        json["semiprimos"] = []
        json["limite"] = limite
        json["asignado"] = False
        
        for num in primos[::salto]:
            primos.remove(num)
        salto -= 1

        rangos.append(json)
    return rangos

def calcular_semiprimos(semiprimos_json):
    primos = semiprimos_json["primos_all"]
    ini = semiprimos_json["ini"]
    limite = semiprimos_json["limite"]

    semiprimos = []
    for num in ini:
        for x in primos[primos.index(num):]:
            if num * x <= limite:
                semiprimos.append(num * x)
    return semiprimos
