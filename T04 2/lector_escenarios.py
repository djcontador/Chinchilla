class Escenarios:
    """
    Esta clase contiene los datos de escenarios.csv guardados en su
    atributo escenarios.
    """
    # valores default de parametros
    parametros_default = {'prob_40_creditos': 0.1,
                          'prob_50_creditos': 0.7,
                          'prob_55_creditos': 0.15,
                          'prob_60_creditos': 0.05,
                          'prob_visitar_profesor': 0.2,
                          'prob_atraso_notas_Mavrakis': 0.1,
                          'porcentaje_progreso_tarea_mail': 0.5,
                          'fiesta_mes': 1/30,
                          'partido_futbol_mes': 1/70,
                          'nivel_inicial_confianza_inferior': 2,
                          'nivel_inicial_confianza_superior': 12}

    # que siga el mismo formato, pero para cada escenario
    matriz_escenarios = None

    def __init__(self):
        import csv
        with open('escenarios.csv') as csvfile:  # abre la matriz de notas esperadas
            reader = csv.DictReader(csvfile)
            matriz = {}
            for fila in reader:
                parametro = fila['Parametro:string']
                del fila['Parametro:string']
                for escenario in fila:
                    key_escenario = escenario.split(":")
                    if not key_escenario[0] in matriz:  # si no existe, crea ese elemento
                        matriz[key_escenario[0]] = {}
                        matriz[key_escenario[0]][parametro] = fila[escenario]
                    else:
                        matriz[key_escenario[0]][parametro] = fila[escenario]

            for escenario in matriz:
                for parametro in matriz[escenario]:
                    if matriz[escenario][parametro] == '-':
                        valor = Escenarios.parametros_default[parametro]
                        matriz[escenario][parametro] = valor
                    else:
                        valor = float(matriz[escenario][parametro])
                        matriz[escenario][parametro] = valor

            Escenarios.matriz_escenarios = matriz
        self.escenarios = Escenarios.matriz_escenarios
