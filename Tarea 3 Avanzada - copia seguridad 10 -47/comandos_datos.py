from errores import ErrorDeTipo, ImposibleProcesar
from itertools import tee
from functools import reduce
from comandos_numericos import LEN
from comandos_basicos import crear_funcion


def extraer_columna(nombre_archivo, columna):
    # verifica que los argumentos sean strings
    if not isinstance(nombre_archivo, str) or not isinstance(columna, str):  # alguno de los argumentos no es str
        print("alguno de los argumentos no es un string")
        raise ErrorDeTipo

    # verifica que el archivo exista
    try:
        archivo = open(nombre_archivo + '.csv', "r")
        gen_listas = (linea.strip().split(";") for linea in archivo)  # cambiar a ;
        header = list(enumerate(next(gen_listas)))
        match = list(filter(lambda x: columna in x[1], header))

        # verifica si la columna esta en el archivo
        if len(match) == 0:  # la columna no esta en el archivo
            print("la columna no esta en el archivo")
            raise ImposibleProcesar
        else:  # la columna esta en el archivo
            head = match[0][1].split(":")
            tipo = head[1].replace(" ", "")

            # verifica que la columna sea de datos numericos
            if tipo != "int" and tipo != "float":  # No se puede retornar una columna no numerica
                print("No se puede retornar una columna no numerica")
                raise ErrorDeTipo  # asumo que aqui es error de tipo porque int(string) es ValueError, en que int espera un digito, no un string READMEEEEE
            else:  # la columna es numerica
                posicion = match[0][0]
                if tipo == "int":
                    gen_columna = map(lambda x: int(x[posicion]), gen_listas)
                elif tipo == "float":
                    gen_columna = map(lambda x: float(x[posicion]), gen_listas)
                return gen_columna

    except FileNotFoundError as err:
        print("El archivo no existe")
        raise ImposibleProcesar


def filtrar(columna_i, simbolo, valor):
    # verifica que la columna sea iterable
    try:
        columna, columna2 = tee(columna_i)
    except TypeError as err:
        print("la columna no es iterable")
        raise ErrorDeTipo             # por que se levantan 2 excepciones filtar(3, '>=', 1) ???????????????
    # verifica argumentos validos
    if not isinstance(valor, float) and not isinstance(valor, int):  # args invalidos
        print("alguno de los argumentos es invalido")
        raise ErrorDeTipo
    if not isinstance(simbolo, str):
        print("simbolo no es un string")
        raise ErrorDeTipo
    comparaciones = ['==', '>', '<', '>=', '<=', '!=']
    if simbolo not in comparaciones:
        print("Simbolo no valido")
        raise ErrorDeTipo

    # verifica que la columna sea un conjunto numerico
    gen = filter(lambda x: not isinstance(x, int) and not isinstance(x, float), columna2)
    if LEN(gen) > 0:
        print("la columna no es un conjunto numerico")
        raise ErrorDeTipo

    # verifica que columna sea un set de datos iterable (secuencia, lista, generador, etc) y numerica
    if simbolo == '==':
        filtrado = filter(lambda x: x == valor, columna)
        return filtrado
    elif simbolo == '>':
        filtrado = filter(lambda x: x > valor, columna)
        return filtrado
    elif simbolo == '<':
        filtrado = filter(lambda x: x < valor, columna)
        return filtrado
    elif simbolo == '>=':
        filtrado = filter(lambda x: x >= valor, columna)
        return filtrado
    elif simbolo == '<=':
        filtrado = filter(lambda x: x <= valor, columna)
        return filtrado
    elif simbolo == '!=':
        filtrado = filter(lambda x: x != valor, columna)
        return filtrado


def operar(columna_i, simbolo, valor):
    # verifica que la columna sea un iterable
    try:
        columna, columna2 = tee(columna_i)
    except TypeError as err:
        print("la columna no es iterable")
        raise ErrorDeTipo

    # verifica argumentos validos
    if not isinstance(valor, float) and not isinstance(valor, int):  # args invalidos
        print("alguno de los argumentos es invalido")
        raise ErrorDeTipo
    if not isinstance(simbolo, str):
        print("simbolo no es un string")
        raise ErrorDeTipo
    operaciones = ['+', '-', '*', '/', '>=<']
    if simbolo not in operaciones:
        print("Simbolo no valido")
        raise ErrorDeTipo

    # realizar operaciones
    if simbolo == 'x':
        operado = map(lambda x: x + valor, columna)
        return operado
    elif simbolo == '-':
        operado = map(lambda x: x - valor, columna)
        return operado
    elif simbolo == '*':
        operado = map(lambda x: x * valor, columna)
        return operado
    elif simbolo == '/':
        operado = map(lambda x: x / valor, columna)
        return operado
    elif simbolo == '>=<':
        if valor < 0:
            print("para hacer una aproximacion, el numero de decimales debe ser mayor o igual a cero")
            raise ErrorDeTipo
        operado = map(lambda x: round(x, valor), columna)
        return operado


def evaluar(funcion, inicio, final, intervalo):
    if not isinstance(inicio, int) and not isinstance(inicio, float):
        raise ErrorDeTipo
    if not isinstance(final, int) and not isinstance(final, float):
        raise ErrorDeTipo
    if not isinstance(intervalo, int) and not isinstance(intervalo, float):
        raise ErrorDeTipo
    if inicio < final and intervalo < 0:
        raise ErrorDeTipo
    if inicio > final and intervalo > 0:
        raise ErrorDeTipo

    if inicio <= final:
        multiplicador = int((final - inicio) / intervalo) + 1
        secuencia = enumerate(intervalo for i in range(multiplicador))
        gen_x = map(lambda x: round(inicio + x[0] * intervalo, 8), secuencia)
        gen = map(lambda x: funcion(x), gen_x)
        return gen
    else:  # inicio > final
        multiplicador = int((inicio - final)/abs(intervalo)) + 1
        secuencia = (i for i in range(multiplicador))
        gen_x = map(lambda x: round(inicio + x*intervalo, 8), secuencia)
        gen = map(lambda x: funcion(x), gen_x)
        return gen


# print(filtrar(3, '>=', 1)) luego probar arreglar la doble exepcion que se levanta

# print(list(operar(filtrar(extraer_columna("registros", "tiempo_infectado"), '>=', 699650.3), '>=<', 0)))

print(list(evaluar(crear_funcion('gamma', 1, 4), 1, 4, 0.4)))
print(list(evaluar(crear_funcion('gamma', 1, 4), 4, 1, -0.4)))
