import random


class Evaluacion:
    """
    Corresponde a todas las clases madres de las evaluaciones, crea los atributos necesarios
    para reconocer el rendimiento y la asignacion de notas para los alumnos
    """
    def __init__(self, numero, contenido, dificultad, fecha, exigencia):
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
        :param exigencia: nivel de progreso minimo para obtener un 7 en la evaluacion, seteado por los ayudantes
        docentes al reunirse antes de la actividad.
        :type exigencia: float
        """
        self.numero = numero
        self.contenido = contenido
        self.dificultad = dificultad
        self.fecha = fecha

        self.bonificacion_personalidad = 0
        self.nota_esperada = None
        self.nota_real = None
        self.progreso_total = None
        self.exigencia = exigencia


class Actividad(Evaluacion):
    def __init__(self, numero, contenido, dificultad, fecha, exigencia):
        super().__init__(numero, contenido, dificultad, fecha, exigencia)
        self.tipo = 'actividad'
        self.categoria = 'actividades'

    def progreso(self, manejo_contenidos, nivel_programacion, confianza):
        progreso_pep8 = 0.7 * manejo_contenidos + 0.2 * nivel_programacion + 0.1 * confianza
        progreso_funcionalidad = 0.3 * manejo_contenidos + 0.6 * nivel_programacion + 0.1 * confianza
        progreso_contenidos = 0.7 * manejo_contenidos + 0.2 * nivel_programacion + 0.1 * confianza
        self.progreso_total = 0.4 * progreso_funcionalidad + 0.4 * progreso_contenidos + 0.2 * progreso_pep8


class Tarea(Evaluacion):
    def __init__(self, numero, contenido, dificultad, fecha, exigencia, fecha_termino):
        super().__init__(numero, contenido, dificultad, fecha, exigencia)
        self.tipo = 'tarea'
        self.categoria = 'tareas'
        self.fecha_termino = fecha_termino

    def progreso(self, manejo_contenidos, nivel_programacion, horas_tarea, personalidad):
        if personalidad == 'eficiente':
            progreso_pep8 = (0.5 * horas_tarea + 0.5 * nivel_programacion) * 1.1
            progreso_contenidos = (0.7 * manejo_contenidos + 0.1 * nivel_programacion + 0.2 * horas_tarea) * 1.1
            progreso_funcionalidad = (0.5 * manejo_contenidos + 0.1 * nivel_programacion + 0.4 * horas_tarea) * 1.1
            self.progreso_total = 0.4 * progreso_funcionalidad + 0.4 * progreso_contenidos + 0.2 * progreso_pep8
        elif personalidad == 'artistico':
            progreso_pep8 = (0.5 * horas_tarea + 0.5 * nivel_programacion) * 1.2
            progreso_contenidos = 0.7 * manejo_contenidos + 0.1 * nivel_programacion + 0.2 * horas_tarea
            progreso_funcionalidad = 0.5 * manejo_contenidos + 0.1 * nivel_programacion + 0.4 * horas_tarea
            self.progreso_total = 0.4 * progreso_funcionalidad + 0.4 * progreso_contenidos + 0.2 * progreso_pep8
        elif personalidad == 'teorico':
            progreso_pep8 = (0.5 * horas_tarea + 0.5 * nivel_programacion) * 0.9
            progreso_contenidos = (0.7 * manejo_contenidos + 0.1 * nivel_programacion + 0.2 * horas_tarea) * 0.9
            progreso_funcionalidad = (0.5 * manejo_contenidos + 0.1 * nivel_programacion + 0.4 * horas_tarea) * 0.9
            self.progreso_total = 0.4 * progreso_funcionalidad + 0.4 * progreso_contenidos + 0.2 * progreso_pep8




class Control(Evaluacion):
    def __init__(self, numero, contenido, dificultad, fecha, exigencia):
        super().__init__(numero, contenido, dificultad, fecha, exigencia)
        self.tipo = 'control'
        self.categoria = 'controles'

    def progreso(self, manejo_contenidos, nivel_programacion, confianza):
        progreso_contenido = 0.7 * manejo_contenidos + 0.05 * nivel_programacion + 0.25 * confianza
        progreso_funcionalidad = 0.3 * manejo_contenidos + 0.2 * nivel_programacion + 0.5 * confianza
        self.progreso_total = 0.3 * progreso_funcionalidad + 0.7 * progreso_contenido


# todo
class Examen(Evaluacion):
    def __init__(self, numero, contenido, dificultad, fecha, exigencia):
        super().__init__(numero, contenido, dificultad, fecha, exigencia)
        self.tipo = 'examen'
        # en este caso el contenido es una lista de contenidos en funcion de lo pedido [('3'), ('6')]
