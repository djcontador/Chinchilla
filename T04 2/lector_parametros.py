class Variables:
    """
    Esta clase almacena las constantes del enunciado que pueden
    ser modificadas a traves de parametros.csv
    las variables a modificar son:
    - Intervalos de la tabla "Nota esperada por el alumno, para cada contenido, segun las horas dedicadas"
        (Cuadro 4 del enunciado)
    - Dificultad de cada contenido del curso (Cuadro 3 del enunciado)
    """
    matriz1 = None
    diccionario1 = None

    def __init__(self):
        import csv
        with open('parametros_nota_esperada.csv') as csvfile:  # abre la matriz de notas esperadas
            reader = csv.DictReader(csvfile)
            diccionario = next(reader)
            for key in diccionario:
                horas = diccionario[key].replace("(", "").replace(")", "").split(", ")
                lista = []
                for intervalo in horas:
                    lista.append(intervalo.split("-"))
                diccionario[key] = lista
                if key != 'header':
                    rangos = []
                    for elemento in lista:
                        rangos.append(range(int(elemento[0]), int(elemento[1])))
                    diccionario[key] = rangos
            Variables.matriz1 = diccionario
        self.matriz_nota_esperada = Variables.matriz1

        with open('parametros_dificultad.csv') as csvfile:  # abre el diccionario de dificultad
            reader = csv.DictReader(csvfile)
            diccionario1 = next(reader)
            for key in diccionario1:
                valor = int(diccionario1[key])
                diccionario1[key] = valor
            Variables.diccionario1 = diccionario1
        self.diccionario_dificultad = Variables.diccionario1
