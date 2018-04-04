# https://api.fda.gov/drug/label.json?search=id:8e9683a0-5608-4cf6-8cdc-13cfc199498f
#para buscar manualmente con el id en el navegador
import http.client
import json

SERVER="api.fda.gov"
RESOURCE="/drug/label.json"
header={'User-Agent':'http-client'}
limite='?limit=10'
conexion=http.client.HTTPSConnection(SERVER)
conexion.request("GET",RESOURCE+limite,None,header)
datos10=conexion.getresponse()
medicamentos=datos10.read().decode("utf-8")
conexion.close()

medicamentos_json=json.loads(medicamentos)
resultados=medicamentos_json['results']

for medicamento in resultados:

    id=medicamento['id']
    print("Identificador:\n", id)