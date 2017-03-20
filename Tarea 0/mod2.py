import sys
import os
from mod1 import Usuario, Meteorologia, Incendio, Recurso


# Funciones que retornan los objetos de sus respectivos diccionarios
# despues ver si es util encontrar los objetos con otros parametros
def objeto_incendio(dato):
    if str(type(dato)) == "<class 'int'>":  # si el dato es un numero
        return Incendio.dicc_incendios[dato]
    if dato.isdigit():  # si el dato es un string de un numero
        return Incendio.dicc_incendios[int(dato)]
    return False


def objeto_recurso(dato):
    if str(type(dato)) == "<class 'int'>":  # si el dato es un numero
        return Recurso.dicc_recursos[dato]
    if dato.isdigit():  # si el dato es un string de un numero
        return Recurso.dicc_recursos[int(dato)]
    return False


def objeto_meteorologia(dato):
    if str(type(dato)) == "<class 'int'>":  # si el dato es un numero
        return Meteorologia.dicc_meteorologia[dato]
    if dato.isdigit():  # si el dato es un string de un numero
        return Meteorologia.dicc_meteorologia[int(dato)]
    return False


def objeto_usuario(dato):
    if str(type(dato)) == "<class 'int'>":  # si el dato es un numero
        return Usuario.dicc_usuarios[dato]
    if dato.isdigit():  # si el dato es un string de un numero
        return Usuario.dicc_usuarios[int(dato)]
    for ide in Usuario.dicc_usuarios:  # si el dato es el nombre
        if Usuario.dicc_usuarios[ide].nombre == dato:
            return Usuario.dicc_usuarios[ide]
    return False


# Funciones que aseguran que los inputs sean correctos
def usuario_valido(nombre):
    # retorna si el nombre es valido (si esta dentro de la base de datos)
    lista_usuarios = []
    for id_usuario in Usuario.dicc_usuarios:
        lista_usuarios.append(Usuario.dicc_usuarios[id_usuario].nombre)
    if nombre in lista_usuarios:
        return True
    return False


def constrasena_valida(contrasena):
    # retorna si la constrasena es valida (si esta dentro de la base de datos)
    lista_constrasenas = []
    for id_usuario in Usuario.dicc_usuarios:
        lista_constrasenas.append(Usuario.dicc_usuarios[id_usuario].contrasena)
    if contrasena in lista_constrasenas:
        return True
    return False


def fecha_valida(fecha):
    # retorna si la fecha es valida (si esta en un formato adecuado
    # y si esta puede existir)
    triplete = fecha.split("-")
    if len(triplete) == 3:
        ano = triplete[0]
        mes = triplete[1]
        dia = triplete[2]
        bisiesto = "no"
        if ano.isdigit() and mes.isdigit() and dia.isdigit():
            # revisa si el ano es o no bisiesto
            if int(int(ano)/4) - int(ano)/4 == 0:
                if int(int(ano)/100) - int(ano)/100 == 0:
                    bisiesto = "no"
                    if int(int(ano)/400) - int(ano)/400 == 0:
                        bisiesto = "si"
            if mes in ["1", "01", "3", "03", "5", "05", "7", "07", "8", "08",
                       "10", "12"]:  # tambien permite meses y dias de 1 digito
                if int(dia) <= 31:
                    return True
                return False
            if mes in ["4", "04", "6", "06", "9", "09", "11"]:
                if int(dia) <= 30:
                    return True
                return False
            if mes in ["2", "02"]:
                if bisiesto == "no":
                    if int(dia) <= 28:
                        return True
                    return False
                if bisiesto == "si":
                    if int(dia) <= 29:
                        return True
    return False


def hora_valida(hora):
    # retorna si la hora ingresada es valida:
    # "hora:minuto:segundo" y que sean digitos
    if hora.find("-") != -1:  # si esque hay valores negativos, no es valida
        return False
    triplete = hora.split(":")
    if len(triplete) == 3:
        hora = triplete[0]
        minuto = triplete[1]
        segundo = triplete[2]
        if hora.isdigit() and minuto.isdigit() and segundo.isdigit():
            if int(hora) <= 23 and int(minuto) <= 59 and int(segundo) <= 59:
                return True
    return False

################################################
################################################

# Menú

# Interaccion

menu_actions = {}


# =======================
#     MENUS FUNCTIONS
# =======================

