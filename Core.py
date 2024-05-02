from Ram import Ram
from Instruction import *
from ErrorHandler import ErrorHandler
from RegisterSet import *
import cargo
import queue

class Core:

    # external classes
    ram : Ram = None
    error_handler : ErrorHandler = None
    register_set : RegisterSet


    # true = Core has a code to execute
    # false = Core is out of code to execute
    core_bussy : bool = False

    # code to execute
    code : list

    # avaiable instrucions in a core
    instructions : dict

    # TODO for pipelining
    pipeline : queue.Queue = None

    def clock(self):
        self.error_handler.clock()
        if self.is_bussy() == True:
            line = self.code[self.register_set.pp_get()]
            self.exec_line(line)
            ins = self.pipeline.get()
            ins.start()

        if (self.register_set.pp_get() == len(self.code)):
            self.core_bussy = False

    # get a code to execute line by line
    def append_code(self, code : list):
        self.code = code
        self.register_set.pp_set(0)
        self.core_bussy = True

    # take a line of code, extract instruction and its args, and pass it to a pipeline -> then execute it
    def exec_line(self, line : str):

        instruction, args = line.split(' ', 1)

        self.error_handler.progress(line)

        try:
            ins_object = self.instructions[instruction](self.ram, self.register_set)
            ins_object.parse_args(args)
            self.pipeline.put(ins_object)
        except cargo.exceptions.DependencyNotFound:
            self.error_handler.error('Instruction {} not in this core'.format(instruction))
        except Exception as e:
            self.error_handler.error('Unnusual error happened when trying to execute {} instrution...\nException: {}'.format(instruction, e))
    
    def is_bussy(self):
        return self.core_bussy


    def __init__(self, core_number : int = 0, pipeline_size : int = 1 ) -> None:
        self.instructions = dict()
        self.pipeline = queue.Queue(pipeline_size)
        self.error_handler = ErrorHandler('Core {}'.format(core_number))
        self.register_set = RegisterSet()

        self.register_instructions()

    # Builder methods
    def connect_ram(self, ram : Ram):
        self.ram = ram


    # TODO
    def __register_instruction__(self, ins : Instruction):
        self.instructions[ins.__name__] = ins

    # TODO
    def register_instructions(self):
        self.__register_instruction__(MOV)
        self.__register_instruction__(SET)
        self.__register_instruction__(ADD)
        self.__register_instruction__(SUB)
        self.__register_instruction__(JMP)
        self.__register_instruction__(BRZ)
        self.__register_instruction__(BRE)