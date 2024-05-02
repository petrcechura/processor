# TODO
# solve the factory method problem
#   - instructions shall be registered in core and then initialized (and destroyed) when needed - SOLVED
# not sure if ram references will propagate properly inside the code (if there will be only one ram) - SOLVED
# try to extend it to a multi-core processor
#   - there probably will be a problem with multi access to a ram and registers
# try to move the program inside ram memory
#   - should be represented by a characters
#   - maybe all ram shall be able to store bytes, thus characters?


from Processor import Processor
from Core import *
from Ram import *
from ErrorHandler import *

proc = Processor(cores_cnt=2)
ram = Ram(10)

proc.connect_ram(ram)
proc.load_program()
proc.exec_program()

ram.print()

