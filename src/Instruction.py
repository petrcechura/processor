from abc import *
from .ErrorHandler import ErrorHandler
from enum import Enum
from .Ram import Ram
from typing import Protocol

# TODO add virtual memory access

class Instruction(ABC):

    # Register set interface class that shall be passed into an __init__ method for instruction to work
    class RegisterSet(Protocol):
        def pp_get() -> int: pass
        def pp_incr() -> None: pass
        def pp_set() -> None: pass

    __name__ : str

    # references to external classes
    reporter : ErrorHandler
    ram : Ram
    register_set : object

    # given arguments
    args : list

    def __init__(self, ram: Ram, regs : RegisterSet) -> None:
        self.reporter = ErrorHandler('Instruction {}'.format(self.__name__))
        self.connect_ram(ram)
        self.register_set = regs

    def connect_ram(self, ram : Ram):
        if isinstance(ram, Ram):    
            self.ram = ram
        else:
            self.reporter.error('Connected RAM is not type of RAM! Your type: {}'.format(type(ram)))

    # is called inside clock() method
    @abstractmethod
    def __exec__(self) -> None:
        pass

    # called at the end of instruction lifetime
    # NOTE: should be overriden by a instruction that uses the program counter register, otherwise dont touch 
    def __program_counter__(self, val : int = 1) -> None:
        self.register_set.pp_incr()

    # input: string representing either value or address ('*02')
    # output: value
    def __get_value__(self, _in : str) -> int:
        # input is address
        if (_in[0] == '*'):
            _in = _in[1:]
            if _in.isnumeric():
                _in = int(_in)
                return self.ram.read(_in)
            else:
                self.reporter.error('input address is not valid')
        # input is number
        else:
            if _in.isnumeric():
                return int(_in)
            else:
                self.reporter.error('input value is not valid')




    # take a string, extract address from it
    def __get_address__(self, _in : str) -> int:
        if (_in[0] == '*') and _in[1:].isnumeric():
            return int(_in[1:])
        else:
            self.reporter.error('the given string ({}) does not contain address'.format(_in))

    # TODO make this safe against bad syntax
    def parse_args(self, args : list[str]):
        self.args = args
    
    # PUBLIC API method
    def clock(self) -> None:
        self.__exec__()
        self.__program_counter__()

    def get_name(self) -> str:
        return self.__name__
    

class MOV(Instruction):

    addr1 : int
    addr2 : int

    __name__ = 'MOV'

    def __exec__(self):
        self.addr1 = self.__get_address__(self.args[0])
        self.addr2 = self.__get_address__(self.args[1])
        self.ram.write(self.addr1, self.addr2)

class SET(Instruction):

    value : int
    addr : int

    __name__ = 'SET'

    def __exec__(self):
        self.addr = self.__get_address__(self.args[0])
        self.value = self.__get_value__(self.args[1])
        self.ram.write(self.addr, self.value)

class ADD(Instruction):

    val1 : int
    val2 : int
    addr : int

    __name__ = 'ADD'

    def __exec__(self):
        self.val1 = self.__get_value__(self.args[0])
        self.val2 = self.__get_value__(self.args[1])
        self.addr = self.__get_address__(self.args[2])
        self.ram.write(self.addr, self.val1 + self.val2)

class SUB(Instruction):

    val1 : int
    val2 : int
    addr : int

    __name__ = 'SUB'

    def __exec__(self):
        self.val1 = self.__get_value__(self.args[0])
        self.val2 = self.__get_value__(self.args[1])
        self.addr = self.__get_address__(self.args[2])
        self.ram.write(self.addr, self.val1 - self.val2)


class JMP(Instruction):
    
    __name__ = 'JMP'
    
    val : int

    def __program_counter__(self) -> None:
        self.register_set.pp_set(self.val)

    def __exec__(self):
        self.val = self.__get_value__(self.args[0])

# 'BRE 0 0 2'
class BRE(Instruction):

    __name__ = 'BRE'

    val1 : int
    val2 : int
    addr : int


    def __program_counter__(self) -> None:
        self.register_set.pp_set(self.addr)

    def __exec__(self):
        self.val1 = self.__get_value__(self.args[0])
        self.val2 = self.__get_value__(self.args[1])
        
        if self.val1 == self.val2:
            self.addr = self.addr = self.__get_value__(self.args[2])
        else:
            self.addr = self.register_set.pp_get() + 1
# 'BRZ 0 5'
class BRZ(Instruction):

    __name__ = 'BRZ'

    val : int
    addr : int

    def __program_counter__(self) -> None:
        self.register_set.pp_set(self.addr)

    def __exec__(self):
        self.val = self.__get_value__(self.args[0])

        if self.val == 0:
            self.addr = self.addr = self.__get_value__(self.args[1])
        else:
            self.addr = self.register_set.pp_get() + 1

class NOP(Instruction):

    __name__ = 'NOP'

    def __exec__(self):
        pass
