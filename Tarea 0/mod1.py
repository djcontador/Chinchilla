# Tarea 2 - SuperLuchin
# Daniela Contador Zanforlin

# MODULO TRABAJO DE DATOS:
# trabajar con los datos y modificarlos en el programa (modificacion o
# actualizacion de diccionarios)

# para LLAMAR a un incendio ESPECIFICO: Incendio.dicc_incendios[ide]
# para llamar a sus ATRIBUTOS: Incendio.dicc_incendios[ide].atributo

# para CREAR un incendio;
# Incendio(ide, lat, lon, potencia, fecha_inicio)

# para MODIFICAR/ACTUALIZAR un incendio;
# Incendio(ide a modificar, modificar sus atributos deseados)


# funcion identificadora de orden de columnas en archivos CSV
def columna(dato, guia_columna):  # retorna posicion del dato en guia_columna[x]
    n_columna = 0
    for elemento in guia_columna:
        par = elemento.split(":")  # par = (dato, tipo)
        if par[0] == dato:
            return n_columna
        n_columna += 1


# escribe un diccionario de objetos tipo incendio
# a partir de la base de datos CSV
class Importar:

    def incendios(self):
        i = -1
        datos_incendios = open("incendios.csv")
        guia_columna = []
        for fila in datos_incendios:
            fila = fila.strip()  # quita "\n del string"
            lista_fila = fila.split(",")  # transforma string en lista
            if i == -1:
                guia_columna = lista_fila
            i += 1
            if lista_fila != guia_columna:  # evitar importar primera linea
                key_ide = lista_fila[columna("id", guia_columna)]  # orden num.
                lat = lista_fila[columna("lat", guia_columna)]
                lon = lista_fila[columna("lon", guia_columna)]
                potencia = lista_fila[columna("potencia", guia_columna)]
                fecha_inicio = lista_fila[columna("fecha_inicio", guia_columna)]
                Incendio(int(key_ide), float(lat), float(lon), int(potencia),
                         fecha_inicio)
        datos_incendios.close()

    def recursos(self):
        i = -1
        datos_recursos = open("recursos.csv")
        guia_columna = []
        for fila in datos_recursos:
            fila = fila.strip()
            lista_fila = fila.split(",")
            if i == -1:
                guia_columna = lista_fila
            i += 1
            if lista_fila != guia_columna:
                key_ide = lista_fila[columna("id", guia_columna)]
                tipo = lista_fila[columna("tipo", guia_columna)]
                velocidad = lista_fila[columna("velocidad", guia_columna)]
                lat = lista_fila[columna("lat", guia_columna)]
                lon = lista_fila[columna("lon", guia_columna)]
                autonomia = lista_fila[columna("autonomia", guia_columna)]
                delay = lista_fila[columna("delay", guia_columna)]
                tasa_extincion = lista_fila[columna("tasa_extincion",
                                                    guia_columna)]
                costo = lista_fila[columna("costo", guia_columna)]
                Recurso(int(key_ide), tipo, int(velocidad), float(lat),
                        float(lon), int(autonomia), int(delay),
                        int(tasa_extincion), int(costo))
        datos_recursos.close()

    def meteorologia(self):
        i = -1
        datos_meteorologia = open("meteorologia.csv")
        guia_columna = []
        for fila in datos_meteorologia:
            fila = fila.strip()
            lista_fila = fila.split(",")
            if i == -1:
                guia_columna = lista_fila
            i += 1
            if lista_fila != guia_columna:
                key_ide = lista_fila[columna("id", guia_columna)]
                fecha_inicio = lista_fila[columna("fecha_inicio", guia_columna)]
                fecha_termino = lista_fila[columna("fecha_termino",
                                                   guia_columna)]
                tipo = lista_fila[columna("tipo", guia_columna)]
                valor = lista_fila[columna("valor", guia_columna)]
                lat = lista_fila[columna("lat", guia_columna)]
                lon = lista_fila[columna("lon", guia_columna)]
                radio = lista_fila[columna("radio", guia_columna)]
                Meteorologia(int(key_ide), fecha_inicio, fecha_termino, tipo,
                             float(valor), float(lat), float(lon), int(radio))
        datos_meteorologia.close()

    def usuarios(self):
        i = -1
        datos_usuarios = open("usuarios.csv", encoding="utf-8")
        guia_columna = []
        for fila in datos_usuarios:
            fila = fila.strip()
            lista_fila = fila.split(",")
            if i == -1:
                guia_columna = lista_fila
            i += 1
            if lista_fila != guia_columna:
                key_ide = lista_fila[columna("id", guia_columna)]
                nombre = lista_fila[columna("nombre", guia_columna)]
                contrasena = lista_fila[columna("contraseÃ±a", guia_columna)]
                recurso_id = lista_fila[columna("recurso_id", guia_columna)]
                Usuario(int(key_ide), nombre, contrasena, recurso_id)
        datos_usuarios.close()


