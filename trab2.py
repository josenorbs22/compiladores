# ATIVIDADE PRÁTICA - reconhecedor de estruturas em C

from ply import *
import logging

contexto = 0

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

def t_eof(t):
    # Get more input (Example)
    return None

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

def p_inicial(p):
    'inicial : DINTEGER MAIN LPAREN RPAREN bloco SEMICOLON'
    print("Reconheci INICIAL")

def p_bloco(p):
    '''bloco : LBRACES expressoes RBRACES'''
    print("Reconheci Bloco Principal")

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

def p_math(p):
    '''math : literal
            | ID
            | LPAREN ID operacoes math RPAREN
            | ID operacoes math
            | LPAREN literal operacoes math RPAREN
            | literal operacoes math'''
    if(len(p) == 2):
        print("Reconheci a expressão matemática:", p[1])
        p[0] = p[1]
    elif(len(p) == 4):
        print("Reconheci a expressão matemática:", p[1], p[2], p[3])
        p[0] = p[1]
    elif(len(3) == 6):
        print("Reconheci a expressão matemática:", p[1], p[2], p[3], p[4], p[5])
        p[0] = p[1]

def p_operacoes(p):
    '''operacoes : DIVIDE
                    | PLUS
                    | MINUS
                    | TIMES
                    | POWER'''

def p_declaracoes(p):
    '''declaracoes : ID SEMICOLON
                | ID COMMA declaracoes
                | ID EQUALS math SEMICOLON
                | ID EQUALS math COMMA declaracoes SEMICOLON
                | tipos ID SEMICOLON 
                | tipos ID COMMA declaracoes
                | tipos ID declaracoes SEMICOLON
                | tipos ID EQUALS math SEMICOLON'''

    if(len(p) == 4):
        simbolos[p[2]] = {'valor': None, 'tipo': p[1], 'contexto':get_contexto()}
        print("Reconheci Declarações", p[1], p[2])
        p[0] = p[2]
    elif(len(p) == 5):
        simbolos[p[2]] = {'valor': p[4], 'tipo': p[1], 'contexto':get_contexto()}
        p[0] = p[2]
    elif(len(p) == 4 and p[2] == "EQUALS"):
        simbolos[p[1]] = {'valor': p[3], 'tipo': None, 'contexto':get_contexto()}
        p[0] = p[1]
    elif(len(p) == 3):
        simbolos[p[1]] = {'valor': None, 'tipo': None, 'contexto':get_contexto()}
        p[0] = p[1]
    elif(len(p) == 4 and p[2] == "COMMA"):
        simbolos[p[1]] = {'valor': None, 'tipo': None, 'contexto':get_contexto()}
        p[0] = p[1]
    elif(len(p) == 6):
        simbolos[p[1]] = {'valor': p[3], 'tipo': None, 'contexto':get_contexto()}
        p[0] = p[1]
    elif(len(p) == 4 and p[3] == "COMMA"):
        simbolos[p[2]] = {'valor': None, 'tipo': p[1], 'contexto':get_contexto()}
        p[0] = p[1]
        simbolos[p[4]] = {'valor': None, 'tipo': p[1], 'contexto':get_contexto()}
    elif(len(p) == 4 and p[2] == "EQUALS"):
        simbolos[p[1]] = {'valor': p[3], 'tipo': None, 'contexto':get_contexto()}
        p[0] = p[1]

def p_ifelse(p):
    '''ifelse : IF LPAREN condicao RPAREN bloco
                | IF LPAREN condicao RPAREN bloco ELSE bloco
                | IF LPAREN condicao RPAREN bloco ELSE ifelse'''

def p_forloop(p):
    '''forloop : FOR LPAREN declaracoes SEMICOLON condicao SEMICOLON math RPAREN bloco'''

def p_whileloop(p):
    '''whileloop : WHILE LPAREN condicao RPAREN bloco'''

def p_dowhileloop(p):
    '''dowhileloop : DO LBRACES bloco RBRACES WHILE LPAREN condicao RPAREN SEMICOLON'''

def p_tipos(p):
    ''' tipos : DINTEGER 
            | DCHAR 
            | DFLOAT
            | DDOUBLE
            | DBOOLEAN'''
    p[0] = p[1]

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
        print("Reconheci a comparação:", p[1], p[2])
        p[0] = p[1] + p[2]
    else:
        print("Reconheci a comparação:", p[1])
        p[0] = p[1]

def p_literal(p):
    '''literal : TRUE
                | FALSE
                | INTEGER
                | FLOAT
                | STRING
                | CHAR'''
    p[0] = p[1]
    
def p_condicao(p):
    '''condicao : math
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
