from enum import Enum

class OPERACION_ARITMETICA(Enum) :
    PLUS = 1
    MINUS = 2
    MULTIPLY = 3
    DIVIDE = 4

class OPERACION_LOGICA(Enum) :
    MORETHAN = 1
    LESSTHAN = 2
    EQUALS = 3
    NOTEQUALS = 4

class ExpresionNumerica:
    ' Esta clase representa una expresión numérica '

class ExpresionBinaria(ExpresionNumerica) :

    def __init__(self, exp1, exp2, operador) :
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador

class ExpresionNegativo(ExpresionNumerica) :

    def __init__(self, exp) :
        self.exp = exp


class ExpresionNumero(ExpresionNumerica) :

    def __init__(self, val = 0) :
        self.val = val

class ExpresionIdentificador(ExpresionNumerica) :

    def __init__(self, id = "") :
        self.id = id

class ExpresionCadena :
    ' Esta clase representa una Expresión de tipo cadena.'

class ExpresionConcatenar(ExpresionCadena) :

    def __init__(self, exp1, exp2) :
        self.exp1 = exp1
        self.exp2 = exp2

class ExpresionDobleComilla(ExpresionCadena) :

    def __init__(self, val) :
        self.val = val

class ExpresionCadenaNumerico(ExpresionCadena) :

    def __init__(self, exp) :
        self.exp = exp

class ExpresionLogica() :

    def __init__(self, exp1, exp2, operador) :
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador