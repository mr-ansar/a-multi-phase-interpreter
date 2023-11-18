# Author: Scott Woods <scott.18.ansar@gmail.com.com>
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

"""A simple calculator.

A very slow implementation of a calculator that delegates work
to the following child processes;

* parser - lex/bnf tools that turn text into tree
* codegen - recursive walk of tree to generate executable code
* vm - machine that executes code and produces a value
"""

import ansar.create as ar
from lib.calc_if import CalcInput
from lib.parser_if import AbstractSyntaxTree
from lib.codegen_if import VirtualMachine
from lib.vm_if import MachineValue

#
#
def calc(self, settings, input):
	# Phase #1 - compile to an abstract syntax tree.
	a = self.create(ar.Process, 'parser', input=input)
	m = self.select(ar.Completed, ar.Stop)
	if isinstance(m, ar.Stop):
		self.send(m, a)
		self.select(ar.Completed)
		return ar.Aborted()
	r = m.value
	if not isinstance(r, AbstractSyntaxTree):
		return r

	# Phase #2 - encode abstract syntax tree to machine code.
	self.create(ar.Process, 'codegen', input=r)
	m = self.select(ar.Completed, ar.Stop)
	if isinstance(m, ar.Stop):
		self.send(m, a)
		self.select(ar.Completed)
		return ar.Aborted()
	r = m.value
	if not isinstance(r, VirtualMachine):
		return r

	self.create(ar.Process, 'vm', input=r)
	m = self.select(ar.Completed, ar.Stop)
	if isinstance(m, ar.Stop):
		self.send(m, a)
		self.select(ar.Completed)
		return ar.Aborted()
	r = m.value
	return r

ar.bind(calc)

default_input = '(10 - 3) * (4 + 5)'

#
#
if __name__ == '__main__':
	ar.create_object(calc, factory_input=default_input)
