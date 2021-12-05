from expresiones import *
from instrucciones import *
import ply.lex as lex
import ply.yacc as yacc


reservadas = {
    'cantidad' : 'CANTIDAD',
    'servir' : 'SERVIR',
    'durante' : 'DURANTE',
    'sitiene' : 'SITIENE',
    'sino' : 'SINO'
}

tokens  = [
    'SEMMICOLOM',
    'LKEY',
    'RKEY',
    'LPARENT',
    'RPARENT',
    'ASSIGN',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'CONCAT',
    'LESSTHAN',
    'MORETHAN',
    'EQUALS',
    'NOTEQUALS',
    'ONZA', 
    'GRAMO', 
    'CHAIN', 
    'ID'
] + list(reservadas.values())


t_SEMMICOLOM = r';'
t_LKEY       = r'{'
t_RKEY       = r'}'
t_LPARENT    = r'\('
t_RPARENT    = r'\)'
t_ASSIGN     = r'='
t_PLUS       = r'\+'
t_MINUS      = r'-'
t_MULTIPLY   = r'\*'
t_DIVIDE     = r'/'
t_CONCAT     = r'&'
t_LESSTHAN   = r'<'
t_MORETHAN   = r'>'
t_EQUALS     = r'=='
t_NOTEQUALS  = r'!='

def t_GRAMO(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_ONZA(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value.lower(),'ID')    
     return t

def t_CHAIN(t):
    r'\".*?\"'
    t.value = t.value[1:-1] 
    return t 

def t_MULTI_COMMENT(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')


def t_SIMPLE_COMMENT(t):
    r'//.*\n'
    t.lexer.lineno += 1


t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print ("caracter ilegal " + t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()


# Asociación de operadores y precedencia
precedence = (
    ('left','CONCAT'),
    ('left','PLUS','MINUS'),
    ('left','MULTIPLY','DIVIDE'),
    ('right','UMENOS'),
    )

# Definición de la gramática




def p_init(t) :
    'init            : instrucciones'
    t[0] = t[1]

def p_instrucciones_lista(t) :
    'instrucciones    : instrucciones instruccion'
    t[1].append(t[2])
    t[0] = t[1]


def p_instrucciones_instruccion(t) :
    'instrucciones    : instruccion '
    t[0] = [t[1]]

def p_instruccion(t) :
    '''instruccion      : servir_instr
                        | definicion_instr
                        | asignacion_instr
                        | durante_instr
                        | sitiene_instr
                        | sino_instr'''
    t[0] = t[1]

def p_instruccion_servir(t) :
    'servir_instr     : SERVIR LPARENT expresion_chain RPARENT SEMMICOLOM'
    t[0] =Servir(t[3])

def p_instruccion_definicion(t) :
    'definicion_instr   : CANTIDAD ID SEMMICOLOM'
    t[0] =Definicion(t[2])

def p_asignacion_instr(t) :
    'asignacion_instr   : ID ASSIGN expresion_numerica SEMMICOLOM'
    t[0] =Asignacion(t[1], t[3])

def p_durante_instr(t) :
    'durante_instr     : DURANTE LPARENT expresion_logica RPARENT LKEY instrucciones RKEY'
    t[0] =Durante(t[3], t[6])

def p_sitiene_instr(t) :
    'sitiene_instr           : SITIENE LPARENT expresion_logica RPARENT LKEY instrucciones RKEY'
    t[0] =SiTiene(t[3], t[6])

def p_sino_instr(t) :
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

def p_expresion_concatenacion(t) :
    'expresion_chain     : expresion_chain CONCAT expresion_chain'
    t[0] = ExpresionConcatenar(t[1], t[3])

def p_expresion_chain(t) :
    'expresion_chain     : CHAIN'
    t[0] = ExpresionDobleComilla(t[1])

def p_expresion_cadena_numerico(t) :                               #REVISAR, 
    'expresion_chain     : expresion_numerica'                     #Pendiente
    t[0] = ExpresionCadenaNumerico(t[1])

def p_expresion_logica(t) :
    '''expresion_logica : expresion_numerica MORETHAN expresion_numerica
                        | expresion_numerica LESSTHAN expresion_numerica
                        | expresion_numerica EQUALS expresion_numerica
                        | expresion_numerica NOTEQUALS expresion_numerica'''
    if t[2] == '>'    : t[0] = ExpresionLogica(t[1], t[3], OPERACION_LOGICA.MORETHAN)
    elif t[2] == '<'  : t[0] = ExpresionLogica(t[1], t[3], OPERACION_LOGICA.LESSTHAN)
    elif t[2] == '==' : t[0] = ExpresionLogica(t[1], t[3], OPERACION_LOGICA.EQUALS)
    elif t[2] == '!=' : t[0] = ExpresionLogica(t[1], t[3], OPERACION_LOGICA.NOTEQUALS)



def p_error(t):
    print(t)
    print("Error sintáctico en '%s'" % t.value)


parser = yacc.yacc()


def parse(input) :
    return parser.parse(input)