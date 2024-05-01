

class RegisterSet:


    __stack_pointer__ : int
    __program_pointer__ : int

    def __init__(self) -> None:
        self.__stack_pointer__ = 0
        self.__program_pointer__ = 0

    def sp_set(self, val : int):
        self.__stack_pointer__ = val

    def sp_get(self):
        return self.__stack_pointer__

    def pp_set(self,val : int):
        self.__program_pointer__ = val

    def pp_get(self):
        return self.__program_pointer__
    
    def pp_incr(self, val : int = 1):
        a = self.pp_get() + 1
        self.__program_pointer__ = a