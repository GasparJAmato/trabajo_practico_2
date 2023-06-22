import csv , requests , random , requests
from passlib.context import CryptContext
import matplotlib.pyplot as plt

#-----------------------------VALIDACIONES------------------------------------------------------------------------------------------
def validation_yes_no(respuesta)->bool:
    return respuesta not in ["s" , "n"]

def validation_1_2(respuesta)->bool:
    return respuesta not in ["1", "2"]

def validation_mail(mail, lista_de_mails)->bool:
     return "@" not in mail or mail in lista_de_mails or ".com" not in mail 

def validation_equipos(equipo_elegido, equipos_existentes)->bool:
    return equipo_elegido not in equipos_existentes

def validation_temporadas(temporada):
    lista_temporadas = []
    for i in range(9):
        lista_temporadas.append(str(i + 2015))

    return temporada not in lista_temporadas

def validar_numero(numero:str)->int:
    validar = numero.isnumeric()
    while validar != True:
        numero = input("Ingrese un numero ")
        validar = numero.isnumeric()
    numero = int(numero)


    return numero 
#-----------------------------VALIDACIONES--------------------------------------------------------------------------------------------


#lee el archivo csv y lo convierte en una lista                
def lista_informacion_de_usuarios()->list:
    lista_info = []

    with open("usuarios.csv") as archivo_csv:
        csv_reader = csv.reader(archivo_csv)

        for listas_csv in csv_reader:
            lista_info.append([listas_csv[0], listas_csv[1], listas_csv[2], listas_csv[3],listas_csv[4],listas_csv[5]])

    return lista_info

#1-------------------------------------------------------------------------------------------------------------------------------------
#lee archivos csv y lo convierte en un diccionario 

def diccionario_infromacion_usuarios()->dict:
    diccionario_info = {}
    with open("usuarios.csv") as archivo_csv:
        csv_reader = csv.reader(archivo_csv)

        for listas_csv in csv_reader:
            #"id" : {"userName": , "password": , "cantidadApostada":, "fechaUltimaApuesta": , "dineroDisponible": }
            diccionario_info[listas_csv[0]] = {"username": listas_csv[1], "password": listas_csv[2], "cantidadApostada": listas_csv[3], "fechaUltimaApuesta":listas_csv[4], "dineroDisponible":listas_csv[5] }

    return diccionario_info

def iniciar_sesion()-> None:

    validacion = "1"
    while(validacion == "1"):
        dic_ingresado = diccionario_infromacion_usuarios()
        mail = input("ingrese su mail: ")


        if mail in list(dic_ingresado.keys()):
            print("su mail es correcto")
            validacion = "0"

        elif mail not in list(dic_ingresado.keys()):
            print("su mail no se encuentra en nustro sistema")
            qst = input("si quiere ingresar un nuevo usuario ingrese (1) si quiere intentarlo de nuevo ingrese (2): ")
            while (validation_1_2(qst)):
                qst = input("Intente denuevo, (1)- nuevo usuario (2)- intentar de nuevo con otro mail: ")
            
            if(qst == "1"):
                creacion_usuario()
           
            print("intentemoslo de nuevo")

    password = input("Ingrese la contraseña ")

    password_crypt = dic_ingresado[mail]["password"]

    while (True != verificar_contraseña(password,password_crypt)):
            
            print("contraseña incorrecta")
            password = input("Ingrese de nuevo la contraseña ")
            password_crypt = encriptar_contraseña(password)

    if True == verificar_contraseña(password,password_crypt):
        menu(mail)        

def verificar_contraseña(password:str,password_crypt:str)->bool:
    #Pre:Ingreso una variable con la contraseña y otra con la contraseña encryptada
    #Post:Devuelve true si la contraseña correspone a la encriptacion
    contexto = CryptContext(
          schemes =["pbkdf2_sha256"],
          default ="pbkdf2_sha256",
          pbkdf2_sha256__default_rounds = 3000)
    
    return contexto.verify(password,password_crypt)

def encriptar_contraseña(password:str)->str:
    #Pre: Ingrese un str 
    #Post: Devuelve el str encriptado
    contexto = CryptContext(
    schemes =["pbkdf2_sha256"],
    default ="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds = 3000)

    password_crypt = contexto.hash(password)

    return password_crypt

def creacion_usuario()-> None:   
    dic_ingresado = diccionario_infromacion_usuarios()
    
    

    print("Bienvenido a #Jugarsela# ingrese sus datos para continuar")
    #ingreso del mail
    mail = input("Ingrese su mail: ")
    lista_de_mails = list(dic_ingresado.keys())
    while(validation_mail(mail, lista_de_mails)):
         mail = input("Su mail ya existe en el sistema o es incorrecto: ")
    
    #ingreso de username
    username = input("Ingrese su nombre usuario: ")

    #ingreso de password
    password = input("Ingrese su contraseña: ")

    #Encripto la password
    password_crypt = encriptar_contraseña(password)

    print("Su informacion fue ingresada con exito")

    #Ingreso de usuario a la lista para despues que se suba al usuarios.csv
    nuevo_usuario = [mail, username, password_crypt, 0,0,0]
    
    lista_ingresar_archivo("usuarios.csv", nuevo_usuario)
    #Sube la lista anterior con el archivo usuarios.csv
     
def lista_ingresar_archivo_usuarios(lista_a_ingresar)->None: 
    with open("usuarios.csv", 'w', newline ='') as archivo_csv:
        writer = csv.writer(archivo_csv, delimiter=",")       
        writer.writerows(lista_a_ingresar)

def lista_ingresar_archivo(archivo, lista_a_ingresar)->None:
    with open(archivo, 'a', newline ='') as archivo_csv:
        writer = csv.writer(archivo_csv, delimiter=",")       
        writer.writerow(lista_a_ingresar)   

def inicio()->None:
    qst = input("¿Es un usuario nuevo? s/n: ")
    while(validation_yes_no(qst)):
        qst = input("Hubo un error: ¿Es un usuario nuevo? s/n: ")

    if(qst == "s"):
        creacion_usuario()
            
    iniciar_sesion()  

#1----------------------------------------------------------------------------------------------------------------------------------------

#5-----------------------------------------------------------------------------------------------------------------------------------------
def grafico() -> None:
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

def generar_grafico_goles_minutos(minutos,goles,equipo):
    #print(f"Goles del equipo {nombre_equipo}: {goles_equipo}")
    #print(f"Minutos jugados del equipo {nombre_equipo}: {minutos_jugados}")

    plt.plot(minutos, goles)
    plt.xlabel("Minutos")
    plt.ylabel("Goles")
    plt.title("Goles realizados por " + equipo)
    plt.show()
#5-----------------------------------------------------------------------------------------------------------------------------------------

def menu(usuario)->None:
    pass

def main()->None:
    inicio()

main()