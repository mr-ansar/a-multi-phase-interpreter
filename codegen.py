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

"""Code generator starting with an AST and ending with an instruction sequence.

A simple tree walk that flattens the tree into a series of post-fix operations.
"""

import ansar.create as ar
from lib.parser_if import BinaryOperator, UnaryOperator, Operand, OP
from lib.parser_if import AbstractSyntaxTree
from lib.codegen_if import VirtualMachine
from lib.codegen_if import Push, Add, Sub, Mul, Div, Negate

def walk(ast):
    if isinstance(ast, BinaryOperator):
        yield from walk(ast.left_operand)
        yield from walk(ast.right_operand)
        if ast.operator == OP.ADD:
            yield Add()
        elif ast.operator == OP.SUB:
            yield Sub()
        elif ast.operator == OP.MUL:
            yield Mul()
        elif ast.operator == OP.DIV:
            yield Div()
        else:
            pass
    elif isinstance(ast, UnaryOperator):
        yield from walk(ast.operand)
        yield Negate()
    elif isinstance(ast, Operand):
        yield Push(ast.value)
    else:
        pass

#
#
def generate(self, ast):
    code = []
    self.console('Instruction block begin')
    for i, c in enumerate(walk(ast)):
        if self.halted:
            return ar.Aborted()
        self.console('[{i:04}] {code}'.format(i=i, code=c.__art__.name))
        code.append(c)
    self.console('Instruction block end')
    return VirtualMachine(code)

ar.bind(generate)

#
#
def codegen(self, settings, input):
    a = self.create(generate, input.ast)
    m = self.select(ar.Completed, ar.Stop)
    if isinstance(m, ar.Stop):
        self.halt(a)
        self.select(ar.Completed)
        return ar.Aborted()
    return m.value

ar.bind(codegen)

#
#
default_input = AbstractSyntaxTree()

if __name__ == '__main__':
	ar.create_object(codegen, factory_input=default_input)
