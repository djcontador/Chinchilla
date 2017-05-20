import random


class Evaluacion:
    """
    Corresponde a todas las clases madres de las evaluaciones, crea los atributos necesarios
    para reconocer el rendimiento y la asignacion de notas para los alumnos
    """
    def __init__(self, numero, contenido, dificultad, fecha):
        """
        :param numero: numero de la evaluacion. Por ejemplo: Tarea 01, Control 07, etc.
        :type numero: str
        :param contenido: identificador del contenido a evaluar en aquella evaluacion. Los contenidos se encuentran
        enumerados del 1 al 12 en funcion del cuadro 3 del enunciado.
        :type contenido: str
        :param dificultad: parametro obtenido de Parametros_dificultad.csv que indica la dificultad del contenido
        :type dificultad: int
        :param fecha: dia del semestre en que ocurre el evento evaluacion
        :type fecha: int
        """
        self.numero = numero
        self.contenido = contenido
        self.dificultad = dificultad
        self.fecha = fecha

        self.bonificacion_personalidad = 0
        self.nota_esperada = None
        self.nota_real = None
        self.progreso_total = None


class Actividad(Evaluacion):
    def __init__(self, numero, contenido, dificultad, fecha):
        super().__init__(numero, contenido, dificultad, fecha)
        self.tipo = 'actividad'

    def progreso(self, manejo_contenidos, nivel_programacion, confianza):
        progreso_pep8 = 0.7 * manejo_contenidos + 0.2 * nivel_programacion + 0.1 * confianza
        progreso_funcionalidad = 0.3 * manejo_contenidos + 0.6 * nivel_programacion + 0.1 * confianza
        progreso_contenidos = 0.7 * manejo_contenidos + 0.2 * nivel_programacion + 0.1 * confianza
        self.progreso_total = 0.4 * progreso_funcionalidad + 0.4 * progreso_contenidos + 0.2 * progreso_pep8


class Tarea(Evaluacion):
    def __init__(self, numero, contenido, dificultad, fecha):
        super().__init__(numero, contenido, dificultad, fecha)
        self.tipo = 'tarea'

    def progreso(self, manejo_contenidos, nivel_programacion, horas_tarea):
        progreso_pep8 = 0.5 * horas_tarea + 0.5 * nivel_programacion
        progreso_contenidos = 0.7 * manejo_contenidos + 0.1 * nivel_programacion + 0.2 * horas_tarea
        progreso_funcionalidad = 0.5 * manejo_contenidos + 0.1 * nivel_programacion + 0.4 * horas_tarea
        self.progreso_total = 0.4 * progreso_funcionalidad + 0.4 * progreso_contenidos + 0.2 * progreso_pep8


class Control(Evaluacion):
    def __init__(self, numero, contenido, dificultad, fecha):
        super().__init__(numero, contenido, dificultad, fecha)
        self.tipo = 'control'

    def progreso(self, manejo_contenidos, nivel_programacion, confianza):
        progreso_contenido = 0.7 * manejo_contenidos + 0.05 * nivel_programacion + 0.25 * confianza
        progreso_funcionalidad = 0.3 * manejo_contenidos + 0.2 * nivel_programacion + 0.5 * confianza
        self.progreso_total = 0.3 * progreso_funcionalidad + 0.7 * progreso_contenido


# todo
class Examen(Evaluacion):
    def __init__(self, numero, contenido, dificultad, fecha):
        super().__init__(numero, contenido, dificultad, fecha)
        self.tipo = 'examen'
        # en este caso el contenido es una lista de contenidos en funcion de lo pedido [('3'), ('6')]

# recordar setear la dificultad por 'parametros_dificultad.csv'
actividades = [(4, Actividad('01', '1', 2, 4)), (11, Actividad('02', '2', 2, 11)), (18, Actividad('03', '3', 3, 18)),
               (25, Actividad('04', '4', 5, 25)), (32, Actividad('05', '5', 7, 32)), (39, Actividad('06', '6', 10, 39))]
