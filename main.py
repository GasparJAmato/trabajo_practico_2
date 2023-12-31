import csv , requests , random
from passlib.context import CryptContext
import matplotlib.pyplot as plt
from datetime import datetime
from PIL import Image
from io import BytesIO

#-----------------------------VALIDACIONES------------------------------------------------------------------------------------------
def validation_yes_no(respuesta:str)->bool:
    #Pre: Resive una respuesta del tipo str
    #Post: Retorna un booleano dependiendo si la respues es "s" o "n"
    return respuesta not in ["s" , "n"]

def validation_1_2(respuesta:str)->bool:
    #Pre: Resive una variable llamada respuesta que contenga un str 
    #Post: Retorna un booleano dependiendo si la respues es "1" o "2"
    return respuesta not in ["1", "2"]

def validation_mail(mail:str, lista_de_mails:list)->bool:
    #Pre: Resive una variable llamada mail (mail = nombre@hotmail.com) y una lista con los mails ingresado (lista_de_mails = [name@hotmail.com,username@gmail.com,etc])
    #Post: Retorna un booleano dependiendo si mail cumple con @, .com o si esta en lista_de_mails
     return "@" not in mail or mail in lista_de_mails or ".com" not in mail 

def validation_equipos(equipo_elegido:str, equipos_existentes:list)->bool:
    #Pre: Resive una variable llamado equipo_elegido ingresado por el usuario (ej Tigre) y una lista llamada lista equipos_existentes donde se encuentra los equipos traidos por la api  (lista equipos_existentes = Tigre, Boca Juniors, etc) 
    #Post: Retorna un booleano dependiendo si el equipo_elegido se encuentra en en la llamada lista equipos_existentes
    return equipo_elegido not in equipos_existentes

def validation_temporadas(temporada:str):
    #Pre: Resive una variable con el numero de temporada ingresado por el usuario (temporada = 2022)
    #POst: Retorna un booleando dependiendo si se en la lista llamada lista_temporadas (lista_temporadas = [2015,..,2023])
    lista_temporadas = []
    for i in range(9):
        lista_temporadas.append(str(i + 2015))

    return temporada not in lista_temporadas

def validar_numero(numero:str)->int:
    #Pre: Resive una variable llamado numero del tipo str (ej numero = "1")
    #Post: Retorna retorna un numero entero (ej numero = 1)

    validar = numero.isnumeric()
    while validar != True:
        numero = input("Ingrese un numero ")
        validar = numero.isnumeric()
    numero = int(numero)

    return numero 

def validar_contraseña(password:str,password_crypt:str)->bool:
    #Pre:Ingreso dos variable una con la contraseña y otra con la contraseña encryptada
    #Post:Devuelve true si la contraseña correspone a la encriptacion
    contexto = CryptContext(schemes=["sha256_crypt"])#Esquema de incriptacion
    return contexto.verify(password, password_crypt)

#-----------------------------VALIDACIONES--------------------------------------------------------------------------------------------

#1-------------------------------------------------------------------------------------------------------------------------------------
               
def lista_informacion_de_usuarios()->list:
    #lee el archivo csv y lo convierte en una lista 
    lista_info = []

    with open("usuarios.csv") as archivo_csv:
        csv_reader = csv.reader(archivo_csv)

        for listas_csv in csv_reader:
            lista_info.append([listas_csv[0], listas_csv[1], listas_csv[2], listas_csv[3],listas_csv[4],listas_csv[5]])

    return lista_info

def diccionario_infromacion_usuarios()->dict:
    #lee archivos csv y lo convierte en un diccionario 
    diccionario_info = {}
    with open("usuarios.csv") as archivo_csv:
        csv_reader = csv.reader(archivo_csv)

        for listas_csv in csv_reader:
            #"id" : {"userName": , "password": , "cantidadApostada":, "fechaUltimaApuesta": , "dineroDisponible": }
            diccionario_info[listas_csv[0]] = {"username": listas_csv[1], "password": listas_csv[2], "cantidadApostada": listas_csv[3], "fechaUltimaApuesta":listas_csv[4], "dineroDisponible":listas_csv[5] }

    return diccionario_info

