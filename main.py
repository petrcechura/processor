# TODO
# solve the factory method problem
#   - instructions shall be registered in core and then initialized (and destroyed) when needed
#   - use cargo or something else
# not sure if ram references will propagate properly inside the code (if there will be only one ram)
# 


from Processor import Processor
from Core import *
from Ram import *
from ErrorHandler import *

proc = Processor()
ram = Ram(10)

proc.connect_ram(ram)
proc.load_program()
proc.exec_program()

ram.print()

