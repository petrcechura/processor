from Ram import *
from ErrorHandler import *
from Core import Core
import time


class Processor:

    cores : list = []
    ram : Ram = None
    

    # inner registers
    _program_pointer_ : int

    # --- REGISTERS API --- # TODO
    def get_pp(self) -> int:
        return self._program_pointer_
    
    def set_pp(self, val : int) -> None:
        self._program_pointer_ = val

    def incr_pp(self) -> None:
        self._program_pointer_ = self.get_pp() + 1

    program : list = []

    error_handler : ErrorHandler = None

    # the program counter is at ram address 0x00
    program_counter : int = 0

    clock_cycle : int


    def __init__(self, cores_cnt : int = 1) -> None:
        self.program_counter = 0
        self.clock_cycle = 0
        self.error_handler = ErrorHandler('Processor')
        for i in range(cores_cnt):
            self.cores.append(Core())

    # take the program file, read it and execute it
    def load_program(self):
        #TODO
        self.program = ["SET *05 5 ",
                        "SUB *05 1 *05",
                        "BRZ *05 4",
                        "JMP 1",
                        "SET *02 1" ]

    def exec_program(self):
        while(self.program_counter < len(self.program)-1):
            # read the current program counter value 
            self.program_counter = self.ram.read(0)

            # get the instruction
            instruction = self.program[self.program_counter]
            
            # try to exec instruction (if core is ready)
            self.exec_line(instruction)

            # clock
            self.clock_cycle = self.clock_cycle + 1
            time.sleep(0.5)

    # dummy approach - find out something about that
    def exec_line(self, line : str) -> bool:
        if self.cores[0].get_core_status() == 0:
            self.cores[0].exec_line(line)
            return True
        else:
            print('NOP added')
            return False

    # builder method - add core to the processor
    def add_core(self, core):
        core.connect_ram(self.ram)
        self.cores.append(core)

    
    # pass a reference to the RAM
    def connect_ram(self, ram : Ram):    
        self.ram = ram
        self.program_counter = self.ram.read(0)

        for c in self.cores:
            c.connect_ram(self.ram)
