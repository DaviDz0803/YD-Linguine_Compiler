from expresiones import *
from palabrasReservadas import *
from analizadorLexico import *
import ply.yacc as yacc


precedence = (
    ('left','CONCAT'),
    ('left','PLUS','MINUS'),
    ('left','MULTIPLY','DIVIDE'),
    ('right','UMENOS'),
    )

def p_init(t):
    'init            : instrucciones'
    t[0] = t[1]

def p_instrucciones_lista(t):
    'instrucciones    : instrucciones instruccion'
    t[1].append(t[2])
    t[0] = t[1]

def p_instrucciones_instruccion(t):
    'instrucciones    : instruccion '
    t[0] = [t[1]]

def p_instruccion(t):
    '''instruccion      : servir_instr
                        | definicion_instr
                        | asignacion_instr
                        | durante_instr
                        | sitiene_instr
                        | sino_instr'''
    t[0] = t[1]

def p_instruccion_servir(t):
    'servir_instr     : SERVIR LPARENT expresion_chain RPARENT SEMMICOLOM'
    t[0] =Servir(t[3])

def p_instruccion_definicion(t):
    'definicion_instr   : INGREDIENTE ID SEMMICOLOM'
    t[0] =Definicion(t[2])

def p_asignacion_instr(t):
    'asignacion_instr   : ID ASSIGN expresion_numerica SEMMICOLOM'
    t[0] =Asignacion(t[1], t[3])

def p_durante_instr(t):
    'durante_instr     : DURANTE LPARENT expresion_logica RPARENT LKEY instrucciones RKEY'
    t[0] =Durante(t[3], t[6])

def p_sitiene_instr(t):
    'sitiene_instr           : SITIENE LPARENT expresion_logica RPARENT LKEY instrucciones RKEY'
    t[0] =SiTiene(t[3], t[6])

def p_sino_instr(t):
    'sino_instr      : SITIENE LPARENT expresion_logica RPARENT LKEY instrucciones RKEY SINO LKEY instrucciones RKEY'
    t[0] =SiNo(t[3], t[6], t[10])

def p_expresion_binaria(t):
    '''expresion_numerica : expresion_numerica PLUS expresion_numerica
                        | expresion_numerica MINUS expresion_numerica
                        | expresion_numerica MULTIPLY expresion_numerica
                        | expresion_numerica DIVIDE expresion_numerica'''
    if t[2] == '+'  : t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.PLUS)
    elif t[2] == '-': t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.MINUS)
    elif t[2] == '*': t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.MULTIPLY)
    elif t[2] == '/': t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.DIVIDE)


def p_expresion_unaria(t):
    'expresion_numerica : MINUS expresion_numerica %prec UMENOS'
    t[0] = ExpresionNegativo(t[2])

def p_expresion_agrupacion(t):
    'expresion_numerica : LPARENT expresion_numerica RPARENT'
    t[0] = t[2]

def p_expresion_number(t):
    '''expresion_numerica : ONZA
                        | GRAMO'''
    t[0] = ExpresionNumero(t[1])

def p_expresion_id(t):
    'expresion_numerica   : ID'
    t[0] = ExpresionIdentificador(t[1])

def p_expresion_concatenacion(t):
    'expresion_chain     : expresion_chain CONCAT expresion_chain'
    t[0] = ExpresionConcatenar(t[1], t[3])

def p_expresion_chain(t):
    'expresion_chain     : CHAIN'
    t[0] = ExpresionDobleComilla(t[1])

def p_expresion_cadena_numerico(t):  
    'expresion_chain     : expresion_numerica'
    t[0] = ExpresionCadenaNumerico(t[1])

def p_expresion_logica(t):
    '''expresion_logica : expresion_numerica MORETHAN expresion_numerica
                        | expresion_numerica LESSTHAN expresion_numerica
                        | expresion_numerica EQUALS expresion_numerica
                        | expresion_numerica NOTEQUALS expresion_numerica'''
    if t[2] == '>'    : t[0] = ExpresionLogica(t[1], t[3], OPERACION_LOGICA.MORETHAN)
    elif t[2] == '<'  : t[0] = ExpresionLogica(t[1], t[3], OPERACION_LOGICA.LESSTHAN)
    elif t[2] == '==' : t[0] = ExpresionLogica(t[1], t[3], OPERACION_LOGICA.EQUALS)
    elif t[2] == '!=' : t[0] = ExpresionLogica(t[1], t[3], OPERACION_LOGICA.NOTEQUALS)

def p_error(t):
    print("Error sintáctico en '%s'" % t.value)

parser = yacc.yacc()

def parse(input):
    return parser.parse(input)