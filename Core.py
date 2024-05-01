from Ram import Ram
from Instruction import *
from ErrorHandler import ErrorHandler
import cargo
import queue

class Core:

    ram : Ram = None
    error_handler : ErrorHandler = None
    proc : object

    instructions : dict

    pipeline : queue.Queue = None

    def clock(self):
        ins = self.pipeline.get()
        ins.start()

    # take a line of code and execute it
    def exec_line(self, line : str):

        instruction, args = line.split(' ', 1)

        print(instruction)

        try:
            ins_object = self.instructions[instruction](self.ram)
            ins_object.parse_args(args)
            self.pipeline.put(ins_object)
        except cargo.exceptions.DependencyNotFound:
            self.error_handler.handle('Instruction {} not in this core'.format(instruction))
        except Exception as e:
            self.error_handler.handle('Unnusual error happened when trying to execute {} instrution...\nException: {}'.format(instruction, e))

        self.clock()


    # 0 = pipeline empty
    # 1 = pipeline not empty
    # 2 = pipeline full
    def get_core_status(self):
        if (self.pipeline.empty()):
            return 0
        elif (self.pipeline.full()):
            return 2
        else:
            return 1


    def __init__(self,  pipeline_size : int = 1 ) -> None:
        self.instructions = dict()
        self.pipeline = queue.Queue(pipeline_size)
        self.error_handler = ErrorHandler('Core')

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