def iniciar_sesion()-> None:
    #Pre:Resive del usuario la contraseña y el mail
    #Post:Ingresa al menu 
    validacion = "1"
    while(validacion == "1"): #Verifica que el mail ingresado sea correcto
        dic_ingresado = diccionario_infromacion_usuarios()
        mail = input("-ingrese su mail: ")
        print()

        if mail in list(dic_ingresado.keys()):
            print("Su mail es correcto")
            print()
            validacion = "0"

        elif mail not in list(dic_ingresado.keys()):
            print("XXX-Su mail no se encuentra en nustro sistema-XXX")
            print()
            qst = input("si quiere ingresar un nuevo usuario ingrese (1) si quiere intentarlo de nuevo ingrese (2): ")
            print()
            while (validation_1_2(qst)):
                qst = input("Intente de nuevo, (1)- nuevo usuario (2)- intentar de nuevo con otro mail: ")
                print()
            
            if(qst == "1"):
                creacion_usuario()
            print("Intentemoslo de nuevo")
            print()

    password = input("-Ingrese la contraseña: ")
    print()

    password_crypt = dic_ingresado[mail]["password"]

    while (True != validar_contraseña(password,password_crypt)):#Valida la password
            
            print("XXX-contraseña incorrecta-XXX")
            print()
            password = input("-Ingrese de nuevo la contraseña: ")
            password_crypt = encriptar_contraseña(password)

    if True == validar_contraseña(password,password_crypt):
        menu(mail)        

def encriptar_contraseña(password:str)->str:
    #Pre: Ingrese una variable llamada paswword (password = contraseña del usuario)
    #Post: Retorno la variable con su str encriptado 
    contexto = CryptContext(schemes=["sha256_crypt"])#Esquema de incriptacion
    return contexto.hash(password)


def creacion_usuario()-> None:   
    #Pre: Le pide al usuario que ingrese la contraseña y el mail
    #Post: Crea el usuario metiendolo en el archivo csv llamado usuarios.csv
    dic_ingresado = diccionario_infromacion_usuarios()
    
    print("Bienvenido a #Jugarsela# ingrese sus datos para continuar")
    print()
    #ingreso del mail
    mail = input("-Ingrese su mail: ")
    print()
    lista_de_mails = list(dic_ingresado.keys())
    while(validation_mail(mail, lista_de_mails)):
         mail = input("Su mail ya existe en el sistema o es incorrecto: ")
         print()
    
    #ingreso de username
    username = input("-Ingrese su nombre usuario: ")
    print()
    #ingreso de password
    password = input("-Ingrese su contraseña: ")
    print()
    #Encripto la password
    password_crypt = encriptar_contraseña(password)
    print("Su informacion fue ingresada con exito")
    print()

    #Ingreso de usuario a la lista para despues que se suba al usuarios.csv
    nuevo_usuario = [mail, username, password_crypt, 0,0,0]
    
    lista_ingresar_archivo("usuarios.csv", nuevo_usuario)
    #Sube la lista anterior con el archivo usuarios.csv
     
def lista_ingresar_archivo_usuarios(lista_a_ingresar)->None: 
    #Pre:Resive una lista llamada lista_a_ingresar con los movimientos echos por el usuario(ej ingreso de dinero)
    #Post:Remplaza el archivo usuario,csv y lo cambia por la nueva lista
    with open("usuarios.csv", 'w', newline ='') as archivo_csv:
        writer = csv.writer(archivo_csv, delimiter=",")       
        writer.writerows(lista_a_ingresar)

def lista_ingresar_archivo(archivo, lista_a_ingresar)->None:
    #Pre:Resive un str con el nombre del archivo csv en la variable archivo y una lista con con los str a ingresar al archivo
    #Post:Ingresa la lista al archivo csv en la ultima linea
    with open(archivo, 'a', newline ='') as archivo_csv:
        writer = csv.writer(archivo_csv, delimiter=",")       
        writer.writerow(lista_a_ingresar)   

def inicio()->None:
    #Pre: Solicita s o n al usuario 
    #Post: Si es ingresa a la funcion creacion de usuario, y si es n ingresa a la funcion iniciar secion
    qst = input("¿Es un usuario nuevo? s/n: ")
    print()
    while(validation_yes_no(qst)):
        qst = input("Hubo un error: ¿Es un usuario nuevo? s/n: ")
        print()

    if(qst == "s"):
        creacion_usuario()
            
    iniciar_sesion()  

