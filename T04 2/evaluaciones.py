import random


portafolio = {'tareas': [], 'actividades': [], 'controles': [], 'examen': []}


class Evaluacion:
    def __init__(self, numero, contenido, dificultad):
        self.numero = numero
        self.contenido = contenido
        self.dificultad = dificultad

        self.nota_esperada = None
        self.nota_real = None
        self.progreso_total = None


class Actividad(Evaluacion):
    def __init__(self, numero, contenido, dificultad):
        super().__init__(numero, contenido, dificultad)
        self.tipo = 'actividad'

    def progreso(self, manejo_contenidos, nivel_programacion, confianza):
        progreso_pep8 = 0.7 * manejo_contenidos + 0.2 * nivel_programacion + 0.1 * confianza
        progreso_funcionalidad = 0.3 * manejo_contenidos + 0.6 * nivel_programacion + 0.1 * confianza
        progreso_contenidos = 0.7 * manejo_contenidos + 0.2 * nivel_programacion + 0.1 * confianza
        self.progreso_total = 0.4 * progreso_funcionalidad + 0.4 * progreso_contenidos + 0.2 * progreso_pep8


class Tarea(Evaluacion):
    def __init__(self, numero, contenido, dificultad):
        super().__init__(numero, contenido, dificultad)
        self.tipo = 'tarea'

    def progreso(self, manejo_contenidos, nivel_programacion, horas_tarea):
        progreso_pep8 = 0.5 * horas_tarea + 0.5 * nivel_programacion
        progreso_contenidos = 0.7 * manejo_contenidos + 0.1 * nivel_programacion + 0.2 * horas_tarea
        progreso_funcionalidad = 0.5 * manejo_contenidos + 0.1 * nivel_programacion + 0.4 * horas_tarea
        self.progreso_total = 0.4 * progreso_funcionalidad + 0.4 * progreso_contenidos + 0.2 * progreso_pep8


class Control(Evaluacion):
    def __init__(self, numero, contenido, dificultad):
        super().__init__(numero, contenido, dificultad)
        self.tipo = 'control'

    def progreso(self, manejo_contenidos, nivel_programacion, confianza):
        progreso_contenido = 0.7 * manejo_contenidos + 0.05 * nivel_programacion + 0.25 * confianza
        progreso_funcionalidad = 0.3 * manejo_contenidos + 0.2 * nivel_programacion + 0.5 * confianza
        self.progreso_total = 0.3 * progreso_funcionalidad + 0.7 * progreso_contenido


# todo
class Examen(Evaluacion):
    def __init__(self, numero, contenido, dificultad):
        super().__init__(numero, contenido, dificultad)
        self.tipo = 'examen'
        # en este caso el contenido es una lista de contenidos en funcion de lo pedido [('3'), ('6')]

# recordar setear la dificultad por 'parametros_dificultad.csv'
actividades = [(4, Actividad('01', '1', 2)), (11, Actividad('02', '2', 2)), (18, Actividad('03', '3', 3)),
               (25, Actividad('04', '4', 5)), (32, Actividad('05', '5', 7)), (39, Actividad('06', '6', 10))]
