from Ram import Ram
from Instruction import *
from ErrorHandler import ErrorHandler
from RegisterSet import *
from collections import deque

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

    # available instrucions in a core
    instructions : dict

    # pipelining
    pipeline : deque
    pipeline_size : int = 3


    # Emulate a clock cycle behavior inside core
    # -> get new line of code, fetch instruction and execute it
    def clock(self):
        self.reporter.clock()

        if self.is_bussy() == True:
            if self.register_set.pp_get() < len(self.code):
                line = self.code[self.register_set.pp_get()]
            else:
                line = None
            self.exec_pipeline() # executes all instructions from the pipeline
            self.pipeline[-1] = None  # removes last instruction from pipeline
            self.exec_line(line) # add instruction to the queue

        # if the pipeline is empty, the core is no longer busy
        if (self.pipeline.count(None) == self.get_pipeline_size()):
            
            self.core_bussy = False

    def exec_pipeline(self):
        # run every instruction in pipeline
        for i in range(self.get_pipeline_size()):
            if isinstance(self.pipeline[i], Instruction):
                self.pipeline[i].start()
            else:
                # if in the EXECUTE phase isnt any instruction, just increment the program counter
                if i == self.get_pipeline_size()-1:
                    self.register_set.pp_incr()
                else:
                    # TODO error
                    pass

    # get a code to execute line by line
    def append_code(self, code : list):
        self.code = code
        self.register_set.pp_set(0)
        self.core_bussy = True

    # take a line of code, extract instruction and its args, and pass it to a pipeline
    def exec_line(self, line : str):
        if line == None:
            self.pipeline.appendleft(None)
            return
        
        instruction, args = line.split(' ', 1)

        self.reporter.progress(line)

        try:
            ins_object = self.instructions[instruction](self.ram, self.register_set)
            ins_object.parse_args(args)
            self.pipeline.appendleft(ins_object)
        except KeyError:
            self.reporter.error('Instruction {} not in this core'.format(instruction))
        except Exception as e:
            self.reporter.error('Unnusual error happened when trying to execute {} instrution...\nException: {}'.format(instruction, e))
    
    def is_bussy(self):
        return self.core_bussy
    
    # pipeline size
    # 1 = no pipelining used
    # >1 = pipeline in use
    def get_pipeline_size(self):
        return self.pipeline_size


    def __init__(self, core_number : int = 0) -> None:
        self.instructions = dict()
        if self.pipeline_size > 0:
            self.pipeline = deque(maxlen=self.pipeline_size)
        else:
            self.reporter.error('You passed wrong pipeline size! ({})'.format(self.pipeline_size))
        self.reporter = ErrorHandler('Core {}'.format(core_number))
        self.register_set = RegisterSet()

        self.register_instructions()

        # fill the pipeline with NOP instructions at the init
        for i in range(self.get_pipeline_size()):
            self.pipeline.append(None)

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
            if len(ins.phase_t) == self.get_pipeline_size():
                self.instructions[ins.__name__] = ins
            else:
                self.reporter.error('Unable to register {} instruction! Core\'s pipeline size is {}, instruction phasecnt is {}'.format( 
                                    ins.__name__, self.get_pipeline_size(), len(ins.phase_t)))
        
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
        self.__register_instruction__(NOP)