# Main menu
def main_menu():
    print("=========================")
    print("Bienvenido a SuperLuchin")
    print("=========================\n")
    print("LogIn\n")
    global input_usuario  # es necesario????????????????
    input_usuario = input("Usuario: ")
    input_constrasena = input("Constrasena: ")
    if usuario_valido(input_usuario) and constrasena_valida(input_constrasena):
        global identificador_usuario
        identificador_usuario = objeto_usuario(input_usuario).ide
        ejecutar_menu(1)
    else:
        print("LogIn no valido, ingrese nuevamente.")
        ejecutar_menu('')
    return

# Execute menu


def ejecutar_menu(choice):
    if choice == '':
        menu_actions['main_menu']()
    elif choice == 'ANAF':
        menu_actions['ANAF']()
    elif choice == 'piloto/jefe':
        menu_actions['piloto/jefe']()
    elif choice == '9':
        menu_actions['9']()
    elif choice == '0':
        menu_actions['0']()
    else:
        menu_actions['fecha/hora']()
    return


# Menu 1
def menu1():
    print("=========================")
    print("Bienvenido, {} [id: {}]\n".format(input_usuario, identificador_usuario))

    input_fecha = "fecha invalida"
    while fecha_valida(input_fecha) == False:            # ??????????????
        input_fecha = input("Ingrese fecha (año-mes-dia): ")
        if fecha_valida(input_fecha) == False:
            print("fecha no valida, ingrese nuevamente...")

    input_hora = "hora invalida"
    while hora_valida(input_hora) == False:  # ??????????????
        input_hora = input("Ingrese hora (hora:min:seg): ")
        if hora_valida(input_hora) == False:
            print("hora no valida, ingrese nuevamente...")

    if hora_valida(input_hora) and fecha_valida(input_fecha):
        # despliege de menus diferenciados en funcion del recurso perteneciente
        global identificador_recurso
        identificador_recurso = objeto_usuario(input_usuario).recurso_id
        if identificador_recurso == "":  # el usuario es de la ANAF
            ejecutar_menu('ANAF')
        else:  # el usuario es piloto/jefe
            ejecutar_menu('piloto/jefe')
    else:
        print("fecha y/u hora no valida, ingrese nuevamente...")
        ejecutar_menu('fecha/hora')
    return


# Menu 2
def menu2():
    print("=========================")
    print("       >Menu ANAF<")
    print("    Usario: {}".format(input_usuario))
    print("=========================")
    # delegan recursos, tienen info actualizada

    print("Elija un comando: \n")
    print("[1] Consultar Incendios")
    print("[2] Consultar Recursos")
    print("[3] Consultar Usuarios\n")
    print("[4] Crear Nuevo Usuario")
    print("[5] Agregar Pronostico Meteorologico")
    print("[6] Agregar Nuevo Incendio\n")
    print("[9] LogOut")
    print("[0] Quit")
    choice = input(" >>  ")
    ejecutar_menu(choice)
    return


# Menu 2
def menu3():
    print("================================")
    print("identificador de recurso: ", identificador_recurso)
    print("tipo de recurso asignado al usuario: ", objeto_recurso(identificador_recurso).tipo)
    # SABER SI ES PILOTO O JEFE
    # HACER FUNCION EXTERNA QUE LO HAGA, EL RETORNO LO LLAMO EN EL MENU DE ACA
    # UNA VEZ QUE SABEMOS EL TIPO DE RECURSO, SERA DISTINTO LA BARRA DE ESTADO
    print(" ______________________________ ")
    print("|        BARRA DE ESTADO       |")
    print("|______________________________|")
    print("Menu 3: usuario PILOTO o BRIGDADA o BOMBEROS !\n")
    print("9. Back")
    print("0. Quit")
    choice = input(" >>  ")
    ejecutar_menu(choice)
    return


# Back to main menu
def back():
    menu_actions['main_menu']()


# Exit program
def salir():
    sys.exit()


# =======================
#    MENUS DEFINITIONS
# =======================

# Menu definition
menu_actions = {'main_menu': main_menu, 'fecha/hora': menu1, 'ANAF': menu2,
                'piloto/jefe': menu3, '9': back, '0': salir}

# =======================
#      MAIN PROGRAM
# =======================

# Main Program
if __name__ == "__main__":
    # Launch main menu
    main_menu()
