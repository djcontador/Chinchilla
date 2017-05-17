import random
from evaluaciones import Tarea, Control, Actividad, Examen


class Alumno:
    """
    Esta clase representa un alumno del curso avanzacion programada
    """
    _id = 0
    personalidades = ['eficiente', 'artistico', 'teorico']

    def __init__(self, nombre, seccion, creditaje, dificultad):
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
        """
        self.id = Alumno._id
        Alumno._id += 1
        self.nombre = nombre
        self.seccion = seccion
        self.creditaje = creditaje
        self.dificultad = dificultad
        self.personalidad = random.choice(Alumno.personalidades)
        self.portafolio = {'tareas': [], 'actividades': [], 'controles': [], 'examen': []}
        self.rendimiento = {'contenido1': 0, 'contenido2': 0}  # arreglar

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

    def h(self):
        """
        Calcula la cantidad de horas disponibles para dedicarle al ramo durante la semana,
        esta en funcion de la cantidad de creditos tomados
        :return: Cantidad de horas disponibles para la semana
        :rtype: float
        """
        if self.creditos == 'prob_40_creditos':
            return random.uniform(10, 25)
        elif self.creditos == 'prob_50_creditos':
            return random.uniform(10, 15)
        elif self.creditos == 'prob_55_creditos':
            return random.uniform(5, 15)
        else:
            return random.uniform(5, 10)

    #@property
    #def estudiar(self, contenido, creditos):
    #    pass

    # todo
    @property
    def confianza(self):
        pass

    # todo
    @property
    def nivel_programacion(self):
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

    @property
    def manejo_contenidos(self):
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
        return retorno

    @property
    def historial_hs(self):
        """
        permite obtener cuantas horas de estudio le dedico el alumno a cada contenido a lo
        largo del semestre
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
        print("horas estudiadas para esta evaluacion: {}".format(horas))
        intervalo_horas = matriz_notas_esperadas[key_contenido]
        rango_horas = list(filter(lambda rango: horas in rango, intervalo_horas))
        if len(rango_horas) == 0:
            intervalo_notas = matriz_notas_esperadas['header'][3]
        else:
            for i in range(4):
                if matriz_notas_esperadas[key_contenido][i] == rango_horas[0]:
                    intervalo_notas = matriz_notas_esperadas['header'][i]
        nota = random.uniform(float(intervalo_notas[0]), float(intervalo_notas[1]))

        print("nota esperada: ", round(nota, 1))
        evaluacion.nota_esperada = round(nota, 1)

        if isinstance(evaluacion, Tarea):
            self.portafolio['tareas'].append(evaluacion)
        elif isinstance(evaluacion, Control):
            self.portafolio['controles'].append(evaluacion)
        elif isinstance(evaluacion, Actividad):

            self.portafolio['actividades'].append(evaluacion)
        elif isinstance(evaluacion, Examen):
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
