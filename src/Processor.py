from .Ram import Ram 
from .ErrorHandler import ErrorHandler
from .Core import Core
import time
from typing import Protocol
from abc import *


class Processor(ABC):

    # Core objects list
    cores : list = []

    # Ram Object
    ram : Ram = None

    program : list = []

    reporter : ErrorHandler = None

    clock_cycle : int


    # Processor specific method that should be overriden to add more cores, connect RAM and ErrorHandler
    @abstractmethod
    def __setup__(self):
        pass

    def __init__(self) -> None:
        self.clock_cycle = 0
        self.reporter = ErrorHandler('Processor')
        self.__setup__()


    def add_core(self, core : Core) -> None:
        if isinstance(core, Core):
            self.cores.append(core)
        else:
            self.reporter.error('That core cannot be added to a processor')

    # take the program file, read it and execute it
    # shall be able to properly split instructions among multiple cores
    @abstractmethod
    def load_program(self):
        pass
        #TODO how to automatically divide instructions among multiple cores? Probably
        # a complex task... Read about it.
        # Maybe a separate class 'Sheduler' shall be created? (and assign visitor pattern)
        


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
        if isinstance(ram, Ram):    
            self.ram = ram
        else:
            self.reporter.error('Connected RAM is not type of RAM! Your type: {}'.format(type(ram)))

        # connect all cores to the same ram
        for c in self.cores:
            c.connect_ram(self.ram)
