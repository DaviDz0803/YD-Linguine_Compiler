import os
import ply.lex as lex
import gramatica as g
import ts as TS
from expresiones import *
from instrucciones import *


def procesar_servir(instr, ts) :
    print('> ', resolver_chain(instr.cad, ts))

def procesar_definicion(instr, ts) :
    simbolo = TS.Simbolo(instr.id, TS.TIPO_DATO.NUMERO, 0)      # inicializamos con 0 como valor por defecto
    ts.agregar(simbolo)

def procesar_asignacion(instr, ts) :
    val = resolver_expresion_aritmetica(instr.expNumerica, ts)
    simbolo = TS.Simbolo(instr.id, TS.TIPO_DATO.NUMERO, val)
    ts.actualizar(simbolo)

def procesar_durante(instr, ts) :
    while resolver_expreision_logica(instr.expLogica, ts) :
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        procesar_instrucciones(instr.instrucciones, ts_local)

def procesar_sitiene(instr, ts) :
    val = resolver_expreision_logica(instr.expLogica, ts)
    if val :
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        procesar_instrucciones(instr.instrucciones, ts_local)

def procesar_sino(instr, ts) :
    val = resolver_expreision_logica(instr.expLogica, ts)
    if val :
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        procesar_instrucciones(instr.instrIfVerdadero, ts_local)
    else :
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        procesar_instrucciones(instr.instrIfFalso, ts_local)

def resolver_chain(expCad, ts) :
    if isinstance(expCad, ExpresionConcatenar) :
        exp1 = resolver_chain(expCad.exp1, ts)
        exp2 = resolver_chain(expCad.exp2, ts)
        return exp1 + exp2
    elif isinstance(expCad, ExpresionDobleComilla) :
        return expCad.val
    elif isinstance(expCad, ExpresionCadenaNumerico) :
        return str(resolver_expresion_aritmetica(expCad.exp, ts))
    else :
        print('Error: Expresión chain no válida')


def resolver_expreision_logica(expLog, ts) :
    exp1 = resolver_expresion_aritmetica(expLog.exp1, ts)
    exp2 = resolver_expresion_aritmetica(expLog.exp2, ts)
    if expLog.operador == OPERACION_LOGICA.MORETHAN : return exp1 > exp2
    if expLog.operador == OPERACION_LOGICA.LESSTHAN : return exp1 < exp2
    if expLog.operador == OPERACION_LOGICA.ASSIGN : return exp1 == exp2
    if expLog.operador == OPERACION_LOGICA.NOTEQUALS : return exp1 != exp2

def resolver_expresion_aritmetica(expNum, ts) :
    if isinstance(expNum, ExpresionBinaria) :
        exp1 = resolver_expresion_aritmetica(expNum.exp1, ts)
        exp2 = resolver_expresion_aritmetica(expNum.exp2, ts)
        if expNum.operador == OPERACION_ARITMETICA.PLUS : return exp1 + exp2
        if expNum.operador == OPERACION_ARITMETICA.MINUS : return exp1 - exp2
        if expNum.operador == OPERACION_ARITMETICA.MULTIPLY: return exp1 * exp2
        if expNum.operador == OPERACION_ARITMETICA.DIVIDE : return exp1 / exp2
    elif isinstance(expNum, ExpresionNegativo) :
        exp = resolver_expresion_aritmetica(expNum.exp, ts)
        return exp * -1
    elif isinstance(expNum, ExpresionNumero) :
        return expNum.val
    elif isinstance(expNum, ExpresionIdentificador) :
        return ts.obtener(expNum.id).valor


def procesar_instrucciones(instrucciones, ts) :
    ## lista de instrucciones recolectadas
    for instr in instrucciones :
        if isinstance(instr, Servir) : procesar_servir(instr, ts)
        elif isinstance(instr, Definicion) : procesar_definicion(instr, ts)
        elif isinstance(instr, Asignacion) : procesar_asignacion(instr, ts)
        elif isinstance(instr, Durante) : procesar_durante(instr, ts)
        elif isinstance(instr, SiTiene) : procesar_sitiene(instr, ts)
        elif isinstance(instr, SiNo) : procesar_sino(instr, ts)
        else : print('Error: instrucción no válida')



def buscarFicheros(directorio):
    ficheros = []
    numArchivo = ''
    respuesta = False
    cont = 1
    for base, dirs, files in os.walk(directorio):
        ficheros.append(files)
        
    for file in files:
        print (str(cont)+". "+file)
        cont = cont+1
    
    while respuesta == False:
        numArchivo = input('\nNumero del test: ')
        for file in files:
            if file == files[int(numArchivo)-1]:
                respuesta = True
                break

    print ("Has escogido \"%s\" \n" %files[int(numArchivo)-1])

    return files[int(numArchivo)-1]


directorio = './test/'
archivo = buscarFicheros(directorio)
#print(directorio+archivo)
f = open(directorio+archivo, "r")

#f = open("./entrada.txt", "r")
input = f.read()

instrucciones = g.parse(input) #Recibe el archivo y se lo pasa a 
                                #gramatica
ts_global = TS.TablaDeSimbolos()

procesar_instrucciones(instrucciones, ts_global)
