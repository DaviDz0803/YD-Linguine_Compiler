class Instruccion:
    ''' This is an abstract class '''

class Servir(Instruccion):
    '''This is a print class '''
    def __init__(self,  cad):
        self.cad = cad

class Durante(Instruccion):
    ''' This is a while class '''
    def __init__(self, expLogica, instrucciones = []):
        self.expLogica = expLogica
        self.instrucciones = instrucciones

class Definicion(Instruccion) :
    ''' Ejemplo: variable abc; '''

    def __init__(self, id):
        self.id = id

class Asignacion(Instruccion) :
    ''' Ejemplo: abc = 12; '''
    
    def __init__(self, id, expNumerica) :
        self.id = id
        self.expNumerica = expNumerica

class SiTiene(Instruccion) : 
    '''This is a logic class (If)'''

    def __init__(self, expLogica, instrucciones = []) :
        self.expLogica = expLogica
        self.instrucciones = instrucciones

class SiNo(Instruccion) : 
    '''This is a logic class (else)'''

    def __init__(self, expLogica, instrIfVerdadero = [], instrIfFalso = []) :
        self.expLogica = expLogica
        self.instrIfVerdadero = instrIfVerdadero
        self.instrIfFalso = instrIfFalso