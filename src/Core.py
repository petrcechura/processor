from .Ram import Ram
from .Instruction import Instruction
from .ErrorHandler import ErrorHandler
import re as re
from abc import *

class Core(ABC):

    # 'forward definition' of a RegisterSet
    class RegisterSet:
        pass

    # external classes
    ram : Ram = None
    reporter : ErrorHandler = None
    register_set : RegisterSet = None

    # true = Core has a code to execute
    # false = Core is out of code to execute
    core_bussy : bool = False

    # code to execute
    code : list = None

    # available instrucions in a core
    instructions : dict


    # Emulate a clock cycle behavior inside core
    # -> get new line of code, fetch instruction and execute it
    @abstractmethod
    def clock(self) -> None:
        pass
    
    # method that is called in __init__, shall be overriden
    @abstractmethod
    def setup(self) -> None:
        self.register_set = self.RegisterSet()

    # should be overriden to manually register instructions inside cores
    @abstractmethod
    def register_instructions(self):
        pass

    # get a code to execute line by line
    def append_code(self, code : list) -> None:
        self.code = code
        self.register_set.pp_set(0)
        self.core_bussy = True

    # get a line of code, check whether it's valid, then return a parsed string list [INSTRUCTION, ARG1, ARG2, ...]
    def __parse_line__(self, line : str) -> list[str]:
        if not isinstance(line, str):
            self.reporter.error('given line \'' + '\' is not type of str')

        parse_str = line.split(' ')

        for i, s in enumerate(parse_str):
            # check instruction
            if i==0:
                if not s in self.instructions.keys():
                    self.reporter.error('Instruction {} not present in this core (line: \'{}\')'.format(s, line))
            # check argument
            else:
                if not re.search('\*?\d+', s) and s!='':
                    self.reporter.error('Argument {} not valid (line: \'{}\')'.format(s, line))

        return parse_str
    
    # pass a line of code, return initialized Instruction object with parsed args 
    def get_instruction_object(self, line) -> Instruction:
        line_list : list = self.__parse_line__(line)
        instruction = self.instructions[line_list[0]](self.ram, self.register_set)
        instruction.parse_args(line_list[1:])
        return instruction
    
    def is_bussy(self):
        return self.core_bussy


    def __init__(self, core_number : int = 0) -> None:
        self.reporter = ErrorHandler('Core {}'.format(core_number))

        self.setup()

        self.instructions = dict()
        self.register_instructions()

    # Builder methods
    def connect_ram(self, ram : Ram):
        if isinstance(ram, Ram):    
            self.ram = ram
        else:
            self.reporter.error('Connected RAM is not type of RAM! Your type: {}'.format(type(ram)))


    # Register instruction inside a core
    def __register_instruction__(self, ins : Instruction):
        if not issubclass(ins, Instruction):
            self.reporter.error(str(ins) + ' is not an Instruction class instance')
        
        # the processor has no pipeline... instructions can have different execution time
        # TODO is that correct? Does pipeline always strictly specifies execution time in cycles for every instruction?
        # READ ABOUT IT! 
        self.instructions[ins.__name__] = ins

    class RegisterSet:

        # control registers
        __stack_pointer__ : int
        __program_counter__ : int
        __instruction_register__ : int

        # inner registers
        # TODO not in use yet
        __R1__ : int
        __R2__ : int
        __R3__ : int
        __R4__ : int
        __overflow__ : bool
        __underflow__ : bool
        __divbyzero__ : bool

        def __init__(self) -> None:
            self.__stack_pointer__ = 0
            self.__program_counter__ = 0
            self.__instruction_register__ = 0

        def sp_set(self, val : int) -> None:
            self.__stack_pointer__ = val

        def sp_get(self) -> int:
            return self.__stack_pointer__

        def pp_set(self,val : int) -> None:
            self.__program_counter__ = val

        def pp_get(self) -> int:
            return self.__program_counter__

        def pp_incr(self, val : int = 1) -> None:
            self.__program_counter__ = self.pp_get() + 1

        def ir_get(self) -> int:
            return self.__instruction_register__
    
        def ir_set(self, val : int) -> None:
            self.__instruction_register__ = val



