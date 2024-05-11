from abc import *
from ErrorHandler import ErrorHandler
from RegisterSet import *
from enum import Enum
from Ram import Ram

class Instruction(ABC):

    __name__ : str

    # references to external classes
    reporter : ErrorHandler
    ram : Ram
    register_set : RegisterSet

    # given arguments
    args : list

    # phases
    class phase_t(Enum):
        FETCH = 0
        DECODE = 1
        EXECUTE = 2
    
    phase : phase_t = phase_t.FETCH

    def __init__(self, ram: Ram, regs : RegisterSet) -> None:
        self.reporter = ErrorHandler('Instruction {}'.format(self.__name__))
        self.connect_ram(ram)
        self.coonect_register_set(regs)

    def connect_ram(self, ram : Ram):
        if isinstance(ram, Ram):    
            self.ram = ram
        else:
            self.reporter.error('Connected RAM is not type of RAM! Your type: {}'.format(type(ram)))

    def coonect_register_set(self, regs : RegisterSet):
        if isinstance(regs, RegisterSet):    
            self.register_set = regs
        else:
            self.reporter.error('Connected register_set is not type of RegisterSet! Your type: {}'.format(type(regs)))

    def copy(self):
        return self

    @abstractmethod
    def __exec__(self) -> None:
        match self.phase:
            case self.phase_t.FETCH:
                pass
            case self.phase_t.DECODE:
                pass
            case self.phase_t.EXECUTE:
                pass

    # called at the end of instruction lifetime
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
    def parse_args(self, args : str):
        self.args = args.split(sep=' ')

    def get_phase_cnt(self):
        return len(self.phase_t)
    
    def get_curr_phase(self):
        return self.phase.value
    
    # PUBLIC API method
    def start(self) -> None:
        self.__exec__()
        if self.phase == self.phase_t.EXECUTE:
            self.__program_counter__()
        else:
            self.phase = self.phase_t(self.phase.value + 1)

class MOV(Instruction):

    addr1 : int
    addr2 : int

    __name__ = 'MOV'

    def __exec__(self):
        match self.phase:
            case self.phase_t.FETCH:
                pass
            case self.phase_t.DECODE:
                self.addr1 = self.__get_address__(self.args[0])
                self.addr2 = self.__get_address__(self.args[1])
            case self.phase_t.EXECUTE:
                self.ram.write(self.addr1, self.addr2)

class SET(Instruction):

    value : int
    addr : int

    __name__ = 'SET'

    def __exec__(self):
        match self.phase:
            case self.phase_t.FETCH:
                pass
            case self.phase_t.DECODE:
                self.addr = self.__get_address__(self.args[0])
                self.value = self.__get_value__(self.args[1])
            case self.phase_t.EXECUTE:
                self.ram.write(self.addr, self.value)

class ADD(Instruction):

    val1 : int
    val2 : int
    addr : int

    __name__ = 'ADD'

    def __exec__(self):
        match self.phase:
            case self.phase_t.FETCH:
                pass
            case self.phase_t.DECODE:
                self.val1 = self.__get_value__(self.args[0])
                self.val2 = self.__get_value__(self.args[1])
                self.addr = self.__get_address__(self.args[2])
            case self.phase_t.EXECUTE:
                self.ram.write(self.addr, self.val1 + self.val2)

class SUB(Instruction):

    val1 : int
    val2 : int
    addr : int

    __name__ = 'SUB'

    def __decode__(self):
        self.val1 = self.__get_value__(self.args[0])
        self.val2 = self.__get_value__(self.args[1])
        self.addr = self.__get_address__(self.args[2])
        
    def __execute__(self):
        self.ram.write(self.addr, self.val1 - self.val2)

    def __exec__(self):
        match self.phase:
            case self.phase_t.FETCH:
                pass
            case self.phase_t.DECODE:
                self.val1 = self.__get_value__(self.args[0])
                self.val2 = self.__get_value__(self.args[1])
                self.addr = self.__get_address__(self.args[2])
            case self.phase_t.EXECUTE:
                self.ram.write(self.addr, self.val1 - self.val2)


class JMP(Instruction):
    
    __name__ = 'JMP'
    
    val : int

    def __program_counter__(self) -> None:
        self.register_set.pp_set(self.val)

    def __exec__(self):
        match self.phase:
            case self.phase_t.FETCH:
                pass
            case self.phase_t.DECODE:
                self.val = self.__get_value__(self.args[0])
            case self.phase_t.EXECUTE:
                pass

# 'BRE 0 0 2'
class BRE(Instruction):

    __name__ = 'BRE'

    val1 : int
    val2 : int
    addr : int


    def __program_counter__(self) -> None:
        self.register_set.pp_set(self.addr)

    def __exec__(self):
        match self.phase:
            case self.phase_t.FETCH:
                pass
            case self.phase_t.DECODE:
                self.val1 = self.__get_value__(self.args[0])
                self.val2 = self.__get_value__(self.args[1])
            case self.phase_t.EXECUTE:
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
        match self.phase:
            case self.phase_t.FETCH:
                pass
            case self.phase_t.DECODE:
                self.val = self.__get_value__(self.args[0])
            case self.phase_t.EXECUTE:
                if self.val == 0:
                    self.addr = self.addr = self.__get_value__(self.args[1])
                else:
                    self.addr = self.register_set.pp_get() + 1

class NOP(Instruction):

    __name__ = 'NOP'

    def __exec__(self):
        match self.phase:
            case self.phase_t.FETCH:
                pass
            case self.phase_t.DECODE:
                pass
            case self.phase_t.EXECUTE:
                pass
