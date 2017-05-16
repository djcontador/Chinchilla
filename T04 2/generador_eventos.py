import random


def generador_fecha_controles():
    opciones = [4, 11, 18, 25, 32, 39, 46, 53, 60, 67, 74, 81]

    def validar_fecha_controles(a, b, c, d, e):
        if b - a == 7 and c - b == 7:
            return False
        if c - b == 7 and d - c == 7:
            return False
        if d - c == 7 and e - d == 7:
            return False
        return True

    muestra = [4, 11, 18, 25, 32]
    while not validar_fecha_controles(muestra[0], muestra[1], muestra[2], muestra[3], muestra[4]):
        muestra = sorted(random.sample(opciones, 5))
    return muestra

print(generador_fecha_controles())



