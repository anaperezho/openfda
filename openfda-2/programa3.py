# https://api.fda.gov/drug/label.json?search=active_ingredient:"acetylsalicylic"&limit=20

import http.client
import json


SERVER="api.fda.gov"
RESOURCE="/drug/label.json"
skip=0
#busco mediante el principio activo de las aspirinas
#el limite maximo es 100 a partir de ahi ulitizo el metodo skip para que sea capaz de leer todos los medicamentos
QUERY="/?search=active_ingredient:acetylsalicylic&limit=100&skip="
header={'User-Agent':'http-client'}

conexion=http.client.HTTPSConnection(SERVER)
conexion.request("GET",RESOURCE+QUERY+str(skip),None,header)

datos=conexion.getresponse()
aspirina=datos.read().decode("utf-8")
conexion.close()

aspirina_json = json.loads(aspirina)
aspirinas=aspirina_json['results']


for aspirin in aspirinas:
    id = aspirin['id']
    print("\nIdentificador:\n",id)
    if aspirin['openfda']:
        nombre=aspirin['openfda']['manufacturer_name'][0]
        print("Nombre del fabricante:\n",nombre)
    else:
        print("Fabricante no disponible")

if (len(aspirinas))==100:

    skip = skip + 100