import sys
import os
from mod1 import Usuario, Meteorologia, Incendio, Recurso, Exportar


# Funciones que retornan los objetos de sus respectivos diccionarios
# despues ver si es util encontrar los objetos con otros parametros
class Objeto:
    # recibe id
    def incendio(self, dato):
        if str(type(dato)) == "<class 'int'>":  # si el dato es un numero
            return Incendio.dicc_incendios[dato]
        if dato.isdigit():  # si el dato es un string de un numero
            return Incendio.dicc_incendios[int(dato)]
        return False

    # recibe id
    def recurso(self, dato):
        if str(type(dato)) == "<class 'int'>":  # si el dato es un numero
            return Recurso.dicc_recursos[dato]
        if dato.isdigit():  # si el dato es un string de un numero
            return Recurso.dicc_recursos[int(dato)]
        return False

    # recibe id
    def meteorologia(self, dato):
        if str(type(dato)) == "<class 'int'>":  # si el dato es un numero
            return Meteorologia.dicc_meteorologia[dato]
        if dato.isdigit():  # si el dato es un string de un numero
            return Meteorologia.dicc_meteorologia[int(dato)]
        return False

    # recibe id y nombre
    def usuario(self, dato):
        if str(type(dato)) == "<class 'int'>":  # si el dato es un numero
            return Usuario.dicc_usuarios[dato]
        if dato.isdigit():  # si el dato es un string de un numero
            return Usuario.dicc_usuarios[int(dato)]
        for ide in Usuario.dicc_usuarios:  # si el dato es el nombre
            if Usuario.dicc_usuarios[ide].nombre == dato:
                return Usuario.dicc_usuarios[ide]
        return False


# Funciones que aseguran que los inputs sean correctos
class Validar:
    def usuario(self, nombre):
        # retorna si el nombre es valido (si esta dentro de la base de datos)
        lista_usuarios = []
        for id_usuario in Usuario.dicc_usuarios:
            lista_usuarios.append(Usuario.dicc_usuarios[id_usuario].nombre)
        if nombre in lista_usuarios:
            return True
        return False

    def constrasena(self, contrasena):
        # retorna si la constrasena es valida (si esta dentro de la base de datos)
        lista_constrasenas = []
        for id_usuario in Usuario.dicc_usuarios:
            lista_constrasenas.append(Usuario.dicc_usuarios[id_usuario].contrasena)
        if contrasena in lista_constrasenas:
            return True
        return False

    def fecha(self, fecha):
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

    def hora(self, hora):
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

    def fecha_hora(self, fecha_hora):
        # fecha_inicio en incendio
        # ano-mes-dia hora:min:seg
        dupla = fecha_hora.split(" ")
        if len(dupla) == 2:
            fecha = dupla[0]
            hora = dupla[1]
            if self.fecha(fecha) and self.hora(hora):
                return True
        return False


# funciones de barra de estado
def titulo_usuario(tipo):
    if tipo == "AVION":
        return "Piloto de avion"
    elif tipo == "HELICOPERO":
        return "Piloto de helicoptero"
    elif tipo == "BRIGADA":
        return "Jefe de brigada"
    elif tipo == "BOMBEROS":
        return "Jefe de bomberos"
    return False


# funciones de menu

class Menu:

    def menu_anaf(self, choice):
        if choice == '0':  # exit
            Exportar().incendios()
            Exportar().meteorologia()
            Exportar().recursos()
            Exportar().usuarios()
            sys.exit()

        elif choice == '1':  # consultar incendios
            pass

        elif choice == '2':  # consultar recursos
            pass

        elif choice == '3':  # consultar usuarios
            pass

        elif choice == '6':  # Agregar nuevo incendio
            lista_key = []
            for key in Incendio.dicc_incendios:
                lista_key.append(key)
            nuevo_ide = max(lista_key) + 1
            print("=========================")
            print("Creando nuevo Incendio\n")
            lat = input("Ingrese latitut: \n>> ")
            lon = input("Ingrese longitud: \n>>")
            potencia = input("Ingrese potencia: \n>>")
            fecha_inicio = "fecha_inicio invalida"

            while Validar().fecha_hora(fecha_inicio) == False:
                fecha_inicio = input("Ingrese fecha de inicio: \n"
                                     "(formato año-mes-dia hora:seg:min)\n>>  ")
                if Validar().fecha_hora(fecha_inicio) == False:
                    print("Fecha de inicio invalida, ingrese nuevamente...\n")

            Incendio(int(nuevo_ide), float(lat), float(lon), int(potencia),
                     fecha_inicio)
            print("\nIncendio({}, {}, {}, {}, {}) agregado exitosamente".format
                  (nuevo_ide, lat, lon, potencia, fecha_inicio))
            print("volviendo al menu ANAF ->")
            # volver al menu 2 (ANAF)


