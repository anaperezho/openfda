import http.server
import socketserver
import json
PORT=8000
INDEX_FILE="index.html"
REST_SERVER_NAME = "api.fda.gov" 
REST_RESOURCE_NAME = "/drug/label.json"
headers = {'User-Agent': 'http-client'}

class TestHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    #Definimos la funcion que va a ir a la pagina de openfda a por la informacion pedida
    def openfda_req(self,limit=1,search_str=""):
        if search_str != "":
            req_str =REST_RESOURCE_NAME+ "?"+str(search_str)+'&limit='+str(limit)
        else:
            req_str = REST_RESOURCE_NAME+'?limit='+ str(limit)
        #si esta vacio como es el caso de list drugs por ejemplo se mete en el else    

        print("Recurso solicitado: "+ req_str)
        #establece la conexion
        conn = http.client.HTTPSConnection(REST_SERVER_NAME)
        conn.request("GET", req_str, None, headers)

        # Obtener la respuesta del servidor
        r1 = conn.getresponse()
        # Lee el contenido en json, y lo transformar en una cadena
        drugs_json = r1.read().decode("utf-8")
        conn.close()
        return json.loads(drugs_json)
    
    def req_index(self):
        with open(INDEX_FILE, "r") as f:
            index_html = f.read()
        return index_html

    def req_listcompanies(self,limit):
        #llamo a la funcion openfda_req
        drugs = self.openfda_req(limit)
        meta = drugs['meta']
        total = meta['results']['total']
        limit = meta['results']['limit']
       
        
        print("* Objetos recibidos: "+str(limit)+"/"+str(total))
        #creo el contenido de la pagina tipo html

        pagina = (' <!DOCTYPE html>\n'
                   '<html lang="es">\n'
                   '<head>\n'
                   '<meta charset="UTF-8">\n'
                   '<title>List companies</title>'
                   '</head>\n'
                   '<body>\n'
                   '<h1>Companies</h1>'
                   '\n'
                   '<ol>\n')

        #analizamos y seleccionamos la informacion que hemos obtenido con la funcion openfda_req
        for drug in drugs['results']:

            
            if drug['openfda']:
                pagina += "<li>"+drug['openfda']['manufacturer_name'][0]+"</li>"
            else:
                pagina += "<li>"+"Desconocida"+"</li>"
                
       #finalizamos la pagina html
        pagina += ('</ol>\n'
                    '\n'
                    '<a href="/">Home</a>'
                    '</body>\n'
                    '</html>')

        #devuelve la pagina
        return pagina

    def req_companyname(self,limit,search_str):
        print("en companyes",search_str)
        drugs=self.openfda_req(limit,search_str)
        meta = drugs['meta']
        total = meta['results']['total']
        limit = meta['results']['limit']
        print("* Objetos recibidos: "+str(limit)+"/"+str(total))
        
       
        pagina = (' <!DOCTYPE html>\n'
                   '<html lang="es">\n'
                   '<head>\n'
                   '<meta charset="UTF-8">\n'
                    '<title>Company</title>'
                   '</head>\n'
                   '<body>\n'
                   '<h1>Company</h1>'
                   '<h2>id      Company</h2>'
                   '\n'
                   '<ol>\n')
        
        for drug in drugs['results']:

            try:
                if drug['openfda']:
                
                    
                    pagina += "<li>"+str(drug['id'])+"  -->  "+drug['openfda']['manufacturer_name'][0]+"</li>"
            except:
                pagina += "<li>"+"Unknown"+"</li>"
        pagina += ('</ol>\n'
                    '\n'
                    '<a href="/">Home</a>'
                    '</body>\n'
                    '</html>')
        
        return pagina
    def req_listdrugs(self,limit):
        drugs = self.openfda_req(limit)
        print("Principio de pagina")
        pagina = (' <!DOCTYPE html>\n'
                   '<html lang="es">\n'
                   '<head>\n'
                   '    <meta charset="UTF-8">\n'
                    '<title>List Drugs</title>'
                   '</head>\n'
                   '<body>\n'
                   '<h1>Drugs</h1>'
                   '\n'
                   '<ol>\n')
        for drug in drugs['results']:

            if drug['openfda']:
                pagina += "<li>"+drug['openfda']['substance_name'][0]+"</li>"
            else:
                pagina += "<li>"+"DESCONOCIDO"+"</li>"
        pagina += ('</ol>\n'
                    '\n'
                    '<a href="/">Home</a>'
                    '</body>\n'
                    '</html>')
        return pagina
    
    def req_substancename(self,limit,search_str):
       
        drugs=self.openfda_req(limit,search_str)
        pagina = (' <!DOCTYPE html>\n'
                   '<html lang="es">\n'
                   '<head>\n'
                   '    <meta charset="UTF-8">\n'
                    '<title>Active ingredient</title>'
                   '</head>\n'
                   '<body>\n'
                   '<h1>Drug</h1>'
                   '\n'
                   '<ol>\n')
        for drug in drugs['results']:

            # Nombre del componente principal: drugs.active_ingredient[0]
            try:
                if drug['active_ingredient']:
                
                    pagina += "<li>"+str(drug['id'])+"  -->  "+drug['active_ingredient'][0]+"</li>"
            except:
                pagina += "<li>"+"DESCONOCIDA"+"</li>"
        pagina += ('</ol>\n'
                    '\n'
                    '<a href="/">Home</a>'
                    '</body>\n'
                    '</html>')

        
        return pagina
    def req_listwarnings(self,limit):
        drugs = self.openfda_req(limit)
        print("Principio de pagina")
        pagina = (' <!DOCTYPE html>\n'
                   '<html lang="es">\n'
                   '<head>\n'
                   '    <meta charset="UTF-8">\n'
                    '<title>List Warnings</title>'
                   '</head>\n'
                   '<body>\n'
                   '<h1>Warnings</h1>'
                   '\n'
                   '<ol>\n')
        for drug in drugs['results']:

            try:
                if drug['warnings']:
                    pagina += "<li>"+drug['warnings'][0]+"</li>"
            except:
                pagina += "<li>"+"UNKNOWN"+"</li>"
        pagina += ('</ol>\n'
                    '\n'
                    '<a href="/">Home</a>'
                    '</body>\n'
                    '</html>')
        return pagina
        
    def req_secret(self):
        pagina = (' <!DOCTYPE html>\n'
                   '<html lang="es">\n'
                   '<head>\n'
                   '    <meta charset="UTF-8">\n'
                    '<title>Error 401 (Unauthorized)</title>'
                   '</head>\n'
                   '<body>\n'
                   '<h1>Error 401</h1>'
                   '\n'
                   '<h2>You are not authorized to explore this page.</h2>'
                   '\n'
                   '<h3>Try something different.</h3>'
                   '\n')
        pagina += ( '\n'
                    '<a href="/">Home</a>'
                    '</body>\n'
                    '</html>')
        return pagina
        
    def req_error(self):
        pagina = (' <!DOCTYPE html>\n'
                   '<html lang="es">\n'
                   '<head>\n'
                   '    <meta charset="UTF-8">\n'
                    '<title>Error 404 (Not Found)</title>'
                   '</head>\n'
                   '<body>\n'
                   '<h1>Error 404</h1>'
                   '\n'
                   '<h2>The requested URL was not found on this server.</h2>'
                   '\n'
                   '<h3>That is all we know.</h3>'
                   '\n')
        pagina += ( '\n'
                    '<a href="/">Home</a>'
                    '</body>\n'
                    '</html>')
        return pagina
        
    #esta es la primera funcion en ejecutarse ya que hemos utilizado el metodo get
    def do_GET(self):
        print("Recurso pedido: {}".format(self.path))
        error=200
        pagina=""
        
        recurso_list = self.path.split("?")
        endpoint = recurso_list[0]
        #mediante la longitud vemos si habia informacion específica como puede ser la busqueda de un ingrediente activo determinado
        if len(recurso_list) > 1:
            params = recurso_list[1]
        else:
            params = ""

        print("Endpoint: "+endpoint+", params: "+params)

        
        if params:
            print("Hay parametros")
            parse_limit = params.split("=")
            if parse_limit[0] == "limit":
                limit = int(parse_limit[1])
                print("Limit: {}".format(limit))
        else:
            print("SIN PARAMETROS")
        
        if endpoint=="/":
            pagina= self.req_index()
        elif endpoint == "/listCompanies":

            print("Listado de empresas")
            pagina = self.req_listcompanies(limit)
        elif endpoint == "/listDrugs":

            print("List Drugs")
            pagina = self.req_listdrugs(limit)     
        elif endpoint == "/searchCompany":
            
            params=params.split("&")
            params[0]=params[0].replace("=",":")
            
            search_str="search=openfda."+params[0]
            print("parames y search  :",params,search_str)
            
            limite=params[1].split("=")
            limit=limite[1]
            print(limit)
            pagina = self.req_companyname(limit,search_str) 
        elif endpoint == "/searchDrug":
            print(params)
            params=params.split("&")
            params[0]=params[0].replace("=",":")
            search_str="search="+params[0]
            print(search_str)
            print("parames y search  :",params,search_str)
           
            limite=params[1].split('=')
            limit=limite[1]
            pagina = self.req_substancename(limit,search_str)
        elif endpoint=="/listWarnings":
            pagina=self.req_listwarnings(limit)
        elif endpoint=="/secret":
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'basic')#modo basico para que saque el formulario
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes('Sorry but you not authenticated\n',"utf8"))#para que te saque un mensaje dentro de la pagina web
            pagina=self.req_secret()
                     
        elif endpoint=="/redirect":
            path="/"#es el inicial
            self.send_response(302)#le mandamos el error 302
            new_path = '%s%s'%('http://127.0.0.1:8000', path)#dos string al primero estring le guarda http://127.0.0.1:8000 y al segundo path
            self.send_header('Location', new_path)#vuelve a la pagina de inicio location te siyua en la direccion que tu le pases
            self.end_headers()
        else:
            self.send_response(404)
            pagina=self.req_error() 

    
    

        self.send_response(error)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(pagina, "utf8"))
        return#para salir del do get

    
    
# empieza el server   
Handler=TestHTTPRequestHandler    
httpd=socketserver.TCPServer(("",PORT),Handler)
print("serving at port", PORT)
httpd.serve_forever()