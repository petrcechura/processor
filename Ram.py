from ErrorHandler import ErrorHandler


class Ram:
    
    data : list

    error_handler : ErrorHandler

    RAM_SIZE : int

    def __init__(self, ram_size : int = 100) -> None:
        self.error_handler = ErrorHandler('Ram')
        self.RAM_SIZE = ram_size

        self.init()
        

    #### API ####    
    def read(self, addr : int) -> int:
        if addr >= 0 and addr < self.RAM_SIZE:
            return self.data[addr]
        else:
            self.error_handler.handle('read address out of range ({})'.format(addr))

    def write(self, addr : int, value : int) -> None:
        if addr >= 0 and addr < self.RAM_SIZE:
            self.data[addr] = value
        else:
            self.error_handler.handle('write address out of range ({})'.format(addr))

    def clear(self):
        self.data = None
        self.init()

    def init(self):
        self.data = list()
        for i in range(self.RAM_SIZE):
            self.data.append(0)

    def print(self):
        #TODO
        print(self.data)
