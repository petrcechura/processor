from Ram import Ram
from Instruction import *
from ErrorHandler import ErrorHandler
from RegisterSet import *
import cargo
import queue

class Core:

    # external classes
    ram : Ram = None
    reporter : ErrorHandler = None
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


    # Emulate a clock cycle behavior inside core
    # -> get new line of code, fetch instruction and execute it
    def clock(self):
        self.reporter.clock()
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

        self.reporter.progress(line)

        try:
            ins_object = self.instructions[instruction](self.ram, self.register_set)
            ins_object.parse_args(args)
            self.pipeline.put(ins_object)
        except cargo.exceptions.DependencyNotFound:
            self.reporter.error('Instruction {} not in this core'.format(instruction))
        except Exception as e:
            self.reporter.error('Unnusual error happened when trying to execute {} instrution...\nException: {}'.format(instruction, e))
    
    def is_bussy(self):
        return self.core_bussy
    
    # pipeline size
    # 1 = no pipelining used
    # >1 = pipeline in use
    def get_pipeline_size(self):
        return self.pipeline.maxsize


    def __init__(self, core_number : int = 0, pipeline_size : int = 1 ) -> None:
        self.instructions = dict()
        if pipeline_size > 0:
            self.pipeline = queue.Queue(pipeline_size)
        else:
            self.reporter.error('You passed wrong pipeline size! ({})'.format(pipeline_size))
        self.reporter = ErrorHandler('Core {}'.format(core_number))
        self.register_set = RegisterSet()

        self.register_instructions()

    # Builder methods
    def connect_ram(self, ram : Ram):
        if isinstance(ram, Ram):    
            self.ram = ram
        else:
            self.reporter.error('Connected RAM is not type of RAM! Your type: {}'.format(type(ram)))


    # TODO
    def __register_instruction__(self, ins : Instruction):

        # if the core has pipelining, check if the phase_cnt of instruction match the pipeline size
        if self.get_pipeline_size() != 1:
            if ins.phase_cnt == self.get_pipeline_size():
                self.instructions[ins.__name__] = ins
            else:
                self.reporter.error('Unable to register {} instruction! Core\'s pipeline size is {}, instruction phasecnt is {}', 
                                    ins.__name__, self.get_pipeline_size(), ins.phase_cnt)
        
        # the processor has no pipeline... instructions can have different execution time
        # TODO is that correct? Does pipeline always strictly specifies execution time in cycles for every instruction?
        # READ ABOUT IT! 
        else:
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