#1----------------------------------------------------------------------------------------------------------------------------------------
#2----------------------------------------------------------------------------------------------------------------------------------------
def buscar_jugadores_por_equipo()->None:
    #Pre:El usuario ingresa un equipo(str)
    #Post:Lo busca mediante la api y devuelve un print del plantel del equipo correspondiente
    print("EQUIPOS EXISTENTES")
    ids_de_equipos = impresion_equipos_liga_profesional()#Pidos los equipos a la api
    print()
    equipo = input("ingrese un equipo ")
    print()
    while validation_equipos(equipo, ids_de_equipos.keys()):
        print("")
        impresion_equipos_liga_profesional()
        print()
        equipo = input("su equipo no fue encontrado, ingrese un equipo de la lista ")
        print()

    id_de_equipo = ids_de_equipos[equipo] 

    url = "https://v3.football.api-sports.io/players"

    params={#Parametros para filtrar los endpoint
        "league":"128",
        "season":"2023",
        "team" : id_de_equipo
    }
    headers = {
    'x-rapidapi-key': '0a46210016de4ff4781c6efe3d7e8711',
    'x-rapidapi-host': 'v3.football.api-sports.io'
    }

    response = requests.request("GET", url, headers=headers, params=params)
    reponse_json = response.json()

    print(f"LISTA DE JUGADORES DE {equipo.upper()}")
    for i in range(len(reponse_json["response"])):     
       print("-", reponse_json["response"][i]["player"]["name"])
    
