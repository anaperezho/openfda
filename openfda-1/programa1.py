import http.client
import json

SERVER="api.fda.gov"
RESOURCE="/drug/label.json"
header={'User-Agent':'http-client'}
conexion=http.client.HTTPSConnection(SERVER)
conexion.request("GET",RESOURCE,None,header)

datos=conexion.getresponse()
drug=datos.read().decode("utf-8")
conexion.close()


drug_json=json.loads(drug)
meta=drug_json['meta']
resultados=drug_json['results'][0]


id=resultados['id']
print("Identificador:\n",id)

proposito=resultados['purpose']
print("Proposito del producto:\n",proposito)

nombre=resultados['openfda']['manufacturer_name']
print("Nombre del fabricante:\n",nombre)

