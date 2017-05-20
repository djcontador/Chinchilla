import random
from evaluaciones import Tarea, Control, Actividad, Examen


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
        self.rendimiento = {'contenido1': 0, 'contenido2': 0}  # arreglar
        self.visitas_profesor = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0,
                                 '7': 0, '8': 0, '9': 0, '10': 0, '11': 0, '12': 0}
        self.asistencias_fiesta = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0,
                                   '7': 0, '8': 0, '9': 0, '10': 0, '11': 0, '12': 0}
        self.estado = 'en curso'  # en curso, retirado, aprobado, reprobado

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

        # horas semanales disponibles
        # self.hs_anterior = 0
        # self.hs_actual = self.h() * 0.3
        # self.ht_anterior = 0
        # self.ht_actual = 1 - self.hs_actual
        # self.historial_horas_semanales = [self.hs_actual]

        self.horas_disponibles = [(1, self.h()), (2, self.h()), (3, self.h()), (4, self.h()),
                                  (5, self.h()), (6, self.h()), (7, self.h()), (8, self.h()),
                                  (9, self.h()), (10, self.h()), (11, self.h()), (12, self.h())]
        self.manejo_contenidos = {}
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

    def nivel_programacion(self, contenido, v=0, w=0):
        """
        Actualiza el atributo dicc_nivel_programacion con el nivel calculado para la semana correspondiente
        al contenido entregado, y modifica el nivel de programacion en funcion de las probabilidades v y w
        (si ocurrieron los eventos "reunirse con el profesor" o "el alumno va a una fiesta")
        :param contenido: numero del contenido que se evalua en la semana
        :type contenido: str
        :param v: probabilidad de que el alumna se reuna con el profesor
        :type v: float
        :param w: probabilidad de que el alumno vaya a una fiesta
        :type w: float
        :return: nivel de programación actual
        :rtype: float
        """
        if contenido == '1':
            return self.dicc_nivel_programacion[contenido]
        else:
            nivel_antiguo = self.dicc_nivel_programacion[str(int(contenido)-1)]
            nivel_nuevo = 1.05 * nivel_antiguo * (1 + v - w)
            self.dicc_nivel_programacion[contenido] = nivel_nuevo
            return nivel_nuevo
        pass

    #def actualizar_datos_semanales(self):
    #    """
    #    Actualiza los atributos de horas disponibles para tareas(ht) y contenidos(hs),
    #    es decir, calcula cuantas horas puede dedicarle a la semana actual, y setea lo
    #    que fue calculado para la semana anterior
    #    :return: ??????????????????????????????????????????????????????????????????????????????????????????????????
    ##    :rtype: None
     #   """
     #   self.hs_anterior = self.hs_actual
     #   self.hs_actual = self.h() * 0.3
     ##   self.historial_horas_semanales.append(self.hs_actual)
      ##  self.ht_anterior = self.ht_actual
       # self.ht_actual = 1 - self.hs_actual

    # no debe ser una property, porque no deja modificar en otras partes
    # hacer una funcion que me cree el diccionario manejor de contenidos, y luego guardarlo
    # en self.manejo_contenidos_
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

        # nota esperada
        horas = int(self.historial_hs[key_contenido])
        intervalo_horas = matriz_notas_esperadas[key_contenido]

        rango_horas = list(filter(lambda rango: horas in rango, intervalo_horas))

        if len(rango_horas) == 0:
            #print("puse en 7.0 ({0}) en el contenido {1}".format(matriz_notas_esperadas['header'][3], key_contenido))
            #print("intervalo_horas: ", matriz_notas_esperadas[key_contenido])
            intervalo_notas = matriz_notas_esperadas['header'][3]
        else:
            for i in range(4):
                if key_contenido == '4' and self.nombre == "Daniela Contador":
                    print("rango horas: ", rango_horas)
                    print("matriz_notas_esperadas[key_contenido][i]: ", matriz_notas_esperadas[key_contenido][i])

                if matriz_notas_esperadas[key_contenido][i] == rango_horas[0]:
                    intervalo_notas = matriz_notas_esperadas['header'][i]
                    if key_contenido == '4' and self.nombre == "Daniela Contador":
                        print("intervalo notas: ", intervalo_notas)
        nota = random.uniform(float(intervalo_notas[0]), float(intervalo_notas[1]))
        if self.nombre == "Daniela Contador":
            print("nota esperada: ", nota)
            print("en la evaluacion: ", evaluacion.numero)
        evaluacion.nota_esperada = round(nota, 1)
        if self.nombre == "Daniela Contador":
            print("NOTA ESPERAADAA:::: evaluacion {0}, tipo {1}, nota esperada: {2}, hs: {3}".format(evaluacion.numero,
                                                                                                    evaluacion.tipo,
                                                                                                    evaluacion.nota_esperada,
                                                                                                    self.historial_hs[evaluacion.contenido]))

        # agregacion de la evaluacion al portafolio, asignacion del progreso
        # y de las bonificaciones por personalidad
        if isinstance(evaluacion, Tarea):
            ####evaluacion.progreso(self.manejo_contenidos[key_contenido])
            # modificar funcion progreso para la tarea
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

    def corregir(self, evaluacion):
        pass


class Coordinador:
    def __init__(self, nombre):
        self.nombre = nombre

    def publicar_notas(self, notas, dia):
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