def impresion_equipos_liga_profesional()->dict:
    #Pre: Se genera un pedido a la api con los equipos de en argentina en 2023
    #Post: Genera un diccionario con ids y equipos(ej 453:Indendiente), despues de generarlo tambien genera un print con los equipos de la liga utilizando la api
    url = "https://v3.football.api-sports.io/teams?country=Argentina&league=128&season=2023"

    payload={}
    headers = {
    'x-rapidapi-key': '0a46210016de4ff4781c6efe3d7e8711',
    'x-rapidapi-host': 'v3.football.api-sports.io'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    reponse_json = response.json()

    diccionario_equipos_ids = {}

    for i in range(len(reponse_json["response"])):
        diccionario_equipos_ids[reponse_json["response"][i]["team"]["name"]] = reponse_json["response"][i]["team"]["id"]
        print("-",reponse_json["response"][i]["team"]["name"])
    

    return diccionario_equipos_ids
#2-----------------------------------------------------------------------------------------------------------------------------------------
#3-----------------------------------------------------------------------------------------------------------------------------------------
def tabla_posiciones()->None:
    #Pre: Se genera un pedido a la api con el numero de league y año de temporada
    #Post: Genera un print con la tabla de posiciones de la temporada elegida
    season = input("ingrese la temporada a utilizar: ")
    while(validation_temporadas(season)):
        season = input("ingrese una temporada desde 2015-2023 (2023 no esta actualizado)  ")

    url = "https://v3.football.api-sports.io/standings"

    params={
        "league":"128",
        "season": season,
    }
    headers = {
    'x-rapidapi-key': '0a46210016de4ff4781c6efe3d7e8711',
    'x-rapidapi-host': 'v3.football.api-sports.io'
    }

    response = requests.request("GET", url, headers=headers, params=params)
    reponse_json = response.json()

    print("")
    print(f"Tabla de posiciones Año {season}")

    val =0
    for i in range(len(reponse_json["response"])):
       for e in range(len(reponse_json["response"][i]["league"]["standings"])):
            
            for f in range(len(reponse_json["response"][i]["league"]["standings"][e])):     
                print(reponse_json["response"][i]["league"]["standings"][e][f]["rank"],"-", reponse_json["response"][i]["league"]["standings"][e][f]["team"]["name"]," (puntos:", reponse_json["response"][i]["league"]["standings"][e][f]["points"],")")

            if season in ["2022"] and val == 0:
                val = 1
                print("")
                print("----Liga Argentina 1era fase----")

#3-----------------------------------------------------------------------------------------------------------------------------------------
#4-----------------------------------------------------------------------------------------------------------------------------------------
def info_equipos():
    #Pre: Realizo un pedido a la api de un equipo especifico
    #Post: Genera un print con la informacion del equipo y su escudo
    print("EQUIPOS EXISTENTES")
    print()
    dic_equipos_existentes = impresion_equipos_liga_profesional()#Imprimo los equipos y me taigo el diccionario con el id del equipo
    print()

    equipo_elegido = input("Elija un equipo de la lista: ")
    while(validation_equipos(equipo_elegido, list(dic_equipos_existentes.keys()))):
        equipo_elegido = input("Su equipo no esta en la lista, elija otro ")

    url = "https://v3.football.api-sports.io/teams"

    params={
        "league":"128",
        "id": dic_equipos_existentes[equipo_elegido],
        "season": "2023"
    }
    headers = {
    'x-rapidapi-key': '0a46210016de4ff4781c6efe3d7e8711',
    'x-rapidapi-host': 'v3.football.api-sports.io'
    }

    response = requests.request("GET", url, headers=headers, params=params)
    reponse_json = response.json() 
    print("")
    print("----Informacion Sobre el Estadio----")
    print("Nombre del estadio: ", reponse_json["response"][0]["venue"]["name"] )
    print("Direccion del estadio: ",reponse_json["response"][0]["venue"]["address"] )
    print("Ciudad: ", reponse_json["response"][0]["venue"]["city"] )
    print("Capacidad: ",reponse_json["response"][0]["venue"]["capacity"] )
    print("Superficie: ", reponse_json["response"][0]["venue"]["surface"])

    # URL de la imagen
    url_imagen = reponse_json["response"][0]["team"]["logo"]
    # Realiza una solicitud GET para obtener la imagen
    response = requests.get(url_imagen)
    # Abre la imagen utilizando Pillow
    image = Image.open(BytesIO(response.content))
    # Muestra la imagen
    image.show()
#4-----------------------------------------------------------------------------------------------------------------------------------------

#5-----------------------------------------------------------------------------------------------------------------------------------------
def grafico() -> None:
    #Pre: Realizo un pedido a la api de un equipo especifico con las estadisticas de goles x minuto
    #Post: Imprimo un grafico con dichas estadisticas
    print("EQUIPOS EXISTENTES")
    print()
    ids_de_equipos = impresion_equipos_liga_profesional()
    print()
    equipo = input("ingrese un equipo ")
    print()
    while validation_equipos(equipo, ids_de_equipos.keys()):
        print("")
        impresion_equipos_liga_profesional()
        print()
        equipo = input("su equipo no fue encontrado, ingrese un equipo de la lista ")
        print()

    id_de_equipo = ids_de_equipos[equipo] 


    url = "https://v3.football.api-sports.io/teams/statistics"

    params={
        "league":"128",
        "season":"2023",
        "team" : id_de_equipo
    }
    headers = {
    'x-rapidapi-key': '27f73ffa427b9ace919cc32b30270953',
    'x-rapidapi-host': 'v3.football.api-sports.io'
    }

    response = requests.request("GET", url, headers=headers, params=params)
    reponse_json = response.json()

    goles = []
    minutos = list(reponse_json["response"]["goals"]["for"]["minute"].keys())
    for i in minutos:
         goles.append(reponse_json["response"]["goals"]["for"]["minute"][i]["total"])

    generar_grafico_goles_minutos(minutos,goles,equipo)

def generar_grafico_goles_minutos(minutos:list,goles,equipo:list):
    #Pre:Recivo 2 listas, llamadas minutos con los minutos correspondiente a cada gol y Goles con los goles correspondiente a cada minuto
    #Post: Genero un grafico con los minutos jugados en eje x y los goles realizados en el eje y 

    plt.plot(minutos, goles)
    plt.xlabel("Minutos")
    plt.ylabel("Goles")
    plt.title("Goles realizados por " + equipo)
    plt.show()
#5-----------------------------------------------------------------------------------------------------------------------------------------
#6-----------------------------------------------------------------------------------------------------------------------------------------

def lista_transacciones()->list:
    #Pre:Genero una lista llamada lista_info con las transacciones del archivo csv llamado transacciones.csv
    #Post:Retorno la lista llamada lista_info

    lista_info = []
    with open("transacciones.csv") as archivo_csv:
        csv_reader = csv.reader(archivo_csv)

        for listas_csv in csv_reader:
            print(listas_csv)
            lista_info.append([listas_csv[0],listas_csv[1],listas_csv[2]]) 

    return lista_info

def conversor_de_dict_en_list(diccionario:dict)->list:
    #Pre:Recivo una diccionario con la informacion del usuario generado con funcion "diccionario_infromacion_usuarios()""
    #Post: Retorno el diccionario en una lista
    mails = diccionario.keys()
    lista_resultante = []
    for i in mails:
        lista_resultante.append([i, diccionario[i]["username"],diccionario[i]["password"],diccionario[i]["cantidadApostada"],diccionario[i]["fechaUltimaApuesta"],diccionario[i]["dineroDisponible"]])
    
    
    return lista_resultante

def modificar_transacciones(mail:str,tipo_de_transaccion:str, cantidad:int)->None:
    #Pre:Recivo del usuario 3 variables llamadas, mail, tipo_de_transaccion y cantidad (ej mail=name@hotmail.com, tipo_de_transaccion = "deposita" y cantidad = 302002)
    #Post:Actualizo el archivo transaccion.csv y usuarios.csv 

    diccionario_informacion_usuarios = diccionario_infromacion_usuarios()

    if tipo_de_transaccion == "Aposto":#Actualiza usuarios.csv en disponible 
       diccionario_informacion_usuarios[mail]["cantidadApostada"] = int(diccionario_informacion_usuarios[mail]["cantidadApostada"]) + cantidad
       diccionario_informacion_usuarios[mail]["fechaUltimaApuesta"] = str(datetime.now())[0:16]
       lista_informacion_de_usuarios = conversor_de_dict_en_list(diccionario_informacion_usuarios)
       lista_ingresar_archivo_usuarios(lista_informacion_de_usuarios)

   
    elif tipo_de_transaccion != "Aposto":
       #actualiza el archivo de usuarios con lo ganado perdido o ingresado
       diccionario_informacion_usuarios[mail]["dineroDisponible"] = int(diccionario_informacion_usuarios[mail]["dineroDisponible"]) + cantidad
       lista_informacion_de_usuarios = conversor_de_dict_en_list(diccionario_informacion_usuarios)
       lista_ingresar_archivo_usuarios(lista_informacion_de_usuarios)

       #actualiza el archivo de transacciones 
       lista_de_transacciones = [mail,tipo_de_transaccion,str(datetime.now())[0:16],cantidad]
       lista_ingresar_archivo("transacciones.csv", lista_de_transacciones)
    
def ingresar_dinero(usuario:str):
    #Pre: Recivo el mail de usuario que ingreso sesion y solicito la cantidad de dinero a ingresar
    #Post: Ingreso el dinero al archivo usuario.csv y genero una transacion modificando transacciones.csv
    cantidad = input("Ingrese el monto a depositar")
    
    cantidad = validar_numero(cantidad)

    modificar_transacciones(usuario,"Deposita", cantidad)

#6-----------------------------------------------------------------------------------------------------------------------------------------

#7-----------------------------------------------------------------------------------------------------------------------------------------
def usuario_mas_apostado()->None:
     #Pre: Genero un diccionario con la informacion de los usuarios
     #Post: Mediante el diccionario busco al usuario que mas aposto 
     inf_usuarios = diccionario_infromacion_usuarios()
     

     usuarios_apuestas = {}

     for i in inf_usuarios.keys():
         usuarios_apuestas[i] = inf_usuarios[i]["cantidadApostada"]

     if max(usuarios_apuestas, key=usuarios_apuestas.get) == "MAIL":
         print("No hay apuestas realizadas")

     else:
           print("El usuario que mas veces aposto es:",max(usuarios_apuestas, key=usuarios_apuestas.get))

#7-----------------------------------------------------------------------------------------------------------------------------------------

#8-----------------------------------------------------------------------------------------------------------------------------------------
def usuarios_mas_gano()->None:
     #Pre:Leo el archivo transacciones.csv 
     #Post:Busco el usario que mas veces aparacese que gano en el archivo 
     
     with open("transacciones.csv") as archivo_csv:
        csv_reader = csv.reader(archivo_csv)

        print(csv_reader)
        usuarios_ganadas = {}

        for i in csv_reader:
            if i[1] == "Gana":
                if i[0] in usuarios_ganadas.keys():
                    usuarios_ganadas[i[0]] = usuarios_ganadas[i[0]]+1
                
                else:
                    usuarios_ganadas[i[0]] = 1
                

        print("El usuario que mas veces gano es:",max(usuarios_ganadas, key=usuarios_ganadas.get)) 
#8-----------------------------------------------------------------------------------------------------------------------------------------

#9-----------------------------------------------------------------------------------------------------------------------------------------

def gana_local(pago_extra:dict,id_fixture:int,opcion:int,aposto:int,dinero:int,usuario:str)->None:
    #Pre: Resivo pago extra (pago extra:L(Se guarda con "L" si tiene el true el local o con "V"
    #si tiene el true el visitante),3(Numero al azar)), id_fixture(numero de fixture),opcion("L","V" y "EMPATE"), usuario(mail del usuario) y dinero 
    #Post: Revisa la opcion, si gano genera un pago, una transaccion y actualiza el archivo csv con el dinero ganado y si pierde lo resta del archivo csv y genera una transaccion

    print("GANO LOCAL")
    print()
    print(pago_extra[id_fixture][0])
    aposto = int (aposto)
    pago = int(pago_extra[id_fixture][1])


    if  opcion == "L" and opcion == pago_extra[id_fixture][0]:# L == L y L == L
        dinero += aposto*pago
        print("GANASTE: ",dinero)
        modificar_transacciones(usuario,"Gana",dinero)
        
    elif opcion == "L" and opcion != pago_extra[id_fixture][0]: # L == y L != V
       dinero += aposto*(pago/10)
       print("GANASTE: ",dinero)
       modificar_transacciones(usuario,"Gana",dinero)
    
    else:
       print("PERDISTE")
       dinero -= aposto
       modificar_transacciones(usuario,"Pierde",dinero)

def gana_visitante(pago_extra:dict,id_fixture:int,opcion:int,aposto:int,dinero:int,usuario)->None: 
    #Pre: Resivo pago extra (pago extra:L(Se guarda con "L" si tiene el true el local o con "V"
    #si tiene el true el visitante),3(Numero al azar)), id_fixture(numero de fixture),opcion("L","V" y "EMPATE"), usuario(mail del usuario) y dinero 
    #Post: Revisa la opcion, si gano genera un pago, una transaccion y actualiza el archivo csv con el dinero ganado y si pierde lo resta del archivo csv y genera una transaccion
    print("GANO VISITANTE")
    print(pago_extra[id_fixture][0])
    aposto = int (aposto)
    pago = int(pago_extra[id_fixture][1])


    if  opcion == "V" and opcion == pago_extra[id_fixture][0]:# V == V y V == V
        dinero += aposto*pago
        print("GANASTE: ",dinero)
        modificar_transacciones(usuario,"Gana",dinero)
        
    elif opcion == "V" and opcion != pago_extra[id_fixture][0]: # V == V y V != L
       dinero += aposto*(pago/10)
       print("GANASTE: ",dinero)
       modificar_transacciones(usuario,"Gana",dinero)
    
    else:
       print("PERDISTE")
       dinero -= aposto
       modificar_transacciones(usuario,"Pierde",dinero)

def empate(opcion:int,aposto:int,dinero:int,usuario:str)->None:
    #Pre: Resivo pago extra (pago extra:L(Se guarda con "L" si tiene el true el local o con "V"
    #si tiene el true el visitante),3(Numero al azar)), usuario(mail del usuario) y dinero 
    #Post: Revisa la opcion, si gano genera un pago, una transaccion y actualiza el archivo csv con el dinero ganado y si pierde lo resta del archivo csv y genera una transaccion
    print("EMPATARON")
    print()
    aposto = int (aposto)

    if  opcion == "EMPATE": #Empate = Empate
        dinero += aposto*0.5
        print("GANASTE: ",dinero)
        modificar_transacciones(usuario,"Gana",dinero)
        
    else:
       print("PERDISTE")
       dinero -= aposto
       modificar_transacciones(usuario,"Pierde",dinero)

def apuesta(pago_extra:dict,id_fixture:int,usuario:str)->None:
    #Pre: Resivo pago extra (pago extra:L(Se guarda con "L" si tiene el true el local o con "V"
    #si tiene el true el visitante),3(Numero al azar)), id_foxture(numero de fixture),opcion("L","V" y "EMPATE"), usuario(mail del usuario) 
    #Se tira un dado(1 al 3) para ver quien gana
    #Se lee el usuarios.csv para solicitar el dinero del usuario actualmente
    #Post: Se actualiza usuarios.csv y transacciones.csv con lo apostado y se ingresa a las funciones dependiendo el dado 
     datos = []
     
     with open("usuarios.csv", newline='', encoding="UTF-8") as archivo_csv:

        csv_reader = csv.reader(archivo_csv, delimiter=',')

        next(csv_reader) #Evitamos leer el header
 
        for row in csv_reader:

          datos.append(row)


     usuarios_dinero = {} #Usuario:dinero

     for i in range(len(datos)):
         usuarios_dinero[datos[i][0]] = datos[i][5]

     dinero_disponible = int(usuarios_dinero[usuario])

     print("La apuesta podrá ser ganador Local (L)/Empate/Ganador visitante (V)")
     opcion = input("Ingrese su opcion: ").upper()

     print()

     print("Dinero disponible:",dinero_disponible)

     print()

     aposto = input("Cuanto desea apostar: ")

     aposto = validar_numero(aposto)

     while aposto > dinero_disponible: #Verifico que el dinero apostado sea del disponible
              aposto = input("Saldo insuficiente, intente de nuevo: ")

     modificar_transacciones(usuario,"Aposto", aposto) #Aumenta la cantidad apostada en usuarios.csv

     dinero = 0

     simulacion = random.randint(1,3)

     if simulacion == 1:
        gana_local(pago_extra,id_fixture,opcion,aposto,dinero,usuario)
    

     elif simulacion == 2:
        gana_visitante(pago_extra,id_fixture,opcion,aposto,dinero,usuario)

     elif simulacion == 3:
        empate(opcion,aposto,dinero,usuario)
      
def apuesta_opc(pago_extra:dict,id_fixture:int,usuario:str)->None:
    ##Pre: Recibo pago extra (pago extra:L(Se guarda con "L" si tiene el true el local o con "V"
    #si tiene el true el visitante),3(Numero al azar)), id_fixture(numero de fixture),opcion("L","V" y "EMPATE"), usuario(mail del usuario)
    #Post: Ingreso dichas variables a apuesta dependiendo si el usuario decide apostar 


    opcion = input("Deseas apostar por este partido s/n ")

    if opcion == "s":
        apuesta(pago_extra,id_fixture,usuario)

    else:
        print("SALISTE")

def pago_apuesta(fixture_json:dict,usuario:str)->dict:
    #Pre: Recibo el un diccionario con el fixture solicitado en la api y el usuario (usuario = mail)
    #post:Genero mediante el diccionario y el numero de fixture elegido por el usuario un pedido a la api con las predicciones e imprimo lo que paga por apuesta, y te adentra a la funcion apuesta con el id_fixture y el mail
    
    pago_extra = {}#Id fixture:nro random de paga

    numero_fixture = input("Indique el numero de partido para indicar su pago: ")

    numero_fixture = validar_numero(numero_fixture)

    cantidad_fixture = len(fixture_json["response"])+1

    while numero_fixture > cantidad_fixture or numero_fixture <= 0:
        print("Numero de partido incorrecto")
        numero_fixture = input("Indique un numero correcto: ")
        numero_fixture = validar_numero(numero_fixture)

        
    print()

    id_fixture = fixture_json["response"][numero_fixture-1]["fixture"]["id"]#Guardo el id del fixture mediante el numero de fixture elegido

    url = "https://v3.football.api-sports.io/predictions"

    params={
        "fixture":id_fixture
        
    }
    headers = {
    'x-rapidapi-key': '27f73ffa427b9ace919cc32b30270953',
    'x-rapidapi-host': 'v3.football.api-sports.io'
    }
     
    response = requests.request("GET", url, headers=headers, params=params)
    reponse_predicion_json = response.json()

    win_or_draw = reponse_predicion_json["response"][0]["predictions"]["win_or_draw"]

    nro_pago = random.randint(1,4)

    if win_or_draw == True:
        print()
        print("Si se apuesta ",fixture_json["response"][numero_fixture-1]["teams"]["away"]["name"],"ganador paga ",nro_pago," veces lo apostado")
        print()
        print("Si se apuesta ",fixture_json["response"][numero_fixture-1]["teams"]["away"]["name"],"empate paga ",0.5," veces lo apostado")
        print()
        print("Si se apuesta ",fixture_json["response"][numero_fixture-1]["teams"]["home"]["name"],"empate paga ",0.5," veces lo apostado")
        print()
        print("Si se apuesta ",fixture_json["response"][numero_fixture-1]["teams"]["home"]["name"],"ganador paga ",nro_pago/10," veces lo apostado")
        print()
        pago_extra[id_fixture] = "L",nro_pago
    elif win_or_draw == False:
        print()
        print("Si se apuesta ",fixture_json["response"][numero_fixture-1]["teams"]["home"]["name"],"ganador paga ",nro_pago," veces lo apostado")
        print()
        print("Si se apuesta ",fixture_json["response"][numero_fixture-1]["teams"]["home"]["name"],"empata paga ",0.5," veces lo apostado")
        print()
        print("Si se apuesta ",fixture_json["response"][numero_fixture-1]["teams"]["away"]["name"],"empata paga ",0.5," veces lo apostado")
        print()
        print("Si se apuesta ",fixture_json["response"][numero_fixture-1]["teams"]["away"]["name"],"ganador paga ",nro_pago/10," veces lo apostado")
        print()
        pago_extra[id_fixture] = "V",nro_pago
    
    apuesta_opc(pago_extra,id_fixture,usuario)
   
def impresion_fixture(fixture_json:dict)->None:
    #Pre: Ingreso un diccionario con el fixture de un equipo
    #Post: Imprimo el fixture del equipo
    for i in range(len(fixture_json["response"])):
       print()
       print("-"*3,fixture_json["response"][i]["fixture"]["date"],"-"*3)     
       print(" "*10,fixture_json["response"][i]["teams"]["home"]["name"],"(L)")
       print(" "*15,"VS")
       print(" "*10,fixture_json["response"][i]["teams"]["away"]["name"],"(V)")
       print("-"*10,"N°",i+1,"-"*10)   
       print()
       
def fixture(usuario:str)->None:
    #Pre: Pido un equipo (str)
    #Post: Genero un pedido a la api con el fixture del equipo y me adentro a las funciones para apostar
    print("EQUIPOS EXISTENTES")
    ids_de_equipos = impresion_equipos_liga_profesional()
    print()
    equipo = input("ingrese un equipo ")
    print()
    while validation_equipos(equipo, ids_de_equipos.keys()):
        print("")
        impresion_equipos_liga_profesional()
        print()
        equipo = input("su equipo no fue encontrado, ingrese un equipo de la lista ")
        print()

    id_de_equipo = ids_de_equipos[equipo]

    url = "https://v3.football.api-sports.io/fixtures"

    params={
        "league":"128",
        "season":"2023",
        "team" : id_de_equipo
    }
    headers = {
    'x-rapidapi-key': '27f73ffa427b9ace919cc32b30270953',
    'x-rapidapi-host': 'v3.football.api-sports.io'
    }
     
    response = requests.request("GET", url, headers=headers, params=params)
    fixture_json = response.json()

    print(f"FIXTURE {equipo.upper()}")

    impresion_fixture(fixture_json) #Imprime el fixture del equipo elegido 

    pago_apuesta(fixture_json,usuario) 

#9-----------------------------------------------------------------------------------------------------------------------------------------

#-------------------MENU------------------------------------------------------------------------------------------------------------------
def imprimir_opciones() -> None:
    #IMPRIMO LAS OPCIONES
    print("-"*20)
    print("Menu de Opciones:")
    print("a. Plantel segun el equipo")
    print("b. Tabla de posiciones segun la temporada")
    print("c. Informacion de un equipo (Estadio y escudo)")
    print("d. Grafico por minutos y goles segun un equipo")
    print("e. Ingresar dinero a su cuenta")
    print("f. Usuario que mas dinero aposto")
    print("h. Usuario que mas veces gano")
    print("i. Apostar")
    print("k. Salir")
    print("-"*20)

def seleccionar_opcion() -> str:
    #Post: Retorna una opcion elegida por el usuario
    imprimir_opciones()

    opt = input("Ingrese una opcion: ")
    print()

    return opt

def menu(usuario)->None:
    #Pre: Resive al usuario 
    #Post: Se ingresa al menu del juego con las opciones para jugar

    opt = seleccionar_opcion()

    while   opt  !=  'k' :

        if  opt ==  'a' :
            buscar_jugadores_por_equipo()

        elif  opt  ==  'b' :
            tabla_posiciones()

        elif  opt  ==  'c' :
            info_equipos()

        elif  opt  ==  'd' :
             grafico()

        elif  opt  ==  'e' :
            ingresar_dinero(usuario)
        
        elif opt  ==  'f' :
            usuario_mas_apostado()
        
        elif opt  ==  'h' :
            usuarios_mas_gano()

        elif opt  ==  'i' :
            fixture(usuario)#ACEDER AL FIXTURE DE TU EQUIPO PARA APOSTAR
        else:
            print("OPCION INCORRECTA!!!. Seleccione una opcion porfavor")
        
        opt  =  seleccionar_opcion ()
    print()
    print("SALIO")
    print()
    inicio()

#-------------------MENU--------------------------------------------------------------------------------------------------------------------

#-------------------CREACION DE ARCHIVO-----------------------------------------------------------------------------------------------------
def creacion_archivos_csv()->None:
     #CREA LOS ARCHIVOS USUARIOS.CSV Y TRANSACCIONES.CSV
     
     with open("usuarios.csv", 'w', newline ='') as archivo_csv:
        writer = csv.writer(archivo_csv, delimiter=",")       
        writer.writerow(["MAIL","NOMBRE DE USUARIO","PASSWORD", "CANTIDAD APOSTADA","FECHA ULTIMA APUESTA","DINERO DISPONIBLE"])

     with open("transacciones.csv", 'w', newline ='') as archivo_csv:
        writer = csv.writer(archivo_csv, delimiter=",")       
        writer.writerow(["MAIL","TIPO DE TRANSACCION","FECHA", "IMPORTE"])
#-------------------CREACION DE ARCHIVO-----------------------------------------------------------------------------------------------------

def main()->None:
    creacion_archivos_csv()
    inicio()

main()