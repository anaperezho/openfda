import http.client
import json

SERVER = "api.fda.gov"
RESOURCE = "/drug/label.json"
limite = '?limit=10'
header = {'User-Agent': 'http-client'}
conexion = http.client.HTTPSConnection(SERVER)
conexion.request("GET", RESOURCE + limite, None, header)

datos10 = conexion.getresponse()
medicamentos = datos10.read().decode("utf-8")
conexion.close()

medicamentos_json = json.loads(medicamentos)
resultados = medicamentos_json['results']


paracliente = ""

for medicamento in resultados:
    openfda = medicamento['openfda']
    if openfda:
        brand_name = openfda['brand_name']
        brand_name = ','.join(brand_name)
        #print("Brand name: \n", openfda['brand_name'])

        substance_name = openfda['substance_name']
        substance_name = ','.join(substance_name)
        #print("Substance name: \n", openfda['substance_name'])

        paracliente = paracliente + brand_name + "\t" + substance_name + "\n"
    else:
        no_info = ("Informacion no disponible\n")
        paracliente = paracliente + no_info





import socket

IP = "0.0.0.0"
PORT = 8000
#numero maximo de peticiones
MAX_OPEN_REQUEST = 5

#definimos la funcion para el cliente
def paraelcliente(clientsocket):

    contenido = """

    <html>
    <h1>Brand name Substance name</h1>
    <pre> """ + paracliente + """
    </pre>
    </html>
    """
    # -- Indicamos primero que todo OK
    linea_inicial = "HTTP/1.1 200 OK\n"
    cabecera = "Content-Type: text/html\n"
    cabecera += "Content-Length: {}\n".format(len(str.encode(contenido)))
    #  Creamos el mensaje uniendo todas sus partes
    mensaje_respuesta = str.encode(linea_inicial + cabecera + "\n" + contenido)
    clientsocket.send(mensaje_respuesta)



serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((IP, PORT))
#le ponemos a escuchar
serversocket.listen(MAX_OPEN_REQUEST)

while True:
    print("Esperando cliente en IP", IP, " Puerto:", PORT)
    (clientsocket, addressclient) = serversocket.accept()
    print("Peticion recibida:", addressclient)
    #llamada a la funcion para el cliente
    paraelcliente(clientsocket)
    clientsocket.close()


