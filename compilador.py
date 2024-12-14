# ATIVIDADE PRÁTICA - reconhecedor de estruturas em C

from ply import *
import logging

contexto = 0
tipo = ""

def get_contexto():
    return contexto

# Tabela de simbolos
# {ID {valor, tipo, contexto}}
simbolos = {}

# Palavras reservadas <palavra>:<TOKEN>
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'int': 'DINTEGER',
    'double': 'DDOUBLE',
    'float': 'DFLOAT',
    'char': 'DCHAR',
    'const': 'CONST',
    'unsigned': 'UNSIGNED',
    'for': 'FOR',
    'while': 'WHILE',
    'do': 'DO',
    'switch': 'SWITCH',
    'case': 'CASE',
    'free': 'FREE',
    'typedef': 'TYPEDEF',
    'struct': 'STRUCT',
    'bool': 'DBOOLEAN',
    'true': 'TRUE',
    'false': 'FALSE',
    'main': 'MAIN'
}

# Demais TOKENS
tokens = [
        'EQUALS', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER',
        'LPAREN', 'RPAREN', 'LT', 'LE', 'GT', 'GE', 'NE', 'PIPE',
        'COMMA', 'SEMI', 'INTEGER', 'FLOAT', 'STRING', 'ID', 'NEWLINE',
        'RBRACES', 'LBRACES', 'COLON', 'SEMICOLON', 'QUESTION',
        'AMPERSAND', 'LBRACKETS', 'RBRACKETS', 'CHAR'
    ] + list(reserved.values())

t_ignore = ' \t\n'
t_AMPERSAND = r'&'
t_PIPE = r'\|'
t_EQUALS = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_POWER = r'\^'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACES = r'\{'
t_RBRACES = r'\}'
t_LBRACKETS = r'\['
t_RBRACKETS = r'\]'
t_SEMICOLON = r'\;'
t_SEMI = r';'
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_NE = r'!='
t_COMMA = r','
t_COLON = r':'
t_QUESTION = r'\?'
t_INTEGER = r'\d+'
t_FLOAT = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'
t_STRING = r'\".*?\"'
t_CHAR = r'\'.*?\''

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)

# Constroi o analisador léxico
lexer = lex.lex()

# Define-se os procedimentos associados as regras de
# produção da gramática (também é quando definimos a gramática)

#def p_<nome>(p):
#    '<não_terminal> : <TERMINAIS> <nao_terminais> ... ' 
#    <ações semânticas>
# -> ''' para regras com |

def verificar_comp(tipo, tipo_simb):
    if(tipo == "char" and tipo_simb == "char"):
        return True
    elif(tipo == "int" and tipo_simb == "int"):
        return True
    elif((tipo == "double" or tipo == "float") and (tipo_simb == "int" or tipo_simb == "double")):
        return True
    elif(tipo == "string" and (tipo_simb == "string" or tipo_simb == "char")):
        return True
    elif(tipo == "boolean" and tipo_simb == "boolean"):
        return True
    else:
        return False     

def p_inicial(p):
    'inicial : DINTEGER MAIN LPAREN RPAREN bloco SEMICOLON'
    print("Reconheci INICIAL")

def p_bloco(p):
    '''bloco : LBRACES expressoes RBRACES'''
    print("Reconheci Bloco")
    global contexto
    contexto = contexto - 1

def p_expressoes(p):
    '''expressoes : declaracoes
                | declaracoes expressoes
                | ifelse
                | ifelse expressoes
                | forloop
                | forloop expressoes
                | whileloop
                | whileloop expressoes
                | dowhileloop
                | dowhileloop expressoes'''
    global contexto
    contexto = contexto + 1

def p_math(p):
    '''math : literal
            | ID
            | LPAREN ID operacoes math RPAREN
            | ID operacoes math
            | LPAREN literal operacoes math RPAREN
            | literal operacoes math'''
    if(len(p) == 2):
        print("Reconheci a expressão matemática:", p[1])
        if(p[1] in simbolos):
            p[0] = simbolos[p[1]].get('valor')
        else:
            p[0] = p[1]
    elif(len(p) == 4):
        print("Reconheci a expressão matemática:", p[1], p[2], p[3])
        if(p[2] == '+'):
            if(p[1] in simbolos):
                p[0] = float(simbolos[p[1]].get('valor')) + float(p[3])
            else:
                p[0] = float(p[1]) + float(p[3])
        elif(p[2] == '-'):
            if(p[1] in simbolos):
                p[0] = float(simbolos[p[1]].get('valor')) - float(p[3])
            else:
                p[0] = float(p[1]) - float(p[3])
        elif(p[2] == '/'):
            if(p[1] in simbolos):
                p[0] = float(simbolos[p[1]].get('valor')) / float(p[3])
            else:
                p[0] = float(p[1]) / float(p[3])
        elif(p[2] == '*'):
            if(p[1] in simbolos):
                p[0] = float(simbolos[p[1]].get('valor')) * float(p[3])
            else:
                p[0] = float(p[1]) * float(p[3])
        elif(p[2] == '^'):
            if(p[1] in simbolos):
                p[0] = pow(float(simbolos[p[1]].get('valor')), float(p[3]))
            else:
                p[0] = pow(float(p[1]), float(p[3]))

    elif(len(3) == 6):
        print("Reconheci a expressão matemática:", p[1], p[2], p[3], p[4], p[5])
        if(p[3] == '+'):
            if(p[1] in simbolos):
                p[0] = float(simbolos[p[2]].get('valor')) + float(p[4])
            else:
                p[0] = float(p[2]) + float(p[4])
        elif(p[3] == '-'):
            if(p[1] in simbolos):
                p[0] = float(simbolos[p[2]].get('valor')) - float(p[4])
            else:
                p[0] = float(p[2]) - float(p[4])
        elif(p[3] == '/'):
            if(p[1] in simbolos):
                p[0] = float(simbolos[p[2]].get('valor')) / float(p[4])
            else:
                p[0] = float(p[2]) / float(p[4])
        elif(p[3] == '*'):
            if(p[1] in simbolos):
                p[0] = float(simbolos[p[2]].get('valor')) * float(p[4])
            else:
                p[0] = float(p[2]) * float(p[4])
        elif(p[3] == '^'):
            if(p[1] in simbolos):
                p[0] = pow(float(simbolos[p[2]].get('valor')), float(p[4]))
            else:
                p[0] = pow(float(p[2]), float(p[4]))

