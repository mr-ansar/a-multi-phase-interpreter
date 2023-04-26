# Author: Scott Woods <scott.suzuki@gmail.com>
# MIT License
#
# Copyright (c) 2022
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Use lex and bnf packages to turn source text into an AST.

Uses the ply package to implement the grammar for a simple
calculator. Converts flat text into a hierarchy reflecting
the structure of the expression.
"""

import ansar.create as ar
from lib.calc_if import CalcInput
from lib.parser_if import BinaryOperator, UnaryOperator, Operand, OP
from lib.parser_if import AbstractSyntaxTree

# Give parser access to async services
self_service = None

tokens = (
    'NUMBER',
    'PLUS','MINUS','TIMES','DIVIDE',
    'LPAREN','RPAREN',
)

# Tokens

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

def if_halted():
    if self_service.halted:
        self_service.complete(ar.Aborted())

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    if_halted()
    self_service.console('NUMBER "{token}"'.format(token=t.value))
    try:
        value = float(t.value)
    except ValueError:
        value = 0.0
    t.value = Operand(value)
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    if_halted()
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    self_service.warning('Illegal character "{token}"'.format(token=t.value[0]))
    if_halted()
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules

precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS'),
    )

def p_statement_expr(t):
    'statement : expression'
    if_halted()
    self_service.console('statement: expression')
    t[0] = t[1]

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if_halted()
    self_service.console('expression: expression {op} expression'.format(op=t[2]))
    if t[2] == '+'  : t[0] = BinaryOperator(t[1], t[3], OP.ADD)
    elif t[2] == '-': t[0] = BinaryOperator(t[1], t[3], OP.SUB)
    elif t[2] == '*': t[0] = BinaryOperator(t[1], t[3], OP.MUL)
    elif t[2] == '/': t[0] = BinaryOperator(t[1], t[3], OP.DIV)

def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    if_halted()
    self_service.console('expression: - expression')
    t[0] = UnaryOperator(t[2], OP.NEGATE)

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    if_halted()
    self_service.console('expression: ( expression )')
    t[0] = t[2]

def p_expression_number(t):
    'expression : NUMBER'
    if_halted()
    self_service.console('expression: NUMBER')
    t[0] = t[1]

def p_error(t):
    if_halted()
    self_service.fault('syntax error at "{error}"'.format(error=t.value))

import ply.yacc as yacc
parser = yacc.yacc(debug=False)

#
#
def reduce(self, text):
    global self_service
    self_service = self
    t = parser.parse(text)
    return AbstractSyntaxTree(t)

ar.bind(reduce)

#
#
def parse(self, settings, input):
    a = self.create(reduce, input)
    m = self.select(ar.Completed, ar.Stop)
    if isinstance(m, ar.Stop):
        self.halt(a)
        self.select(ar.Completed)
        return ar.Aborted()
    return m.value

ar.bind(parse)

#
#
default_input = '(18 - 6) * (5 + 7)'

if __name__ == '__main__':
	ar.create_object(parse, compiled_input=default_input)
