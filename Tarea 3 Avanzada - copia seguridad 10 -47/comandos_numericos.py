from functools import reduce
from itertools import tee
from errores import ErrorDeTipo, ReferenciaInvalida, ErrorMatematico


def generador_rango(rango):
    try:
        gen = (i for i in range(rango))
        if rango == 0:
            return []
        return gen
    except TypeError as err:
        print("El rango no es un entero, no es posible crear el generador")
        print("Causa: error de tipo")
        raise ErrorDeTipo


def LEN(datos):
    try:  # valida que datos sea iterable
        gen = enumerate(datos)  # generador de tuplas (posicion, elemento)
    except TypeError as err:
        print("no es posible calcular el largo de algo no iterable, solo de una secuencia")
        print("Causa: referencia invalida")
        raise ReferenciaInvalida

    try:  # revisa si la secuencia es vacia
        dupla_filtrada = reduce(lambda x, y: max(x, y), gen)  # ultima dupla
        indice = dupla_filtrada[0]  # posicion del ultimo elemento
        return indice + 1
    except TypeError as err:  # empty secuence: si se genera una secuencia vacia, su largo es 0
        return 0


def PROM(datos):
    try:  # valida si datos es iterable
        copy1, copy2 = tee(datos)
        cantidad = LEN(copy1)
    except TypeError as err:
        print("No es posible calcular el promedio aritmetico de datos no iterables")
        print("Causa: Error de tipo")
        raise ErrorDeTipo

    try:  # valida que el iterable sea de digitos
        suma = reduce(lambda x, y: x + y, copy2)
        return suma/cantidad
    except TypeError as err:
        print("No es posible calcular el promedio arimetico de secuencias de elementos que no sean digitos")
        print("Causa: Error de tipo")
        raise ErrorDeTipo

    except ZeroDivisionError as err:
        print("Causa: Error matematico")
        raise ErrorMatematico


def DESV(datos):
    try:  # valida si datos es iterable
        copy1, copy2, copy3 = tee(datos, 3)
        prom = PROM(copy1)
    except TypeError as err:
        print("No es posible calcular la desviacion estandar de datos no iterables")
        print("Causa: error de tipo")
        raise ErrorDeTipo

    try:  # valida que el iterable sea de digitos
        dif_cuadratica = map(lambda x: (x - prom)**2, copy2)
        suma = reduce(lambda x, y: x + y, dif_cuadratica)
        n = LEN(copy3)
        return (suma/(n - 1))**(1/2)
    except TypeError as err:
        print("No es posible calcular la desviacion estandar de secuencias de elementos que no sean digitos")
        print("Causa: Error de tipo")
        raise ErrorDeTipo
    except ZeroDivisionError as err:
        print(" el largo de la secuencia es 1, por lo que n - 1 = 0")
        print("Causa: Error matematico")
        raise ErrorMatematico


def MEDIAN(datos):
    # se supone que la columna ya esta ordenada
    try:  # valida si datos es iterable
        copy1, copy2, copy3 = tee(datos, 3)
        digitos = filter(lambda x: not (isinstance(x, float) or isinstance(x, int)), copy3)
        if LEN(digitos) != 0:  # revisa si todos los elementos son digitos
            print("No todos los elementos de la secuencia son digitos")
            raise ErrorDeTipo
        indice = (LEN(copy1))/2
        gen = enumerate(copy2)  # generador de tuplas (posicion, elemento)
        # no hay problema en hacer list en medio, dado que tiene como maximo 2 elementos
        medio = list(filter(lambda x: x[0] == int(indice)-1 or x[0] == int(indice) if indice-int(indice) == 0 else x[0] == int(indice), gen))
        elementos_medio = [x[1] for x in medio]  # lista por compresion
        mediana = PROM(elementos_medio)
        return mediana
    except TypeError as err:
        print("No es posible calcular la mediana de datos no iterables")
        print("Causa: error de tipo")
        raise ErrorDeTipo


def VAR(datos):
    try:  # valida si datos es iterable
        copy1, copy2, copy3 = tee(datos, 3)
        prom = PROM(copy1)
    except TypeError as err:
        print("No es posible calcular la varianza de datos no iterables")
        print("Causa: error de tipo")
        raise ErrorDeTipo

    try:  # valida que el iterable sea de digitos
        dif_cuadratica = map(lambda x: (x - prom)**2, copy2)
        suma = reduce(lambda x, y: x + y, dif_cuadratica)
        n = LEN(copy3)
        return suma/(n - 1)
    except TypeError as err:
        print("No es posible calcular la varianza de secuencias de elementos que no sean digitos")
        print("Causa: Error de tipo")
        raise ErrorDeTipo
    except ZeroDivisionError as err:
        print("la secuencia tiene 1 elemento, por lo que n-1 = 0")
        print("Causa: Error matematico")
        raise ErrorMatematico


#print(PROM([1, 'A']))   SE LEVANTAN DOBLE EXEPCIONEEES