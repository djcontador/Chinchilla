import random
from lector_parametros import Variables
variables = Variables()
matriz_nota_esperada = variables.matriz_nota_esperada
dificultad = variables.diccionario_dificultad


def nota_esperada(contenido, hs, matriz_notas_esperadas):
    horas = int(hs)
    intervalo_horas = matriz_notas_esperadas[contenido]
    rango_horas = list(filter(lambda rango: horas in rango, intervalo_horas))
    if len(rango_horas) == 0:
        intervalo_notas = matriz_notas_esperadas['header'][3]
    else:
        for i in range(4):
            if matriz_notas_esperadas[contenido][i] == rango_horas[0]:
                intervalo_notas = matriz_notas_esperadas['header'][i]
    nota = random.uniform(float(intervalo_notas[0]), float(intervalo_notas[1]))
    return round(nota, 1)


print(nota_esperada('1', 4.6, matriz_nota_esperada))



