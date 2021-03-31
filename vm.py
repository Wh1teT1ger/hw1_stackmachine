import sys
from compiler import compiler
from stackMachine import *

if __name__ == "__main__":
    # Machine(compiler('test.txt')).run() # запуск программы из описания
    Machine(compiler('factorial.txt')).run()
