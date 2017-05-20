import random
# from clases import Control, Actividad


def generador_eventos_controles(dificultad):
    contador = 0
    numeros = ['01', '02', '03', '04', '05']
    opciones = [11, 18, 25, 32, 39, 46, 53, 60, 67, 74, 81]
    cantidad = random.randint(0, 5)
    eventos_controles = []

    def validar_fecha_controles_5(a, b, c, d, e):
        if b - a == 7 and c - b == 7:
            return False
        if c - b == 7 and d - c == 7:
            return False
        if d - c == 7 and e - d == 7:
            return False
        return True

    def validar_fecha_controles_4(a, b, c, d):
        if b - a == 7 and c - b == 7:
            return False
        if c - b == 7 and d - c == 7:
            return False
        return True

    def validar_fecha_controles_3(a, b, c):
        if b - a == 7 and c - b == 7:
            return False
        return True

    if cantidad == 0:
        return eventos_controles
    elif cantidad == 5:
        muestra = [4, 11, 18, 25, 32]
        while not validar_fecha_controles_5(muestra[0], muestra[1], muestra[2], muestra[3], muestra[4]):
            muestra = sorted(random.sample(opciones, 5))
    elif cantidad == 4:
        muestra = [4, 11, 18, 25]
        while not validar_fecha_controles_4(muestra[0], muestra[1], muestra[2], muestra[3]):
            muestra = sorted(random.sample(opciones, 4))
    elif cantidad == 3:
        muestra = [4, 11, 18]
        while not validar_fecha_controles_3(muestra[0], muestra[1], muestra[2]):
            muestra = sorted(random.sample(opciones, 3))
    elif cantidad == 2:
        muestra = sorted(random.sample(opciones, 2))
    elif cantidad == 1:
        muestra = random.sample(opciones, 1)

    for dia in muestra:
        contenido = None
        for i, j in enumerate(opciones):
            if j == dia:
                contenido = str(i + 1)
        evento = {'evento': 'Control', 'numero': numeros[contador], 'contenido': contenido,
                  'dificultad': dificultad[contenido], 'fecha': dia}
        contador += 1
        eventos_controles.append((dia, evento))
    return eventos_controles


def generador_eventos_actividades(dificultad):
    eventos_actividades = []
    numeros = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    jueves_disponibles = [4, 11, 18, 25, 32, 39, 46, 53, 60, 67, 74, 81]
    indice = 0

    for jueves in jueves_disponibles:
        contenido = str(indice + 1)
        actividad = {'evento': 'Actividad', 'numero': numeros[indice], 'contenido': contenido,
                     'dificultad': dificultad[contenido], 'fecha': jueves}
        eventos_actividades.append((jueves, actividad))
        indice += 1
    return eventos_actividades

# ddificultad = {'12': 5, '5': 7, '2': 2, '3': 3, '4': 5, '11': 6, '8': 9, '7': 7, '10': 6, '1': 2, '6': 10, '9': 1}
