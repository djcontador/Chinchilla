import random
from evaluaciones import Tarea, Control, Actividad, Examen
from functools import reduce


class Alumno:
    """
    Esta clase representa un alumno del curso avanzacion programada
    """
    _id = 0
    personalidades = ['eficiente', 'artistico', 'teorico']

    def __init__(self, nombre, seccion, creditaje, dificultad,
                 nivel_inicial_confianza_superior, nivel_inicial_confianza_inferior):
        """
        :param nombre: Nombre del alumno inscrito
        :type nombre: str
        :param seccion: Numero de la seccion en la que esta inscrito
        :type seccion: str
        :param creditaje: Lista de duplas probabilidad/cantidad_creditos_tomados
        :type creditaje: list
        :param dificultad: diccionario con el contenido como key, y el parametro dificultad como valor.
        (puede ser modificado a traves del archivo parametros.csv)
        :type dificultad: dict
        :param nivel_inicial_confianza_superior: cota superior para el random inicial de confianza
        :type nivel_inicial_confianza_superior: int
        :param nivel_inicial_confianza_inferior: cota inferior para e random inicial de confianza
        :type nivel_inicial_confianza_inferior: int
        """
        self.id = Alumno._id
        Alumno._id += 1
        self.nombre = nombre
        self.seccion = seccion
        self.creditaje = creditaje
        self.dificultad = dificultad
        self.confianza = random.uniform(nivel_inicial_confianza_inferior, nivel_inicial_confianza_superior)
        self.dicc_nivel_programacion = {'1': random.randint(2, 10)}
        self.personalidad = random.choice(Alumno.personalidades)
        self.portafolio = {'tareas': [], 'actividades': [], 'controles': [], 'examen': []}
        # promedio por cada semana
        # semana 1 : promedio
        self.promedio_semanal = {'tareas': [], 'actividades': [], 'examen': [], 'controles': []}
        self.rendimiento = {'contenido1': 0, 'contenido2': 0}  # arreglar
        self.visitas_profesor = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0,
                                 '7': 0, '8': 0, '9': 0, '10': 0, '11': 0, '12': 0}
        self.asistencias_fiesta = []
        self.estado = 'en curso'  # en curso, retirado, aprobado, reprobado
        self.promedio = {'1': None, '2': None, '3': None, '4': None, '5': None, '6': None, '7': None, '8': None,
                         '9': None, '10': None, '11': None, '12': None, '13': None, '14': None, '15': None, '16': None}


        # cantidad de creditos tomados
        x = random.random()
        prob_ordenada = sorted(self.creditaje)
        if x <= prob_ordenada[0][0]:
            creditos = prob_ordenada[0][1]
            self.creditos = creditos
        elif x <= (prob_ordenada[0][0] + prob_ordenada[1][0]):
            creditos = prob_ordenada[1][1]
            self.creditos = creditos
        elif x <= (prob_ordenada[0][0] + prob_ordenada[1][0] + prob_ordenada[2][0]):
            creditos = prob_ordenada[2][1]
            self.creditos = creditos
        else:
            creditos = prob_ordenada[3][1]
            self.creditos = creditos

        self.horas_disponibles = []
        #[(1, self.h()), (2, self.h()), (3, self.h()), (4, self.h()),
        #                          (5, self.h()), (6, self.h()), (7, self.h()), (8, self.h()),
        #                          (9, self.h()), (10, self.h()), (11, self.h()), (12, self.h())]
        self.manejo_contenidos = {}
        self.calculador_horas_disponibles()
        self.creador_manejo_contenidos()

    def h(self):
        """
        Calcula la cantidad de horas disponibles para dedicarle al ramo durante la semana,
        esta en funcion de la cantidad de creditos tomados
        :return: Cantidad de horas disponibles para la semana
        :rtype: float
        """
        if self.creditos == '40_creditos':
            return random.uniform(10, 25)
        elif self.creditos == '50_creditos':
            return random.uniform(10, 15)
        elif self.creditos == '55_creditos':
            return random.uniform(5, 15)
        else:
            return random.uniform(5, 10)

    def calculador_horas_disponibles(self):
        """
        crea una lista de duplas semana / cantidad horas disponibles, y las horas disponibles,
        que estan en funcion de la cantidad de creditos que tomo el alumno y si asistira o no a una fiesta
        esa semana.
        :return: lista de duplas semana / cantidad horas disponibles
        :rtype: list
        """
        lista = []
        for i in range(16):
            semana = i + 1
            if str(semana) in self.asistencias_fiesta:
                # como fue a fiesta, se quitan 2 dias de estudio de ese contenido (o semana)
                h_disponibles = self.h()
                h_disponibles_descontadas = (h_disponibles / 7) * 2
                h_reales = h_disponibles - h_disponibles_descontadas
                lista.append((semana, h_reales))
                # print("{0} disminuyo de {1} a {2} horas disponibles por asistir a fiesta en la semana {3}".format(self.nombre, h_disponibles, h_reales, semana))
            else:
                lista.append((semana, self.h()))
        self.horas_disponibles = lista

    def nivel_programacion(self, contenido):
        """
        Actualiza el atributo dicc_nivel_programacion con el nivel calculado para la semana correspondiente
        al contenido entregado, y modifica el nivel de programacion en funcion de las probabilidades v y w
        (si ocurrieron los eventos "reunirse con el profesor" o "el alumno va a una fiesta")
        :param contenido: numero del contenido que se evalua en la semana
        :type contenido: str
        :return: nivel de programación actual
        :rtype: float
        """

        if contenido == '1':
            if contenido in self.asistencias_fiesta:
                antiguo = self.dicc_nivel_programacion[contenido]
                self.dicc_nivel_programacion[contenido] = antiguo * 0.9
                return self.dicc_nivel_programacion[contenido]
            return self.dicc_nivel_programacion[contenido]

        else:
            if contenido in self.asistencias_fiesta:
                # descuento por asistir a una parranda (fiesta)
                nivel_antiguo = self.dicc_nivel_programacion[str(int(contenido) - 1)]
                nivel_nuevo = 1.05 * nivel_antiguo * (1 - 0.15)
                self.dicc_nivel_programacion[contenido] = nivel_nuevo
                return nivel_nuevo
            else:  # no hubo fiesta ni partido
                nivel_antiguo = self.dicc_nivel_programacion[str(int(contenido)-1)]
                nivel_nuevo = 1.05 * nivel_antiguo
                self.dicc_nivel_programacion[contenido] = nivel_nuevo
                return nivel_nuevo

    def creador_manejo_contenidos(self):
        """
        corresponde a un diccionario del manejo de contenidos para cada contenido
        :return: diccionario con el contenido como key
        :rtype: dict
        """
        # asumiendo que cada lunes parte una materia diferente
        retorno = {}
        for contenido in self.dificultad:
            d = self.dificultad[contenido]
            if contenido == '1':
                h_disponibles = self.horas_disponibles[0][1] * 0.3
                hs = (h_disponibles / 7) * 4
            else:
                indice = int(contenido) - 1
                h_disponibles_actual = self.horas_disponibles[indice][1] * 0.3
                h_disponibles_anterior = self.horas_disponibles[indice-1][1] * 0.3
                hs = (h_disponibles_anterior / 7) * 3 + (h_disponibles_actual / 7) * 4
            s_i = hs / d
            retorno[contenido] = s_i
        self.manejo_contenidos = retorno
        # return retorno

    @property
    def historial_hs(self):
        """
        permite obtener cuantas horas de estudio le dedico el alumno a cada contenido a lo
        largo del semestre, asumiendo que el cambio de contenidos es cada jueves.
        :return: diccionario con el contenido como key
        :rtype: dict
        """
        retorno = {}
        for contenido in self.dificultad:
            if contenido == '1':
                h_disponibles = self.horas_disponibles[0][1] * 0.3
                hs = (h_disponibles / 7) * 4
            else:
                indice = int(contenido) - 1
                h_disponibles_actual = self.horas_disponibles[indice][1] * 0.3
                h_disponibles_anterior = self.horas_disponibles[indice - 1][1] * 0.3
                hs = (h_disponibles_anterior / 7) * 3 + (h_disponibles_actual / 7) * 4
            retorno[contenido] = hs
        return retorno

    @property
    def historial_ht(self):
        """
        indica la cantidad de horas semanales dedicadas al desarrollo de tareas a lo largo del semestre
        :return: diccionario con el numero de semana como key
        (que concuerda con el numero de contenido visto en aquella semana)
        :rtype: dict
        """
        retorno = {}
        for contenido in self.dificultad:
            for indice in range(len(self.horas_disponibles)):
                if self.horas_disponibles[indice][0] == int(contenido):
                    retorno[contenido] = self.horas_disponibles[indice][1] * 0.7
        return retorno

    @property
    def nivel_programacion_promedio(self):
        pass

    def entregar_tarea(self, arg_numero, porcentaje_progreso_tarea_mail):
        """
        se calcula el progreso obtenido, y se aumenta el avance del alumno en funcion de su personalidad mediante la
        funcion progreso()
        :param arg_numero: numero de la tarea a entregar
        :return: retorna si se realiza la entrega o no, de realizarse retorna True, y si retorna False, es porque
        intentaran atrasar la entrega
        :rtype: bool
        """
        # calcular la nota esperada cuando tengan que entregar la tarea ******
        for tarea in self.portafolio['tareas']:
            if arg_numero == tarea.numero:
                key_contenido = tarea.contenido
                evaluacion = tarea
        nota_esperada_contenido_1 = None
        nota_esperada_contenido_2 = None
        for actividad in self.portafolio['actividades']:
            if actividad.contenido == key_contenido[0]:
                nota_esperada_contenido_1 = actividad.nota_esperada
            elif actividad.contenido == key_contenido[1]:
                nota_esperada_contenido_2 = actividad.nota_esperada
        nota_esperada = (nota_esperada_contenido_1 + nota_esperada_contenido_2) / 2
        evaluacion.nota_esperada = nota_esperada

        # definicion del progreso realizado para la tarea
        manejo_contenidos = (self.manejo_contenidos[key_contenido[0]] + self.manejo_contenidos[key_contenido[1]]) / 2
        horas_tarea = self.historial_ht[key_contenido[0]] + self.historial_ht[key_contenido[1]]
        evaluacion.progreso(manejo_contenidos, self.dicc_nivel_programacion[key_contenido[1]], horas_tarea, self.personalidad)

        # true o false si se quiere atrasar la entrega
        progreso_esperado = evaluacion.exigencia * porcentaje_progreso_tarea_mail
        progreso_realizado = evaluacion.progreso_total
        if progreso_realizado < progreso_esperado:
            print(self.nombre, " envia mail pidiendo mas plazo")
            return False
        elif progreso_realizado >= progreso_esperado:
            return True

    def rendir_evaluacion(self, evaluacion, matriz_notas_esperadas):
        """
        permite guardar todas las variables necesarias para el calculo de notas y estadisticas
        al momento en que ocurre el evento evaluacion. Se calcula la nota esperada, y se agrega la evaluacion
        al portafolio personal del alumno.
        :param evaluacion: instancia de alguna hija de Evaluacion
        :type evaluacion: object
        :param matriz_notas_esperadas: diccionario con el contenido como key, que contiene una lista con los rangos
        de horas necesarias para esperar un rango de notas determinado (cuadro 4 del enunciado). Este parametro puede
        ser modificado en parametros.csv
        :type matriz_notas_esperadas: dict
        :return:
        :rtype: None
        """
        key_contenido = evaluacion.contenido

        if not isinstance(evaluacion, Tarea):
            horas = int(self.historial_hs[key_contenido])
            intervalo_horas = matriz_notas_esperadas[key_contenido]

            rango_horas = list(filter(lambda rango: horas in rango, intervalo_horas))

            if len(rango_horas) == 0:
                intervalo_notas = matriz_notas_esperadas['header'][3]
            else:
                for i in range(4):
                    if matriz_notas_esperadas[key_contenido][i] == rango_horas[0]:
                        intervalo_notas = matriz_notas_esperadas['header'][i]
            nota = random.uniform(float(intervalo_notas[0]), float(intervalo_notas[1]))
            evaluacion.nota_esperada = round(nota, 1)

        # agregacion de la evaluacion al portafolio, asignacion del progreso
        # y de las bonificaciones por personalidad en las actividades
        if isinstance(evaluacion, Tarea):
            # solo se entrega la tarea al alumno en su portafolio, no se calcula el progreso aun
            self.portafolio['tareas'].append(evaluacion)

        elif isinstance(evaluacion, Control):
            evaluacion.progreso(self.manejo_contenidos[key_contenido],
                                self.dicc_nivel_programacion[key_contenido], self.confianza)
            self.portafolio['controles'].append(evaluacion)

        elif isinstance(evaluacion, Actividad):
            if self.personalidad == 'eficiente' and key_contenido in ['5', '8']:
                evaluacion.bonificacion_personalidad = 1
            elif self.personalidad == 'artistico' and key_contenido in ['9', '12']:
                evaluacion.bonificacion_personalidad = 1
            elif self.personalidad == 'teorico' and key_contenido in ['6']:
                evaluacion.bonificacion_personalidad = 1

            # seteo del progreso total del la evaluacion
            evaluacion.progreso(self.manejo_contenidos[key_contenido],
                                self.dicc_nivel_programacion[key_contenido], self.confianza)
            # adhesion al portafolio personal
            self.portafolio['actividades'].append(evaluacion)

        elif isinstance(evaluacion, Examen):
            if self.personalidad == 'teorico':
                evaluacion.bonificacion_personalidad = 1
            # evaluacion.progreso
            self.portafolio['examen'].append(evaluacion)



