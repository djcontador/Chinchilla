import random
from clases import Seccion, Profesor,  Alumno, AyudanteDocente, AyudanteTareas, Coordinador
from evaluaciones import Actividad, Control, Tarea, Examen
from generador_eventos import generador_visitas_profesor, generador_eventos_controles, \
                              generador_eventos_actividades, ordenador_eventos, generador_eventos_tareas, \
                              generador_eventos_fiesta
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

        self.promedio_semanal_semestre = {'tareas': [], 'actividades': [], 'examen': []}

        self.posibilidad_extender_plazo_tareas = True

        # lista de eventos
        self.lista_fiestas = generador_eventos_fiesta(self.fiesta_mes)

        self.eventos = ordenador_eventos(generador_visitas_profesor() +
                                         generador_eventos_controles(self.dificultad) +
                                         generador_eventos_actividades(self.dificultad) +
                                         generador_eventos_tareas(self.dificultad) +
                                         self.lista_fiestas)

        # recuerda sumar los otros eventos, como publicacion tareas (correccion + plazo), publicacion mavrakis,
        # eventos no programados

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
        """
        se encarga de recorrer el atributo eventos de la clase semestre, y va ejecutando cada evento
        para realizar la simulacion DES.
        :return:
        :rtype: None
        """
        self.importar_integrantes()

        # modificar por eventos no programados
        # fiesta

        for fiesta in self.lista_fiestas:
            semana = fiesta[1]['semana']  # string de semana, que calza con el contenido
            total_alumnos = []
            for seccion in self.secciones:
                for alumno in self.secciones[seccion].alumnos:
                    total_alumnos.append(alumno)
            alumnos_carreteros = random.sample(total_alumnos, 50)
            for fiestero in alumnos_carreteros:
                fiestero.asistencias_fiesta.append(semana)
                print("fiestero: {0} asistira a la fiesta de la semana {1}".format(fiestero.nombre, semana))

        # actualizacion de sus horas disponibles de estudio funcion de su asistencia a fiestas
        for seccion in self.secciones:
            for alumno in self.secciones[seccion].alumnos:
                alumno.calculador_horas_disponibles()

        # partido futbol todo


        contenido = 0
        # recorrido de la lista de eventos
        for evento in self.eventos:
            # evento publicacion de notas por el coordinador Mavrakis
            #if evento[1]['evento'] == ''
            # luego agregar promedio a self.promedio_semanal

            # evento Reunion con el Profesor
            if evento[1]['evento'] == 'Visitar Profesor':
                for seccion in self.secciones:
                    for alumno in self.secciones[seccion].alumnos:
                        alumno.nivel_programacion(self.contenidos[contenido])  # actualiza el nivel de programacion
                contenido += 1  # numero de la semana, que calza con el contenido correspondiente

                # hacer la visita con el profesor
                for seccion in self.secciones:
                    profesor = self.secciones[seccion].profesor
                    alumnos = self.secciones[seccion].alumnos
                    # seleccionar cant_alumnos del evento (si hay o no hay corte de agua)

            # evento Ayudantia
            # if evento[1]['evento] == 'Ayudantia':

            # evento Control Sorpresa
            elif evento[1]['evento'] == 'Control':
                n = 0
                # Reunion de los ayudantes de docencia para definir la exigencia del control
                exigencia = 7 + ((random.uniform(1, 5)) / evento[1]['dificultad'])
                print("Reunion de ayudantes docentes para definir exigencia de {0} para el control {1} en la "
                      "semana {2}".format(exigencia, evento[1]['numero'], int(evento[1]['contenido']) + 1))
                # rendicion del control
                for seccion in self.secciones:
                    for alumno in self.secciones[seccion].alumnos:
                        n += 1
                        alumno.rendir_evaluacion(Control(evento[1]['numero'],
                                                         evento[1]['contenido'],
                                                         evento[1]['dificultad'],
                                                         evento[1]['fecha'],
                                                         exigencia), self.matriz_nota_esperada)
                print("{0} alumnos realizaron el control {1} la semana {2}.".format(n, evento[1]['numero'],
                                                                                    int(evento[1]['contenido']) + 1))

            # evento Catedra y Actividad Evaluada
            elif evento[1]['evento'] == 'Actividad':
                n = 0
                # Reunion de los ayudantes de docencia para definir la exigencia de la actividad
                exigencia = 7 + ((random.uniform(1, 5)) / evento[1]['dificultad'])
                print("Reunion de ayudantes docentes para definir exigencia de {0} para la actividad de la "
                      "semana {1}".format(exigencia, evento[1]['contenido']))
                for seccion in self.secciones:
                    for alumno in self.secciones[seccion].alumnos:
                        n += 1
                        x = random.random()
                        if x <= 0.5:  # esucho el tip del profesor
                            alumno.manejo_contenidos[evento[1]['contenido']] *= 1.1  # incrementa en un 10%
                        alumno.rendir_evaluacion(Actividad(evento[1]['numero'],
                                                           evento[1]['contenido'],
                                                           evento[1]['dificultad'],
                                                           evento[1]['fecha'], exigencia), self.matriz_nota_esperada)
                print("{0} alumnos asistieron a la catedra la semana {1}.".format(n, evento[1]['contenido']))

                # hacer las preguntas a los ayudantes para aumentar el manejo de contenidos en preguntas
                # antes de que termine la actividad evaluada
                print("{0} alumnos realizaron la actividad {1} la semana {2}.".format(n, evento[1]['numero'],
                                                                                      evento[1]['contenido']))

            elif evento[1]['evento'] == 'Correccion Control':
                for seccion in self.secciones:
                    for alumno in self.secciones[seccion].alumnos:
                        for control in alumno.portafolio['controles']:
                            if control.numero == evento[1]['numero']:
                                ayudante_con_mala_suerte = random.sample(self.ayudantes['Docencia'], 1)[0]
                                ayudante_con_mala_suerte.corregir(alumno, control)
                print("Se corrigio el control {0} y se le entrego a el coordinador Dr. Mavrakis en la semana "
                      "{1}.".format(evento[1]['numero'], int(evento[1]['contenido']) + 3))

            elif evento[1]['evento'] == 'Correccion Actividad':
                for seccion in self.secciones:
                    for alumno in self.secciones[seccion].alumnos:

                        for actividad in alumno.portafolio['actividades']:
                            if actividad.numero == evento[1]['numero']:
                                # se elegira el ayudante que lamentablemente debe corregir
                                # la actividad para todos los alumnos
                                ayudante_con_mala_suerte = random.sample(self.ayudantes['Docencia'], 1)[0]
                                ayudante_con_mala_suerte.corregir(alumno, actividad)
                print("Se corrigio la actividad {0} y se le entrego a el coordinador Dr. Mavrakis en la semana "
                      "{1}.".format(evento[1]['numero'], int(evento[1]['contenido']) + 2))

            elif evento[1]['evento'] == 'Tarea':
                n = 0
                # Reunion de los ayudantes de tareas para definir la exigencia de la tarea
                exigencia = 7 + ((random.uniform(1, 5)) / evento[1]['dificultad'])
                print("cacahuate, " , evento[1]['contenidos'])
                print("Reunion de ayudantes de tarea para definir exigencia de {0} para la tarea {1} en la "
                      "semana {2}".format(exigencia, evento[1]['numero'], evento[1]['contenidos'][0]))
                # rendicion de la tarea
                for seccion in self.secciones:
                    for alumno in self.secciones[seccion].alumnos:
                        n += 1
                        alumno.rendir_evaluacion(Tarea(evento[1]['numero'],
                                                       evento[1]['contenidos'],
                                                       evento[1]['dificultad'],
                                                       evento[1]['fecha_inicio'],
                                                       exigencia,
                                                       evento[1]['fecha_termino']),
                                                 self.matriz_nota_esperada)
                print("{0} alumnos comenzaron con la Tarea {1} la "
                      "semana {2}.".format(n, evento[1]['numero'], evento[1]['contenidos'][0]))

            elif evento[1]['evento'] == 'Entrega Tarea':
                print("queremos entregar la tareaaaaaaaaaaaaaaaaaaaaaa {}".format(evento[1]['numero']))

                alumnos_atrasados = 0
                cantidad_alumnos = 0
                for seccion in self.secciones:
                    for alumno in self.secciones[seccion].alumnos:
                        if not alumno.entregar_tarea(evento[1]['numero'], self.porcentaje_progreso_tarea_mail):
                            # si esque retorna False
                            alumnos_atrasados += 1
                        cantidad_alumnos += 1

                if self.posibilidad_extender_plazo_tareas:
                    # si esque no se a extendido el plazo de ninguna tarea anterior
                    print("{0} alumnos enviaron mail pidiendo mas tiempo para la tarea {1} en la semana "
                          "{2}".format(alumnos_atrasados, evento[1]['numero'], int(evento[1]['contenidos'][1]) + 1))
                    if alumnos_atrasados >= 0.8 * cantidad_alumnos:
                        # el 80% mando mail
                        x = random.random()
                        if x <= 0.2:
                            print("se ha extendido el plazo de entrega de la tarea {0} para el "
                                  "{1}".format(evento[1]['numero'], evento[1]['fecha_termino'] + 2))
                            # hacer que los alumnos puedan poner el avance de horas correspondiente a esos dias extras
                            # hacer ue si hay un partido, sacar esas horas disponibles
                            # una vez hecho eso, copiar el mismo print del else para que se entrege
                            self.posibilidad_extender_plazo_tareas = False
                else:
                    # la tarea se entregara...

                    print("Se ha entregalo la tarea {} el dia {}".format(evento[1]['numero'],
                                                                         evento[1]['fecha_termino']))
                    for seccion in self.secciones:
                        for alumno in self.secciones[seccion].alumnos:
                            for tarea in alumno.portafolio['tareas']:
                                if tarea.numero == evento[1]['numero']:
                                    print("progreso del alumno {}: ".format(alumno.nombre), tarea.progreso_total)
                                    print("progreso esperado (exigencia): ", tarea.exigencia)

            elif evento[1]['evento'] == 'Fiesta':
                print("50 alumnos asistieron a la fiesta de la semana {}".format(evento[1]['semana']))







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
print('12:', simulacion.matriz_nota_esperada['12'], "\n")


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
                # print("horas disponibles esa semana", alumnos.horas_disponibles[int(evaluacion.contenido) - 1])
                print("horas estudiadas: ", alumnos.historial_hs[evaluacion.contenido])

                print("manejo de contenidos: ", alumnos.manejo_contenidos[evaluacion.contenido])
                print("confianza: ", alumnos.confianza)
                print("nota esperada: {}".format(evaluacion.nota_esperada))
                print("nota obtenida: {}".format(evaluacion.nota_real))
                print("exigencia: {}".format(evaluacion.exigencia))
                print("progreso total: {}".format(evaluacion.progreso_total))
                print("promedio actual: ", alumnos.promedio)

            print("horas disponibles: ", alumnos.horas_disponibles)
            print("historial Hs: ", alumnos.historial_hs)
            # print("confianza: ", alumnos.confianza)

            print("## \nCONTROLES ", alumnos.nombre)
            for evaluacion in alumnos.portafolio['controles']:
                print("\nControl {0} - contenido: {1} - dificultad: {2}".format(evaluacion.numero,
                                                                                evaluacion.contenido,
                                                                                evaluacion.dificultad))
                # print("horas disponibles esa semana", alumnos.horas_disponibles[int(evaluacion.contenido) - 1])
                print("horas estudiadas: ", alumnos.historial_hs[evaluacion.contenido])

                print("manejo de contenidos: ", alumnos.manejo_contenidos[evaluacion.contenido])
                print("confianza: ", alumnos.confianza)
                print("nota esperada: {}".format(evaluacion.nota_esperada))
                print("nota obtenida: {}".format(evaluacion.nota_real))
                print("exigencia: {}".format(evaluacion.exigencia))
                print("progreso total: {}".format(evaluacion.progreso_total))
                print("promedio actual: ", alumnos.promedio)

            #
            print("## \nTAREAS ", alumnos.nombre)
            for evaluacion in alumnos.portafolio['tareas']:
                print("\nTarea {0} - contenido: {1} - dificultad: {2}".format(evaluacion.numero,
                                                                              evaluacion.contenido,
                                                                              evaluacion.dificultad))
                # print("horas disponibles esa semana", alumnos.horas_disponibles[int(evaluacion.contenido) - 1])
                print("horas estudiadas: ", alumnos.historial_ht[evaluacion.contenido[0]] +
                      alumnos.historial_ht[evaluacion.contenido[1]])

                print("manejo de contenidos: ", (alumnos.manejo_contenidos[evaluacion.contenido[0]] +
                                                 alumnos.manejo_contenidos[evaluacion.contenido[1]])/2)
                print("confianza: ", alumnos.confianza)
                print("nota esperada: {}".format(evaluacion.nota_esperada))
                print("nota obtenida: {}".format(evaluacion.nota_real))
                print("exigencia: {}".format(evaluacion.exigencia))
                print("progreso total: {}".format(evaluacion.progreso_total))
                print("promedio actual: ", alumnos.promedio)





#print("\nTareos")
#for ayudante in simulacion.ayudantes["Tareas"]:
#    print(ayudante.nombre, isinstance(ayudante, AyudanteTareas))

#print("\nDocencios")
#for ayudante in simulacion.ayudantes["Docencia"]:
#    print(ayudante.nombre, isinstance(ayudante, AyudanteDocente))

#print("\nCoordinador")
#print(simulacion.coordinador.nombre, isinstance(simulacion.coordinador, Coordinador))
