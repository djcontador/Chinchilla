import random
# from clases import Control, Actividad


def generador_eventos_fiesta(parametro_fiesta_mes):
    """
    calculo de que dias ocurrira una fiesta durante la simulacion, asumiendo que el semestre durara maximo 112 dias.
    Se creara un diccionario del evento, con keys descriptivos.
    :param parametro_fiesta_mes: parametro variable en escenarios.csv, que indica la tasa en que ocurre una fiesta
    en unidades de dia
    :return: lista de duplas dia/ diccionario del evento de la fiesta
    :rtype: list
    """
    suma = 1
    dias_fiesta = []
    semana_fiesta = []
    while suma < 112:
        x = int(round(random.expovariate(parametro_fiesta_mes), 0))
        suma += x
        if suma < 112:
            dias_fiesta.append(suma)
    for dia in dias_fiesta:
        if dia // 7 == dia / 7:
            semana = dia // 7
        else:
            semana = (dia // 7) + 1
        evento = {'evento': 'Fiesta', 'semana': str(semana), 'fecha': dia}
        semana_fiesta.append((dia, evento))
    return semana_fiesta

print(generador_eventos_fiesta(1/30))
# en funcion de los dias en que habra eventos no programados, se le pasa esa lista de dias mofidicados
# a cada generador en el init de la simulacion, y ahi se modifican las cosas
#

def generador_publicaciones_mavrakis():
    pass


def generador_eventos_tareas(dificultad):
    """
    genera todos los eventos tareas, que ocurren cada viernes
    :return: lista de duplas dia / tarea
    :rtype: list
    """
    contador = 1
    viernes = [5, 19, 33, 47, 61, 75]
    contenidos = [['1', '2'], ['3', '4'], ['5', '6'], ['7', '8'], ['9', '10'], ['11', '12']]
    lista_eventos = []
    for i in range(6):
        evento = {'evento': 'Tarea', 'contenidos': contenidos[i],
                  'dificultad': (dificultad[contenidos[i][0]] + dificultad[contenidos[i][1]]) / 2,
                  'numero': str(contador), 'fecha_inicio': viernes[i],
                  'fecha_termino': viernes[i] + 14}
        entrega = {'evento': 'Entrega Tarea', 'contenidos': contenidos[i],
                   'dificultad': (dificultad[contenidos[i][0]] + dificultad[contenidos[i][1]]) / 2,
                   'numero': str(contador), 'fecha_inicio': viernes[i],
                   'fecha_termino': viernes[i] + 14}
        contador += 1
        lista_eventos.append((viernes[i], evento))
        lista_eventos.append((viernes[i] + 14, entrega))
    return lista_eventos


def generador_visitas_profesor():
    """
    genera una serie de duplas dia / diccionario de eventos visitas al profesor (lo que ocurre todos los lunes).
    :return: lista de duplas dia / diccionario de los eventos visitar al profesor.
    :rtype: list
    """
    eventos_consulta_profesor = []
    lunes = [(i*7 + 1) for i in range(12)]
    for dia in lunes:
        eventos_consulta_profesor.append((dia, {'evento': 'Visitar Profesor', 'fecha': dia}))
    return eventos_consulta_profesor


def generador_eventos_controles(dificultad):
    """
    genera una serie de duplas dia / diccionario del evento control, que se incorporará a la
    lista de eventos de la simulacion.
    :param dificultad: diccionario del parametro dificultad, con el contenido como llave y la dificultad como valor.
    :type dificultad: dict
    :return: lista de duplas dia / diccionario de actividades.
    :rtype: list
    """
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
        correccion = {'evento': 'Correccion Control', 'numero': numeros[contador], 'contenido': contenido, 'fecha': dia + 14}
        contador += 1
        eventos_controles.append((dia, evento))
        eventos_controles.append((dia + 14, correccion))
    return eventos_controles


def generador_eventos_actividades(dificultad):
    """
    genera una serie de duplas dia / diccionario del evento Actividad, que se incorporará a la
    lista de eventos de la simulacion.
    :param dificultad: diccionario del parametro dificultad, con el contenido como llave y la dificultad como valor
    :type dificultad: dict
    :return: lista de duplas dia / diccionario de actividades
    :rtype: list
    """
    eventos_actividades = []
    numeros = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    jueves_disponibles = [4, 11, 18, 25, 32, 39, 46, 53, 60, 67, 74, 81]
    indice = 0

    for jueves in jueves_disponibles:
        contenido = str(indice + 1)
        actividad = {'evento': 'Actividad', 'numero': numeros[indice], 'contenido': contenido,
                     'dificultad': dificultad[contenido], 'fecha': jueves}
        correccion = {'evento': 'Correccion Actividad', 'numero': numeros[indice], 'contenido': contenido, 'fecha': jueves + 14}
        eventos_actividades.append((jueves, actividad))
        eventos_actividades.append((jueves + 14, correccion))
        indice += 1
    return eventos_actividades


def ordenador_eventos(lista_duplas):
    """
    Ordena la lista de eventos de manera tal que al recorrerla, todos los eventos esten ordenados por dia y cada dia
    si hay multiples eventos, estos tambien estaran ordenados.
    :param lista_duplas: lista de duplas dia, diccionario descriptivo del evento, creada para cada
    simulacion
    :type lista_duplas: list
    :return: retorna la misma lista, pero ordenada por dia, y para un mismo dia
    primero ocurre un control, luego la actividad
    :rtype: list
    """
    eventos_ordenados = []  # tmb lista de duplas ordenadas
    guia = [i + 1 for i in range(100)]
    for dia in guia:
        eventos_diarios = []
        for dupla in lista_duplas:
            if dupla[0] == dia:
                eventos_diarios.append(dupla[1])
        if len(eventos_diarios) == 1:
            eventos_ordenados.append((dia, eventos_diarios[0]))
        else:
            # for para publicacion de notas mavrakis

            for evento in eventos_diarios:
                if evento['evento'] == 'Control':
                    eventos_ordenados.append((dia, evento))
            for evento in eventos_diarios:
                if evento['evento'] == 'Actividad':
                    eventos_ordenados.append((dia, evento))
            for evento in eventos_diarios:
                if evento['evento'] == 'Correccion Control':
                    eventos_ordenados.append((dia, evento))
            for evento in eventos_diarios:
                if evento['evento'] == 'Correccion Actividad':
                    eventos_ordenados.append((dia, evento))
            for evento in eventos_diarios:
                if evento['evento'] == 'Tarea':
                    eventos_ordenados.append((dia, evento))
            for evento in eventos_diarios:
                if evento['evento'] == 'Entrega Tarea':
                    eventos_ordenados.append((dia, evento))
            for evento in eventos_diarios:
                if evento['evento'] == 'Fiesta':
                    eventos_ordenados.append((dia, evento))
    return eventos_ordenados
