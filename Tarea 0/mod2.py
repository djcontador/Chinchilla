import sys
import os
from mod1 import Importar, Exportar
from funcionesmenu import Objeto, Validar, Menu

print("hola modulo 2")


# funciones de barra de estado
def titulo_usuario(tipo):
    if tipo == "AVION":
        return "Piloto de avion"
    elif tipo == "HELICOPERO":
        return "Piloto de helicoptero"
    elif tipo == "BRIGADA":
        return "Jefe de brigada"
    elif tipo =="BOMBEROS":
        return "Jefe de bomberos"
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
    Importar().incendios()
    Importar().meteorologia()
    Importar().recursos()
    Importar().usuarios()

    print("=========================")
    print("Bienvenido a SuperLuchin")
    print("=========================\n")
    print("LogIn\n")
    global input_usuario  # es necesario????????????????
    input_usuario = input("Usuario: ")
    input_constrasena = input("Constrasena: ")
    if Validar().usuario(input_usuario) and Validar().constrasena(input_constrasena):
        global identificador_usuario
        identificador_usuario = Objeto().usuario(input_usuario).ide
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


# Menu 1: fecha/hora
def menu1():
    print("=========================")
    print("Bienvenido, {} [id: {}]\n".format(input_usuario,
                                             identificador_usuario))

    input_fecha = "fecha invalida"
    while Validar().fecha(input_fecha) == False:            # ??????????????
        input_fecha = input("\nIngrese fecha (año-mes-dia): ")
        if Validar().fecha(input_fecha) == False:
            print("fecha no valida, ingrese nuevamente...")

    input_hora = "hora invalida"
    while Validar().hora(input_hora) == False:  # ??????????????
        input_hora = input("\nIngrese hora (hora:min:seg): ")
        if Validar().hora(input_hora) == False:
            print("hora no valida, ingrese nuevamente...")

    if Validar().hora(input_hora) and Validar().fecha(input_fecha):
        # despliege de menus diferenciados en funcion del recurso perteneciente
        global identificador_recurso
        identificador_recurso = Objeto().usuario(input_usuario).recurso_id
        if identificador_recurso == "":  # el usuario es de la ANAF
            ejecutar_menu('ANAF')
        else:  # el usuario es piloto/jefe
            ejecutar_menu('piloto/jefe')
    else:
        print("fecha y/u hora no valida, ingrese nuevamente...")
        ejecutar_menu('fecha/hora')
    return


# Menu 2: ANAF
def menu2():
    print("=========================")
    print("       >Menu ANAF<")
    print("    Usario: {}".format(input_usuario))
    print("=========================")
    # delegan recursos, tienen info actualizada

    print("Elija un comando: \n")
    print("1. Consultar Incendios")
    print("2. Consultar Recursos")
    print("3. Consultar Usuarios\n")
    print("4. Crear Nuevo Usuario")
    print("5. Agregar Pronostico Meteorologico")
    print("6. Agregar Nuevo Incendio\n")
    print("9. LogOut")
    print("0. Quit")
    choice = input(" >>  ")
    Menu().menu_anaf(choice)
    ejecutar_menu('ANAF')
    #ejecutar_menu("ANAF", choice)
    return


# Menu 3: piloto/jefe
def menu3():
    print("================================")
    print("identificador de recurso: ", identificador_recurso)
    print("tipo de recurso asignado al usuario: ",
          Objeto().recurso(identificador_recurso).tipo)
    print(" ________________________________________________ ")
    print("  Barra de Estado: {} - {}      "
          "".format(input_usuario,
                    titulo_usuario(Objeto().recurso(identificador_recurso).tipo)))
    print(" ______________________________________________\n ")

    print("[1] Acceder a Mision")
    print("no ha sido asignado a ninguna mision (no ha sido movilizado)")

    print("\n9. LogOut")
    print("0. Quit")
    choice = input(" >>  ")
    ejecutar_menu(choice)
    return


# Back to main menu
def back():
    menu_actions['main_menu']()


# Exit program
def salir():
    Exportar().incendios()
    Exportar().meteorologia()
    Exportar().recursos()
    Exportar().usuarios()
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
