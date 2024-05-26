from src import Core
from src import Processor
from src import Ram
from src import Instruction
from src import ErrorHandler

class SimpleCore(Core.Core):

    # Emulate a clock cycle behavior inside core
    # -> get new line of code, fetch instruction and execute it
    def clock(self) -> None:
        self.reporter.clock()

        if self.register_set.pp_get() < len(self.code):
            # get a line list of parsed instruction and its args
            line : list = self.code[self.register_set.pp_get()]

            print(line)

            instruction = self.get_instruction_object(line)

            instruction.clock()
        
        else:
            self.core_bussy = False
    
    # method that is called in __init__, shall be overriden
    def setup(self) -> None:
        self.register_set = self.RegisterSet()

    def register_instructions(self):
        self.__register_instruction__(Instruction.MOV)
        self.__register_instruction__(Instruction.SET)
        self.__register_instruction__(Instruction.ADD)
        self.__register_instruction__(Instruction.SUB)
        self.__register_instruction__(Instruction.JMP)
        self.__register_instruction__(Instruction.BRE)
        self.__register_instruction__(Instruction.BRZ)




class SingleCoreProcessor(Processor.Processor):
    def __setup__(self):
        self.reporter = ErrorHandler.ErrorHandler('Processor')

        for i in range(1):
            c = SimpleCore(i)
            self.add_core(c)

        self.connect_ram(Ram.Ram(50))


    def load_program(self):
        #TODO how to automatically distribute instructions among multiple cores? Probably
        # a complex task... Read about it.
        # Maybe a separate class 'Sheduler' shall be created? (and assign visitor pattern)
        self.program = ["SET *05 5 ",
                        "SUB *05 1 *05",
                        "BRZ *05 4",
                        "JMP 1",
                        "SET *02 1",
                        "SET *07 9" ]

        # give core a code to execute
        self.cores[0].append_code(self.program)
