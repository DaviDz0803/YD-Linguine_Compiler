import ply.lex as lex
import re
import codecs
import os 
import sys

reservadas = {
    'cantidad' : 'CANTIDAD',
    'servir' : 'SERVIR',
    'durante' : 'DURANTE',
    'if' : 'IF',
    'else' : 'ELSE'
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
    'ONZA', #DECIMAL
    'GRAMO', #ENTEROS
    'CHAIN', #CADENA
    'ID'
] + list(reservadas.values())


# Tokens
t_SEMMICOLOM = r';'
t_LKEY = r'{'
t_RKEY = r'}'
t_LPARENT = r'\('
t_RPARENT = r'\)'
t_ASSIGN = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_CONCAT = r'&'
t_LESSTHAN = r'<'
t_MORETHAN = r'>'
t_EQUALS = r'=='
t_NOTEQUALS = r'!='


def t_ONZA(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_GRAMO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value.lower(),'ID')    # Check for reserved words
     return t

def t_CHAIN(t):
    r'\".*?\"'
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

# Comentario de múltiples líneas /* .. */
def t_MULTI_COMMENT(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

# Comentario simple // ...
def t_SIMPLE_COMENT(t):
    r'//.*\n'
    t.lexer.lineno += 1

# Caracteres ignorados
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

#def buscarFicheros(directorio):
# 	ficheros = []
# 	numArchivo = ''
# 	respuesta = False
# 	cont = 1

# 	for base, dirs, files in os.walk(directorio):
# 		ficheros.append(files)

# 	for file in files:
# 		print (str(cont)+". "+file)
# 		cont = cont+1

# 	while respuesta == False:
# 		numArchivo = input('\nNumero del test: ')
# 		for file in files:
# 			if file == files[int(numArchivo)-1]:
# 				respuesta = True
# 				break

# 	print ("Has escogido \"%s\" \n" %files[int(numArchivo)-1])

# 	return files[int(numArchivo)-1]

#directorio = 'C://Users/daviddz/Documents/Git/Github/Compilador/YD-Compilador/test/'
#archivo = buscarFicheros(directorio)
#test = directorio+archivo
#fp = codecs.open(test,"r","utf-8")
#cadena = fp.read()
#fp.close()

#lexer = lex.lex()
#lexer.input(cadena)

#while True:
#    tok = lexer.token()
#    if not tok : break
#    print (tok)