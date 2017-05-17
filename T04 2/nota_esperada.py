import random
from lector_parametros import Variables
variables = Variables()
matriz_nota_esperada = variables.matriz_nota_esperada
dificultad = variables.diccionario_dificultad
print(matriz_nota_esperada)


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


def manejo_contenidos(dia, contenido, dificultad):
    """
    Calcula la cantidad de manejo de contenidos para un contenido en especifico, y para un dia
    de la semana (asumiendo que el contenido se trabaja maximo en una semana)
    :param dia: Numero del 1 al 7 que indica el dia de la semana que se quiere obtener el estado
    del manejo de contenidos de la semana hasta aquel entonces
    (lunes = 1, martes = 2, miercoles = 3, jueves = 4, viernes = 5, sabado = 6, domingo = 7)
    :type dia: int
    :param contenido: ID del contenido a desarrollar durante la semana
    :type contenido: str
    :param dificultad: Diccionario con el numero del contenido como key, y su valor es la dificultad
    :type dificultad: dict
    :return: cantidad de manejo del contenido semanal hasta ese dia
    :rtype: float
    """
    d = dificultad[contenido]
    if dia in [5, 6, 7]:
        return ((self.hs_anterior / 7) * (dia - 4)) / d
    elif dia in [1, 2, 3, 4]:
        return ((self.hs_anterior / 7) * 3 + (self.hs_actual / 7) * dia) / d