class AyudanteTareas:
    def __init__(self, nombre):
        self.nombre = nombre

    def corregir(self, evaluacion):
        pass


class AyudanteDocente:
    def __init__(self, nombre):
        self.nombre = nombre
        self.contenidos_dominados = random.sample([str(i+1) for i in range(12)], 3)

    def corregir(self, alumno, evaluacion):
        """
        calcula la nota obtenida en la evaluacion, y actualiza el promedio del alumno que lleva hasta el momento
        :param alumno: objeto alumno que esta cursando avanzacion programada
        :type alumno: object
        :param evaluacion: objeto de evaluacion a corregir y calcular la nota, que fue rendido por el alumno
        :type evaluacion: object
        :return:
        :rtype: None
        """
        nota = max(((evaluacion.progreso_total/evaluacion.exigencia) * 7) + evaluacion.bonificacion_personalidad, 1)

        evaluacion.nota_real = nota

        # calculo del promedio actual
        semana_actual = ""
        promedio = None
        prom_actividades = 0
        prom_controles = 0
        prom_tareas = 0
        n_actividades_corregidas = 0
        n_controles_corregidos = 0
        n_tareas_corregidas = 0

        if len(alumno.portafolio['actividades']) > 0:
            for actividad in alumno.portafolio['actividades']:
                if alumno.nombre == "Daniela Contador":
                    print("actividad {}".format(actividad.tipo + " " + actividad.numero), actividad.nota_real)
                if actividad.nota_real:  # si esque la actividad fue corregida (si nota_real no es None)
                    prom_actividades += actividad.nota_real
                    n_actividades_corregidas += 1
            if n_actividades_corregidas > 0:
                prom_actividades /= n_actividades_corregidas

        if len(alumno.portafolio['controles']) > 0:
            for control in alumno.portafolio['controles']:
                if alumno.nombre == "Daniela Contador":
                    print("control {}".format(control.tipo + " " + control.numero), control.nota_real)
                if control.nota_real:
                    prom_controles += control.nota_real
                    n_controles_corregidos += 1
            if n_controles_corregidos > 0:
                prom_controles /= n_controles_corregidos

        if len(alumno.portafolio['tareas']) > 0:
            for tarea in alumno.portafolio['tareas']:
                if tarea.nota_real:
                    prom_tareas += tarea.nota_real
                    n_tareas_corregidas += 1
            if n_tareas_corregidas > 0:
                prom_tareas /= n_tareas_corregidas

        examen_corregido = 0

        if alumno.nombre == 'Daniela Contador':
            print(alumno.portafolio)
            print('prom act: ', prom_actividades)
            print('prom controles: ', prom_controles)
            print('prom tareas', prom_tareas)

        if examen_corregido == 0:
            if n_tareas_corregidas == 0 and n_controles_corregidos == 0:
                # solo tiene actividades
                promedio = prom_actividades
            elif n_tareas_corregidas == 0:
                # tiene actividades y controles
                promedio = (0.25 / 0.45) * prom_actividades + (0.2 / 0.45) * prom_controles
            elif n_controles_corregidos == 0:
                # tiene actividades y tareas
                promedio = (0.25 / 0.65) * prom_actividades + (0.4 / 0.65) * prom_tareas
        elif n_controles_corregidos == 0:
            # tiene actividades, tareas y examen
            promedio = (0.25 / 0.8) * prom_actividades + (0.4 / 0.8) * prom_tareas + \
                       (0.15 / 0.8) * alumno.portafolio['examen'].nota_real
        else:
            # tiene actividades, tareas, controles y examen
            promedio = 0.25 * prom_actividades + 0.4 * prom_tareas + 0.2 * prom_controles + \
                       0.15 * alumno.portafolio['examen'].nota_real

        #alumno.promedio = promedio
        #alumno.promedio[semana_actual] = promedio
        # aqui el alumno se entera de su nota, entonces varia su nivel de confianza

        if alumno.nombre == 'Daniela Contador':
            print("promedio total actual: ", alumno.promedio)











        pass


class Coordinador:
    def __init__(self, nombre):
        self.nombre = nombre

    def publicar_notas(self, evaluacion, secciones, dia):
        notas_reales = []
        notas_descontadas = []
        notas = {evaluacion: {'notas reales': notas_reales, 'notas descontadas': notas_descontadas, 'dia de entrega': dia}}

        # si las publica instantaneamente:
        for seccion in secciones:
            for alumno in secciones[seccion].alumnos:
                # publica notas, entonces el alumno publica su promedio
                pass
            pass
        pass

        # seccion 2

        # seccion 3
        pass


class Profesor:
    def __init__(self, nombre, seccion):
        self.nombre = nombre
        self.seccion = seccion

    def recibir_consultas(self, alumnos):
        pass


class Seccion:
    def __init__(self, profesor):
        self.profesor = profesor
        self.alumnos = []

    def agregar_alumno(self, alumno):
        self.alumnos.append(alumno)

    def eliminar_alumno(self, alumno):
        self.alumnos.remove(alumno)