def p_operacoes(p):
    '''operacoes : DIVIDE
                    | PLUS
                    | MINUS
                    | TIMES
                    | POWER'''
    p[0] = p[1]

def p_atribuicoes(p):
    '''atribuicoes : EQUALS
                    | PLUS EQUALS
                    | MINUS EQUALS
                    | LT LT'''
    if(len(p) == 2):                
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2]



def p_tipos(p):
    ''' tipos : DINTEGER 
            | DCHAR 
            | DFLOAT
            | DDOUBLE
            | DBOOLEAN'''
    global tipo
    p[0] = p[1]
    tipo = p[1]

def p_declaracoes(p):
    '''declaracoes : ID SEMICOLON
                | ID COMMA declaracoes
                | ID atribuicoes math SEMICOLON
                | ID atribuicoes math COMMA declaracoes
                | ID atribuicoes STRING SEMICOLON
                | ID atribuicoes CHAR SEMICOLON
                | tipos ID SEMICOLON 
                | tipos ID COMMA declaracoes
                | tipos ID atribuicoes math SEMICOLON
                | tipos ID atribuicoes STRING SEMICOLON
                | tipos ID atribuicoes CHAR SEMICOLON'''
    
    if(len(p) == 6 and p[4] == ","):
        simbolos[p[1]] = {'valor': p[3], 'tipo': tipo, 'contexto':get_contexto()}
        p[0] = p[1]
        #print("Teste 1 -> ", p[1], p[3])
    elif(len(p) == 6):
        simbolos[p[2]] = {'valor': p[4], 'tipo': p[1], 'contexto':get_contexto()}
        #print("Teste 2 -> ", p[2], p[4])
        p[0] = p[1]
    elif(len(p) == 5 and p[2] == "="):
        simbolos[p[1]]['valor'] = p[3]
        #print("Teste 3 -> ", p[1], p[3])
        p[0] = p[1]
    elif(len(p) == 5 and p[3] == ","):
        simbolos[p[2]] = {'valor': None, 'tipo': p[1], 'contexto':get_contexto()}
        #tipo = p[1]
        #print("Teste 4 -> ", p[1], p[2])
        p[0] = p[1]
    elif(len(p) == 4 and p[2] == ","):
        simbolos[p[1]] = {'valor': None, 'tipo': tipo, 'contexto':get_contexto()}
        #print("Teste 6 -> ", p[1])
        p[0] = p[1]
    elif(len(p) == 4):
        simbolos[p[2]] = {'valor': None, 'tipo': p[1], 'contexto':get_contexto()}
        #print("Teste 7 -> ", p[1], p[2])
        p[0] = p[2]
    elif(len(p) == 3):
        simbolos[p[1]] = {'valor': None, 'tipo': tipo, 'contexto':get_contexto()}
        #print("Teste 8 -> ", p[1])
        p[0] = p[1]

def p_ifelse(p):
    '''ifelse : IF LPAREN condicao RPAREN bloco
                | IF LPAREN condicao RPAREN bloco ELSE bloco
                | IF LPAREN condicao RPAREN bloco ELSE ifelse'''
    print("Reconheci o loop if-else")

def p_forloop(p):
    '''forloop : FOR LPAREN declaracoes condicao SEMICOLON ID atribuicoes math RPAREN bloco
                | FOR LPAREN declaracoes condicao SEMICOLON ID PLUS PLUS RPAREN bloco
                | FOR LPAREN declaracoes condicao SEMICOLON ID MINUS MINUS RPAREN bloco'''
    print("Reconheci o loop for")

def p_whileloop(p):
    '''whileloop : WHILE LPAREN condicao RPAREN bloco'''

def p_dowhileloop(p):
    '''dowhileloop : DO bloco WHILE LPAREN condicao RPAREN SEMICOLON'''
    global contexto
    contexto = contexto - 1

def p_comparador(p):
    '''comparador : EQUALS EQUALS
                    | LT
                    | LE
                    | GT
                    | GE
                    | NE
                    | AMPERSAND
                    | AMPERSAND AMPERSAND
                    | PIPE
                    | PIPE PIPE'''
    if(len(p) == 3):
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]

def p_literal(p):
    '''literal : TRUE
                | FALSE
                | INTEGER
                | FLOAT'''
    p[0] = p[1]
    
def p_condicao(p):
    '''condicao : math
                | STRING
                | CHAR
                | math comparador condicao'''
    if(len(p) == 4):
        print("Reconheci a condição:" , p[1], p[2], p[3])
    else:
        p[0] = p[1]

yacc.yacc()

logging.basicConfig(
    level=logging.INFO,
    filename="parselog.txt"
)

# entrada do arquivo
file = open("input.txt",'r')
data = file.read()

# string de teste como entrada do analisador léxico
lexer.input(data)

# Tokenização
for tok in lexer:
     print(tok)

# chama o parser
yacc.parse(data, debug=logging.getLogger())

print(simbolos)
