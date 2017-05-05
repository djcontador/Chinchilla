import math
from errores import ErrorDeTipo, ReferenciaInvalida
from functools import reduce
from comandos_numericos import LEN

variables = {}


def crear_funcion(nombre_modelo, *parametros):
    if nombre_modelo == 'normal':
        # valida el numero de parametros
        if LEN(parametros) != 2:
            print(" la distribucion normal recibe 2 parametros")
            raise ErrorDeTipo

        mu = parametros[0]
        sigma = parametros[1]

        # valida si los parametros son numeros
        if not isinstance(mu, int) and not isinstance(mu, float):
            print("los paramentros solo pueden ser numeros")
            raise ErrorDeTipo
        if not isinstance(sigma, int) and not isinstance(sigma, float):
            print("los paramentros solo pueden ser numeros")
            raise ErrorDeTipo
        # valida 0 < sigma
        if sigma >= 0:
            print("sigma debe ser mayor que cero")
            raise ErrorDeTipo

        def normal(x):
            # valida si x es un numero
            if not isinstance(x, int) and not isinstance(x, float):
                print("la funcion normal solo se puede evaluar con un numero")
                raise ErrorDeTipo
            y = (1/((2*math.pi*(sigma**2))**2))*math.e**((-1/2)*((x-mu)/sigma)**2)
            return y
        return normal

    elif nombre_modelo == 'exponencial':
        # valida que solo se entrege 1 parametro
        if LEN(parametros) != 1:
            print(" la distribucion exponencial recibe 1 parametro")
            raise ErrorDeTipo

        nu = parametros[0]

        # valida que los parametros son numeros
        if not isinstance(nu, int) and not isinstance(nu, float):
            print("los paramentros solo pueden ser numeros")
            raise ErrorDeTipo
        # valida nu > 0
        if nu <= 0:
            print("el parametro nu solo puede ser mayor a cero")
            raise ErrorDeTipo

        def exponencial(x):
            # valida que x sea un numero
            if not isinstance(x, int) and not isinstance(x, float):
                print("la funcion exponencial solo se puede evaluar con un numero")
                raise ErrorDeTipo
            y = nu*math.e**(-1*nu*x)
            # valida x>=0
            if x < 0:
                print("la funcion exponencial no se puede evaluar con numeros negativos...")
                raise ErrorDeTipo
            return y
        return exponencial

    elif nombre_modelo == 'gamma':
        # valida que solo reciba 2 paramentros
        if LEN(parametros) != 2:
            print("la distribucion gamma recibe 2 parametros")
            raise ErrorDeTipo

        nu = parametros[0]
        k = parametros[1]

        # valida que los parametros son numeros
        if not isinstance(nu, int) and not isinstance(nu, float):
            print("los paramentros solo pueden ser numeros")
            raise ErrorDeTipo
        if not isinstance(k, int) and not isinstance(k, float):
            print("los paramentros solo pueden ser numeros")
            raise ErrorDeTipo
        factorial = reduce(lambda x, y: x*y, (i for i in range(1, int(k))))

        def gamma(x):
            # valida que x sea un numero
            if not isinstance(x, int) and not isinstance(x, float):
                print("la funcion gamma solo se puede evaluar con un numero")
                raise ErrorDeTipo
            y = ((nu**k)/factorial)*(x**(k-1))*math.e**(-1*nu*x)
            # valida x>=0
            if x < 0:
                print("la funcion gamma no se puede evaluar con numeros negativos...")
                raise ErrorDeTipo
            return y
        return gamma


# TODO
def asignar(variable, comando_dato):
    # valida que la variable sea un string
    if not isinstance(variable, str):
        print("la variable no es un string")
        raise ErrorDeTipo

    distribuciones = ['normal', 'exponencial', 'gamma']
    rql = ["asignar", "crear_funcion", 'graficar', 'extraer_columna', 'filtrar', 'operar', 'evaluar', 'LEN', 'PROM',
           'DESV', 'MEDIAN', 'VAR', 'comparar_columna', 'comparar', 'do_if']
    if variable in distribuciones or variable in rql:
        print("no se puede crear una variable con el nombre una funcion de RQL o una distribucion de probabilidad")
        raise ErrorDeTipo
    global variables
    variables[variable] = comando_dato


# TODO
def graficar(columna, opcion):
    pass

#print(crear_funcion('gamma', 1, 4)(9))
asignar('a', 1)
asignar('b', 2)
asignar('a', "caca")
asignar('comando', crear_funcion('exponencial', 4))
print(variables)
