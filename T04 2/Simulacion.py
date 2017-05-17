from clases import Seccion, Profesor,  Alumno, AyudanteDocente, AyudanteTareas, Coordinador
from evaluaciones import Actividad
from lector_parametros import Variables
from lector_escenarios import Escenarios
variable = Variables()
escenario = Escenarios()


class Semestre:
    """
    Esta clase corresponde a la simulacion de el tanscurso de un semestre
    permite que en cada instancia se simule un semestre distinto
    """

    def __init__(self, atributo_escenario=None):
        """
        :param atributo_escenario: key de la base de datos escenarios.csv que indica el escenario con que
        se quiere realizar la simulacion del semestre ('escenario_1, escenario_27, etc)
        :type atributo_escenario: str
        """
        self.ayudantes = {'Docencia': [], 'Tareas': []}
        self.secciones = {}
        self.coordinador = None
        self.contenidos = []
        self.atributo_escenario = atributo_escenario  # si hay un escenario se cambiaran

        # parametros de base de datos
        self.matriz_nota_esperada = variable.matriz_nota_esperada
        self.dificultad = variable.diccionario_dificultad

        # estadisticas
        self.botar_ramo = 0
        self.confianza_i = None
        self.confianza_f = None
        self.dicc_aprobacion = {}
        self.rendimiento = {'tareas': [], 'actividades': [], 'examen': []}

    # parametros en escenarios.csv
    @property
    def creditaje(self):
        if not self.atributo_escenario:
            retorno = [(Escenarios.parametros_default['prob_40_creditos'], '40_creditos'),
                       (Escenarios.parametros_default['prob_50_creditos'], '50_creditos'),
                       (Escenarios.parametros_default['prob_55_creditos'], '55_creditos'),
                       (Escenarios.parametros_default['prob_60_creditos'], '60_creditos')]
            return retorno
        else:
            retorno = [(escenario.escenarios[self.atributo_escenario]['prob_40_creditos'], '40_creditos'),
                       (escenario.escenarios[self.atributo_escenario]['prob_50_creditos'], '50_creditos'),
                       (escenario.escenarios[self.atributo_escenario]['prob_55_creditos'], '55_creditos'),
                       (escenario.escenarios[self.atributo_escenario]['prob_60_creditos'], '60_creditos')]
            return retorno

    @property
    def prob_visitar_profesor(self):
        if not self.atributo_escenario:
            return Escenarios.parametros_default['prob_visitar_profesor']
        else:
            return escenario.escenarios[self.atributo_escenario]['prob_visitar_profesor']

    @property
    def prob_atraso_notas_mavrakis(self):
        if not self.atributo_escenario:
            return Escenarios.parametros_default['prob_atraso_notas_Mavrakis']
        else:
            return escenario.escenarios[self.atributo_escenario]['prob_atraso_notas_Mavrakis']

    @property
    def porcentaje_progreso_tarea_mail(self):
        if not self.atributo_escenario:
            return Escenarios.parametros_default['porcentaje_progreso_tarea_mail']
        else:
            return escenario.escenarios[self.atributo_escenario]['porcentaje_progreso_tarea_mail']

    @property
    def fiesta_mes(self):
        if not self.atributo_escenario:
            return Escenarios.parametros_default['fiesta_mes']
        else:
            return escenario.escenarios[self.atributo_escenario]['fiesta_mes']

    @property
    def partido_futbol_mes(self):
        if not self.atributo_escenario:
            return Escenarios.parametros_default['partido_futbol_mes']
        else:
            return escenario.escenarios[self.atributo_escenario]['partido_futbol_mes']

    @property
    def nivel_inicial_confianza_inferior(self):
        if not self.atributo_escenario:
            return Escenarios.parametros_default['nivel_inicial_confianza_inferior']
        else:
            return escenario.escenarios[self.atributo_escenario]['nivel_inicial_confianza_inferior']

    @property
    def nivel_inicial_confianza_superior(self):
        if not self.atributo_escenario:
            return Escenarios.parametros_default['nivel_inicial_confianza_superior']
        else:
            return escenario.escenarios[self.atributo_escenario]['nivel_inicial_confianza_superior']

    def importar_integrantes(self):
        """
        obtiene los datos necesarios del archivo integrantes.csv para crear las instancias de
        todos los integrantes de avanzacion programada y los guarda en los atributos de Semestre
        :return:
        :rtype: None
        """
        import csv
        with open('integrantes.csv', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for linea in reader:
                # crea profesores y las secciones
                if linea["Rol:string"] == "Profesor":
                    profesor = Profesor(linea['Nombre:string'], linea['Sección:string'])
                    self.secciones[linea['Sección:string']] = Seccion(profesor)

                # crea los alumnos
                elif linea["Rol:string"] == "Alumno":
                    alumno = Alumno(linea['Nombre:string'], linea['Sección:string'], self.creditaje, self.dificultad)
                    self.secciones[linea['Sección:string']].agregar_alumno(alumno)

                # crea los ayudantes
                elif linea["Rol:string"] == "Docencia":
                    ayudante = AyudanteDocente(linea['Nombre:string'])
                    self.ayudantes['Docencia'].append(ayudante)

                elif linea["Rol:string"] == "Tareas":
                    ayudante = AyudanteTareas(linea['Nombre:string'])
                    self.ayudantes['Tareas'].append(ayudante)

                # crea el coordinador
                elif linea["Rol:string"] == 'Coordinación':
                    self.coordinador = Coordinador(linea['Nombre:string'])

    def run(self):
        self.importar_integrantes()


###########################################################################################################
# ############################   tester de simulacion   ###################################################
###########################################################################################################
print("inicia Simulacion.py")
simulacion = Semestre()
simulacion.run()
matriz_nota_esperada = simulacion.matriz_nota_esperada
print(matriz_nota_esperada)
print(simulacion.secciones)
evaluacion = Actividad('01', '1', simulacion.dificultad['1'], 4)


for seccion in simulacion.secciones:
    print("\n", simulacion.secciones[seccion].profesor.nombre, isinstance(simulacion.secciones[seccion].profesor, Profesor))
    for alumnos in simulacion.secciones[seccion].alumnos:
        print(alumnos.seccion, alumnos.nombre, alumnos.creditos, alumnos.personalidad)

        print(alumnos.historial_hs)
        alumnos.rendir_evaluacion(evaluacion, matriz_nota_esperada)


#print("\nTareos")
#for ayudante in simulacion.ayudantes["Tareas"]:
#    print(ayudante.nombre, isinstance(ayudante, AyudanteTareas))

#print("\nDocencios")
#for ayudante in simulacion.ayudantes["Docencia"]:
#    print(ayudante.nombre, isinstance(ayudante, AyudanteDocente))

#print("\nCoordinador")
#print(simulacion.coordinador.nombre, isinstance(simulacion.coordinador, Coordinador))
