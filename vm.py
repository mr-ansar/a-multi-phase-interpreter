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

"""Virtual machine starting with block of generated code and ending with a value.

An iteration of the code block and call to each instruction, passing
a push/pop value stack.
"""

import ansar.create as ar
from lib.codegen_if import Push, Add, Sub, Mul, Div, Negate
from lib.codegen_if import VirtualMachine
from lib.vm_if import MachineValue

#
#
def execute(self, code):
    stack = []
    self.console('Virtual machine start')
    for c in code:
        if self.halted:
            return ar.Aborted()
        c(stack)
        t = ', '.join(['{value}'.format(value=v) for v in stack])
        self.console('{code:8} [{values}]'.format(code=c.__art__.name, values=t))
    self.console('Virtual machine end ({value})'.format(value=stack[-1]))
    return MachineValue(stack[-1])

ar.bind(execute)

#
#
def vm(self, settings, input):
    if input.code is None:
        return MachineValue(0.0)
    a = self.create(execute, input.code)
    m = self.select(ar.Completed, ar.Stop)
    if isinstance(m, ar.Stop):
        self.halt(a)
        self.select(ar.Completed)
        return ar.Aborted()
    return m.value

ar.bind(vm)

#
#
default_input = VirtualMachine()

if __name__ == '__main__':
	ar.create_object(vm, factory_input=default_input)
