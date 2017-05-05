class ArgumentoInvalido(Exception):
    def __init__(self):
        super().__init__('Argumento invalido')


class ReferenciaInvalida(Exception):
    def __init__(self):
        super().__init__('Referencia invalida')


class ErrorDeTipo(Exception):
    def __init__(self):
        super().__init__('Error de tipo')


class ErrorMatematico(Exception):
    def __init__(self):
        super().__init__('Error matematico')


class ImposibleProcesar(Exception):
    def __init__(self):
        super().__init__('Imposible Procesar')