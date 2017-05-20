import random
from clases import Seccion, Profesor,  Alumno, AyudanteDocente, AyudanteTareas, Coordinador
from evaluaciones import Actividad, Control, Tarea, Examen
from generador_eventos import generador_eventos_controles, generador_eventos_actividades
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
        self.contenidos = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
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

        # lista de eventos
        self.calendario = [i + 1 for i in range(100)]

        self.eventos = (generador_eventos_controles(self.dificultad) +
                              generador_eventos_actividades(self.dificultad))
        # recuerda sumar los otros eventos

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
                    alumno = Alumno(linea['Nombre:string'], linea['Sección:string'], self.creditaje, self.dificultad,
                                    self.nivel_inicial_confianza_superior, self.nivel_inicial_confianza_inferior)
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
        contenido = 0

        for dia in self.calendario:
            # actualizacion del nivel de programacion cada lunes
            if (dia - 1)//7 == (dia - 1)/7 and dia <= 78:  # si el dia es un lunes
                for seccion in self.secciones:
                    for alumno in self.secciones[seccion].alumnos:
                        alumno.nivel_programacion(self.contenidos[contenido])
                contenido += 1

            for evento in self.eventos:
                # evento Control Sorpresa
                if dia == evento[0] and evento[1]['evento'] == 'Control':
                    for seccion in self.secciones:
                        for alumno in self.secciones[seccion].alumnos:
                            alumno.rendir_evaluacion(Control(evento[1]['numero'],
                                                             evento[1]['contenido'],
                                                             evento[1]['dificultad'],

                                                             evento[1]['fecha']), self.matriz_nota_esperada)

                # evento Catedra y Actividad Evaluada
                if dia == evento[0] and evento[1]['evento'] == 'Actividad':
                    for seccion in self.secciones:
                        for alumno in self.secciones[seccion].alumnos:
                            x = random.random()
                            if x <= 0.5:  # esucho el tip del profesor
                                alumno.manejo_contenidos[evento[1]['contenido']] *= 1.1  # incrementa en un 10%
                            alumno.rendir_evaluacion(Actividad(evento[1]['numero'],
                                                               evento[1]['contenido'],
                                                               evento[1]['dificultad'],
                                                               evento[1]['fecha']), self.matriz_nota_esperada)



###########################################################################################################
# ############################   tester de simulacion   ###################################################
###########################################################################################################
print("inicia Simulacion.py")
simulacion = Semestre()
print("eventos: ", simulacion.eventos)
print("atributo escenario: ", simulacion.atributo_escenario)

print("\nPARAMETROS de escenarios.csv")
print("creditaje: ", simulacion.creditaje)
print("prob_visitar_profesor: ", simulacion.prob_visitar_profesor)
print("prob_atraso_notas_mavrakis: ", simulacion.prob_atraso_notas_mavrakis)
print("porcentaje_progreso_tarea_mail: ", simulacion.porcentaje_progreso_tarea_mail)
print("fiesta_mes: ", simulacion.fiesta_mes)
print("partido_futbol_mes: ", simulacion.partido_futbol_mes)
print("nivel_inicial_confianza_inferior: ", simulacion.nivel_inicial_confianza_inferior)
print("nivel_inicial_confianza_superior: ", simulacion.nivel_inicial_confianza_superior)

print("\n parametros.csv")
print("dificultad: ", simulacion.dificultad)
print("matriz notas esperadas: ")
print('h:', simulacion.matriz_nota_esperada['header'])
print('1:', simulacion.matriz_nota_esperada['1'])
print('2:', simulacion.matriz_nota_esperada['2'])
print('3:', simulacion.matriz_nota_esperada['3'])
print('4:', simulacion.matriz_nota_esperada['4'])
print('5:', simulacion.matriz_nota_esperada['5'])
print('6:', simulacion.matriz_nota_esperada['6'])
print('7:', simulacion.matriz_nota_esperada['7'])
print('8:', simulacion.matriz_nota_esperada['8'])
print('9:', simulacion.matriz_nota_esperada['9'])
print('10:', simulacion.matriz_nota_esperada['10'])
print('11:', simulacion.matriz_nota_esperada['11'])
print('12:', simulacion.matriz_nota_esperada['12'])


simulacion.run()

for seccion in simulacion.secciones:
    print("\n", simulacion.secciones[seccion].profesor.nombre, isinstance(simulacion.secciones[seccion].profesor,
                                                                          Profesor))
    for alumnos in simulacion.secciones[seccion].alumnos:
        if alumnos.nombre == "Daniela Contador" or alumnos.nombre == "Alfredo De Goyeneche":
            print("\n", alumnos.nombre)
            print("personalidad: ", alumnos.personalidad)
            print("creditos tomados: ", alumnos.creditos)
            print("## \nACTIVIDADES ", alumnos.nombre)
            for evaluacion in alumnos.portafolio['actividades']:

                print("\nActividad {0} - contenido: {1} - dificultad: {2}".format(evaluacion.numero,
                                                                                  evaluacion.contenido,
                                                                                  evaluacion.dificultad))
                #print("horas disponibles esa semana", alumnos.horas_disponibles[int(evaluacion.contenido) - 1])
                print("horas estudiadas: ", alumnos.historial_hs[evaluacion.contenido])

                print("manejo de contenidos: ", alumnos.manejo_contenidos[evaluacion.contenido])
                print("confianza: ", alumnos.confianza)
                print("nota esperada: {}".format(evaluacion.nota_esperada))
                print("progreso total: {}".format(evaluacion.progreso_total))

            print("horas disponibles: ", alumnos.horas_disponibles)
            print("historial Hs: ", alumnos.historial_hs)
            #print("confianza: ", alumnos.confianza)

            print("## \nCONTROLES ", alumnos.nombre)
            for evaluacion in alumnos.portafolio['controles']:
                print("\nControl {0} - contenido: {1} - dificultad: {2}".format(evaluacion.numero,
                                                                                evaluacion.contenido,
                                                                                evaluacion.dificultad))
                #print("horas disponibles esa semana", alumnos.horas_disponibles[int(evaluacion.contenido) - 1])
                print("horas estudiadas: ", alumnos.historial_hs[evaluacion.contenido])

                print("manejo de contenidos: ", alumnos.manejo_contenidos[evaluacion.contenido])
                print("confianza: ", alumnos.confianza)
                print("nota esperada: {}".format(evaluacion.nota_esperada))
                print("progreso total: {}".format(evaluacion.progreso_total))



#print("\nTareos")
#for ayudante in simulacion.ayudantes["Tareas"]:
#    print(ayudante.nombre, isinstance(ayudante, AyudanteTareas))

#print("\nDocencios")
#for ayudante in simulacion.ayudantes["Docencia"]:
#    print(ayudante.nombre, isinstance(ayudante, AyudanteDocente))

#print("\nCoordinador")
#print(simulacion.coordinador.nombre, isinstance(simulacion.coordinador, Coordinador))
