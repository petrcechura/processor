from Ram import *
from ErrorHandler import *
from Core import Core
import time


class Processor:

    cores : list = []
    ram : Ram = None

    program : list = []

    error_handler : ErrorHandler = None

    clock_cycle : int


    def __init__(self, cores_cnt : int = 1) -> None:
        self.program_counter = 0
        self.clock_cycle = 0
        self.error_handler = ErrorHandler('Processor')
        for i in range(cores_cnt):
            c = Core(i)
            self.cores.append(c)

    # take the program file, read it and execute it
    # shall be able to properly split instructions among multiple cores
    def load_program(self):

        #TODO how to automatically divide instructions among multiple cores? Probably
        # a complex task... Read about it.
        # Maybe a separate class 'Sheduler' shall be created? (and assign visitor pattern)
        self.program = ["SET *05 5 ",
                        "SUB *05 1 *05",
                        "BRZ *05 4",
                        "JMP 1",
                        "SET *02 1",
                        "SET *07 9" ]
        
        program1 =      ["SET *05 5 ",
                        "SUB *05 1 *05",
                        "BRZ *05 4",
                        "JMP 1",
                        "SET *02 1",
                        "SET *07 9" ]
        
        program2 =      ["SET *07 6",
                         "SET *01 50",
                         "SUB *07 *01 *04",
                         "MOV *06 *05",]

        # give core a code to execute
        self.cores[0].append_code(program1)
        self.cores[1].append_code(program2)
        


    # TODO the program should run until the pp_register does not reach the end of program...
    # but what to do when we got multiple cores, each with its own pp? -- SOLVED
    def exec_program(self):

        # while cores have a code to execute
        while(self.cores_bussy()):

            for c in self.cores:
                c.clock()

            # clock
            self.clock_cycle = self.clock_cycle + 1
            time.sleep(0.5)

    # Check whether the cores are bussy (running instructions) or not
    def cores_bussy(self):
        for c in self.cores:
            if c.is_bussy():
                return True
        return False

    
    # pass a reference to the RAM
    def connect_ram(self, ram : Ram):    
        self.ram = ram
        self.program_counter = self.ram.read(0)

        # connect all cores to the same ram
        for c in self.cores:
            c.connect_ram(self.ram)
