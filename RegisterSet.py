

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

    def __init__(self) -> None:
        self.__stack_pointer__ = 0
        self.__program_counter__ = 0
        self.__instruction_register__ = 0

    def sp_set(self, val : int):
        self.__stack_pointer__ = val

    def sp_get(self):
        return self.__stack_pointer__

    def pp_set(self,val : int):
        self.__program_counter__ = val

    def pp_get(self):
        return self.__program_counter__
    
    def pp_incr(self, val : int = 1):
        self.__program_counter__ = self.pp_get() + 1
    
    def ir_get(self):
        return self.__instruction_register__
    
    def ir_set(self, val : int):
        self.__instruction_register__ = val