# crear archivos CSV tras cerrar el programa
class Exportar:

    def incendios(self):
        archivo = open("incendios.csv", "w")
        archivo.write("id:string,lat:float,lon:float,potencia:int,fecha_inicio:"
                      "string\n")  # siempre lo escribira en las mismas columnas
        for id_incendio in Incendio.dicc_incendios:
            ide = str(id_incendio) + ","
            lat = str(Incendio.dicc_incendios[id_incendio].lat) + ","
            lon = str(Incendio.dicc_incendios[id_incendio].lon) + ","
            potencia = str(Incendio.dicc_incendios[id_incendio].potencia) + ","
            f_inicio = str(Incendio.dicc_incendios[id_incendio].fecha_inicio)
            archivo.write(ide + lat + lon + potencia + f_inicio + "\n")
        archivo.close()

    def recursos(self):
        archivo = open("recursos.csv", "w")
        archivo.write("id:string,tipo:string,lat:float,lon:float,velocidad:int,"
                      "autonomia:int,delay:int,tasa_extincion:int,costo:int\n")
        for id_recurso in Recurso.dicc_recursos:
            ide = str(id_recurso) + ","
            tipo = str(Recurso.dicc_recursos[id_recurso].tipo) + ","
            lat = str(Recurso.dicc_recursos[id_recurso].lat) + ","
            lon = str(Recurso.dicc_recursos[id_recurso].lon) + ","
            velocidad = str(Recurso.dicc_recursos[id_recurso].velocidad) + ","
            autonomia = str(Recurso.dicc_recursos[id_recurso].autonomia) + ","
            delay = str(Recurso.dicc_recursos[id_recurso].delay) + ","
            t_ext = str(Recurso.dicc_recursos[id_recurso].tasa_extincion) + ","
            costo = str(Recurso.dicc_recursos[id_recurso].costo)
            archivo.write(ide + tipo + lat + lon + velocidad + autonomia + delay
                          + t_ext + costo + "\n")

    def meteorologia(self):
        archivo = open("meteorologia.csv", "w")
        archivo.write("id:string,fecha_inicio:string,fecha_termino:string,"
                      "tipo:string,valor:float,lat:float,lon:float,radio:int\n")
        for id_m in Meteorologia.dicc_meteorologia:
            ide = str(id_m) + ","
            f_inicio = str(Meteorologia.dicc_meteorologia[id_m].fecha_inicio
                           ) + ","
            f_termino = str(Meteorologia.dicc_meteorologia[id_m].fecha_termino
                            ) + ","
            tipo = str(Meteorologia.dicc_meteorologia[id_m].tipo) + ","
            valor = str(Meteorologia.dicc_meteorologia[id_m].valor) + ","
            lat = str(Meteorologia.dicc_meteorologia[id_m].lat) + ","
            lon = str(Meteorologia.dicc_meteorologia[id_m].lon) + ","
            radio = str(Meteorologia.dicc_meteorologia[id_m].radio) + ","
            archivo.write(ide + f_inicio + f_termino + tipo + valor + lat + lon
                          + radio + "\n")

    def usuarios(self):
        archivo = open("usuarios.csv", "w", encoding="utf-8")
        archivo.write("id:string,nombre:string,contraseÃ±a:string,"
                      "recurso_id:string\n")
        for id_u in Usuario.dicc_usuarios:
            ide = str(id_u) + ","
            nombre = str(Usuario.dicc_usuarios[id_u].nombre) + ","
            contrasena = str(Usuario.dicc_usuarios[id_u].contrasena) + ","
            recurso_id = str(Usuario.dicc_usuarios[id_u].recurso_id)
            archivo.write(ide + nombre + contrasena + recurso_id + "\n")


# Clases creadoras de objetos Incendio / Recurso / Meteorologia / Usuario
class Incendio:
    dicc_incendios = {}
    # dicc_incendios = {key_ide1: objeto_incendio1, key_ide2: objeto_incendio2}

    def __init__(self, ide, lat, lon, potencia, fecha_inicio):
        self.ide = ide
        self.lat = lat
        self.lon = lon
        self.potencia = potencia
        self.fecha_inicio = fecha_inicio
        self.puntos_de_poder = 0
        Incendio.dicc_incendios[ide] = self


class Recurso:
    dicc_recursos = {}

    def __init__(self, ide, tipo, velocidad, lat, lon, autonomia, delay,
                 tasa_extincion, costo):
        self.ide = ide
        self.tipo = tipo
        self.velocidad = velocidad
        self.lat = lat
        self.lon = lon
        self.autonomia = autonomia
        self.delay = delay
        self.tasa_extincion = tasa_extincion
        self.costo = costo
        Recurso.dicc_recursos[ide] = self


class Meteorologia:
    dicc_meteorologia = {}

    def __init__(self, ide, fecha_inicio, fecha_termino, tipo, valor,
                 lat, lon, radio):
        self.ide = ide
        self.fecha_inicio = fecha_inicio
        self.fecha_termino = fecha_termino
        self.tipo = tipo
        self.valor = valor
        self.lat = lat
        self.lon = lon
        self.radio = radio
        Meteorologia.dicc_meteorologia[ide] = self


class Usuario:
    dicc_usuarios = {}

    def __init__(self, ide, nombre, contrasena, recurso_id):
        self.ide = ide
        self.nombre = nombre
        self.contrasena = contrasena
        self.recurso_id = recurso_id
        Usuario.dicc_usuarios[ide] = self


# constante actualizacion de datos tras llamar el modulo
if __name__ == "__main__":
    Importar().incendios()
    Importar().meteorologia()
    Importar().recursos()
    Importar().usuarios()

    Exportar().incendios()
    Exportar().meteorologia()
    Exportar().recursos()
    Exportar().usuarios()
    print("mod1.py se ha corrido directamente")
else:
    Importar().incendios()
    Importar().meteorologia()
    Importar().recursos()
    Importar().usuarios()
    print("mod1.py ha sido importado en otro modulo")




