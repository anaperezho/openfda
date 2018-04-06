#importo las librerias http.client y json para conectarme a un servidor web y trabajar con archivos json
import http.client
import json
#constante del servidor y recurso que voy a utilizar
SERVER="api.fda.gov"
RESOURCE="/drug/label.json"
#especifico el navegador
header={'User-Agent':'http-client'}
#utilizo la libreria http.client para establecer la conexion
conexion=http.client.HTTPSConnection(SERVER)
#peticion tipo GET
conexion.request("GET",RESOURCE,None,header)
#almaceno todos los datos obetenidos en la variable datos y decodifico por si hay algun caracter que no puedo leer
datos=conexion.getresponse()
drug=datos.read().decode("utf-8")
#cierro la conexion
conexion.close()

#ordeno en diccionarios y listas
drug_json=json.loads(drug)
meta=drug_json['meta']
#accedo al diccionario mediante la clave results
resultados=drug_json['results'][0]


id=resultados['id']
print("Identificador:\n",id)

proposito=resultados['purpose']
print("Proposito del producto:\n",proposito)
#tengo que acceder antes al diccionario openfda
nombre=resultados['openfda']['manufacturer_name']
print("Nombre del fabricante:\n",nombre)


