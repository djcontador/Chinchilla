import random
from evaluaciones import Tarea, Control, Actividad, Examen
from lector_parametros import Variables
from lector_escenarios import Escenarios
variable = Variables()
escenario = Escenarios()
print(Escenarios.parametros_default)
print(escenario.escenarios)


class Alumno:
    """
    Esta clase representa un alumno del curso avanzacion programada
    """
    _id = 0
    personalidades = ['eficiente', 'artistico', 'teorico']

    def __init__(self, nombre, seccion, creditaje):
        """
        :param nombre: Nombre del alumno inscrito
        :type nombre: str
        :param seccion: Numero de la seccion en la que esta inscrito
        :type seccion: str
        :param creditaje: Lista de duplas probabilidad/cantidad_creditos_tomados
        :type creditaje: list
        """
        self.id = Alumno._id
        Alumno._id += 1
        self.nombre = nombre
        self.seccion = seccion
        self.creditaje = creditaje
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
        self.hs_anterior = 0
        self.hs_actual = self.h() * 0.3
        self.ht_anterior = 0
        self.ht_actual = 1 - self.hs_actual
        self.historial_horas_semanales = [self.hs_actual]

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


    @property
    def estudio_actual(self, contenido, creditos):
        pass

    @property
    def confianza(self):
        pass

    @property
    def progreso(self):
        pass

    @property
    def nivel_programacion(self):
        pass

    def actualizar_datos_semanales(self):
        """
        Actualiza los atributos de horas disponibles para tareas(ht) y contenidos(hs),
        es decir, calcula cuantas horas puede dedicarle a la semana actual, y setea lo
        que fue calculado para la semana anterior
        :return: ??????????????????????????????????????????????????????????????????????????????????????????????????
        :rtype: None
        """
        self.hs_anterior = self.hs_actual
        self.hs_actual = self.h() * 0.3
        self.historial_horas_semanales.append(self.hs_actual)
        self.ht_anterior = self.ht_actual
        self.ht_actual = 1 - self.hs_actual

    def manejo_contenidos(self, dia, contenido, dificultad):
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

    def rendir_evaluacion(self, evaluacion):
        """
        permite guardar todas las variables necesarias para el calculo de notas y estadisticas
        al momento en que ocurre el evento evaluacion
        :param evaluacion: instancia de alguna hija de Evaluacion
        :type evaluacion: object
        :return:
        :rtype: None
        """
        if isinstance(evaluacion, Tarea):
            self.portafolio['tareas'].append(evaluacion)
        elif isinstance(evaluacion, Control):
            self.portafolio['controles'].append(evaluacion)
        elif isinstance(evaluacion, Actividad):
            self.portafolio['actividades'].append(evaluacion)
        elif isinstance(evaluacion, Examen):
            self.portafolio['examen'].append(evaluacion)


class Ayudante:
    def __init__(self, nombre):
        self.nombre = nombre

    def corregir(self, evaluacion):
        pass


class Coordinador:
    def __init__(self, nombre):
        self.nombre = nombre

    def publicar_notas(self, notas):
        pass


class Seccion:
    def __init__(self, profesor):
        self.profesor = profesor
        self.alumnos = []

    def agregar_alumno(self, alumno):
        self.alumnos.append(alumno)

    def eliminar_alumno(self, alumno):
        self.alumnos.remove(alumno)


class Semestre:
    """
    Esta clase corresponde a la simulacion de el tanscurso de un semestre
    permite que en cada instancia se simule un semestre distinto
    """
    def __init__(self, escenario=None):
        """
        :param escenario: key de la base de datos escenarios.csv que indica el escenario con que
        se quiere realizar la simulacion del semestre ('escenario_1, escenario_27, etc)
        :type escenario: str
        """
        self.ayudantes = []
        self.secciones = []
        self.contenidos = []
        self.escenario = escenario  # si hay un escenario se cambiaran

        # parametros de base de datos
        self.matriz_nota_esperada = variable.matriz_nota_esperada
        self.diccionario_dificultad = variable.diccionario_dificultad

        # estadisticas
        self.botar_ramo = 0
        self.confianza_i = None
        self.confianza_f = None
        self.dicc_aprobacion = {}
        self.rendimiento = {'tareas': [], 'actividades': [], 'examen': []}

    # parametros en escenarios.csv
    @property
    # usar self.creditaje para crear alumnos
    def creditaje(self):
        if self.escenario == None:
            retorno = [(Escenarios.parametros_default['prob_40_creditos'], '40_creditos'),
                       (Escenarios.parametros_default['prob_50_creditos'], '50_creditos'),
                       (Escenarios.parametros_default['prob_55_creditos'], '55_creditos'),
                       (Escenarios.parametros_default['prob_60_creditos'], '60_creditos')]
            return retorno
        else:
            retorno = [(escenario.escenarios[escenario]['prob_40_creditos'], '40_creditos'),
                       (escenario.escenarios[escenario]['prob_50_creditos'], '50_creditos'),
                       (escenario.escenarios[escenario]['prob_55_creditos'], '55_creditos'),
                       (escenario.escenarios[escenario]['prob_60_creditos'], '60_creditos')]
            return retorno

    @property
    def prob_visitar_profesor(self):
        if self.escenario == None:
            return Escenarios.parametros_default['prob_visitar_profesor']
        else:
            return escenario.escenarios[self.escenario]

    # properties
    @property
    def prob_atraso_notas_mavrakis(self):
        if self.escenario == None:
            return Escenarios.parametros_default['prob_atraso_notas_Mavrakis']
        else:
            return escenario.escenarios[self.escenario]

    #todo
    # hacer lo mismo con estos otros y revisar condicional booleano "if not None"
    #self.porcentaje_progreso_tarea_mail = Escenarios.parametros_default['porcentaje_progreso_tarea_mail']
    #self.fiesta_mes = Escenarios.parametros_default['fiesta_mes']
    #self.partido_futbol_mes = Escenarios.parametros_default['partido_futbol_mes']
    #self.nivel_inicial_confianza_inferior



# cargar default de Escenarios()
creditaje = [(Escenarios.parametros_default['prob_40_creditos'], '40_creditos'),
             (Escenarios.parametros_default['prob_50_creditos'], '50_creditos'),
             (Escenarios.parametros_default['prob_55_creditos'], '55_creditos'),
             (Escenarios.parametros_default['prob_60_creditos'], '60_creditos')]


y = [Alumno('x', '1', creditaje) for x in range(10)]

print("################################")
for x in y:
    print(x.id, x.creditos, x.hs_actual)
    x.actualizar_datos_semanales()
    x.actualizar_datos_semanales()
    print(x.historial_horas_semanales)
    print("manejo de contenidos: ", x.manejo_contenidos(3, '1', variable.diccionario_dificultad))
    print("\n")
