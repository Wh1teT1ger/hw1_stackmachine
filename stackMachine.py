import sys


class Stack:
    def __init__(self):
        self.items = []

    def push(self, value):
        self.items.append(value)

    def pop(self):
        if len(self.items) > 0:
            return self.items.pop()
        else:
            raise RuntimeError("stack is empty")


class Machine:
    def __init__(self, code):
        self.code = code
        self.data_stack = Stack()
        self.return_stack = Stack()
        self.instruction_pointer = 0
        self.heap = {}
        self.instructions_dict = {'%': self.mod,
                                  '*': self.mult,
                                  '+': self.add,
                                  '-': self.sub,
                                  '/': self.div,
                                  "==": self.eq,
                                  'cast_int': self.cast_int,
                                  'cast_str': self.cast_str,
                                  'drop': self.drop,
                                  'dup': self.dup,
                                  'if': self.condition,
                                  'jmp': self.jmp,
                                  'stack': self.stack,
                                  'swap': self.swap,
                                  'print': self.print,
                                  'println': self.println,
                                  'read': self.read,
                                  'call': self.call,
                                  'return': self.return_,
                                  'exit': self.exit,
                                  'store': self.store,
                                  'load': self.load,
                                  'get_pointer': self.get_pointer
                                  }

    def push(self, value):
        self.data_stack.push(value)

    def pop(self):
        return self.data_stack.pop()

    def mod(self):
        tos = self.pop()
        self.push(self.pop() % tos)

    def mult(self):
        self.push(self.pop() * self.pop())

    def add(self):
        self.push(self.pop() + self.pop())

    def sub(self):
        tos = self.pop()
        self.push(self.pop() - tos)

    def div(self):
        tos = self.pop()
        self.push(self.pop() / tos)

    def eq(self):
        self.push(self.pop() == self.pop())

    def cast_int(self):
        self.push(int(self.pop()))

    def cast_str(self):
        self.push(str(self.pop()))

    def drop(self):
        self.pop()

    def dup(self):
        self.push(self.pop())

    def condition(self):
        true_clause = self.pop()
        false_clause = self.pop()
        if self.pop():
            self.push(true_clause)
        else:
            self.push(false_clause)

    def jmp(self):
        address = self.pop()
        if isinstance(address, int) and 0 <= address < len(self.code):
            self.instruction_pointer = address
        else:
            raise RuntimeError("'jmp' address must be a valid integer.")

    def stack(self):
        print("DS: ", self.data_stack.items)
        print("RS: ", self.return_stack.items)
        print("IP: ", self.instruction_pointer)
        print("heap", self.heap)

    def swap(self):
        tos = self.pop()
        tos_1 = self.pop()
        self.push(tos_1)
        self.push(tos)

    def print(self):
        print(self.pop(), end=' ')

    def println(self):
        print(self.pop())

    def read(self):
        a = input()
        self.push(a)

    def call(self):
        self.return_stack.push(self.instruction_pointer)
        self.jmp()

    def return_(self):
        self.instruction_pointer = self.return_stack.pop()

    def exit(self):
        sys.exit(0)

    def store(self):
        self.heap.update({self.pop(): self.pop()})

    def load(self):
        self.push(self.heap[self.pop()])

    def get_pointer(self):
        self.push(self.instruction_pointer)

    def instruction(self, instr):
        if instr in self.instructions_dict:
            self.instructions_dict[instr]()
        elif isinstance(instr, int) or isinstance(instr, float):
            self.push(instr)
        elif isinstance(instr, str) and len(instr) > 0:
            if instr[0] == instr[-1] == '"':
                self.push(instr[1:-1])

    def run(self):
        while self.instruction_pointer < len(self.code):
            instr = self.code[self.instruction_pointer]
            self.instruction_pointer += 1
            self.instruction(instr)
