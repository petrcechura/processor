# TODO
# solve the factory method problem
#   - instructions shall be registered in core and then initialized (and destroyed) when needed - SOLVED
# not sure if ram references will propagate properly inside the code (if there will be only one ram) - SOLVED
# try to extend it to a multi-core processor
#   - there probably will be a problem with multi access to a ram and registers
# try to move the program inside ram memory
#   - should be represented by a characters
#   - maybe all ram shall be able to store bytes, thus characters?

# TODO continue with pipelining implementation
#   - processor can define its pipeline size; when it's 1, no pipelining, >1 means pipelining
#   - each instruction shall have choosable phase_cnt parameter that defines duration in clock cycles,
#   - in no pipelining, it's just about how long the instruction takes to execute
#       - IS THAT CORRECT?
#   - with pipelining, it should match the pipelining size and then being executed in parallel with previous instruction
#   - in both cases, there must be a mechanism for processor to manage the instructions in pipeline
#       - ...maybe if it will be sure that instructions will be of size of pipeline, it's just about counting cycles
#       - inside an instructiona and doing certain actions depending on phase...
#       - ...or cycles dont have to be counted and the current cycle will be passed into a instruction as argument (somehow)
#           - but thats maybe not suitable since for every instruction there will be different phases
#   - ALSO: program counter is now incremented inside instruction... but what if there will be 5 of them simultaenously?
#       - the program counter management shall be processed in strict phase in every instruction

# TODO The pipeline queue approach maybe isnt the best one... maybe just solve it with list of ref pointers, dunno


# TODO pipeline is now working, queue approach was used... but the code isnt as elegant as it could be. Add some dependency removals, but make sure only right
# instructions shall be added to the core with pipeline
#  -> pipeline size shall NOT be choosed in init function, doesnt make sense...
#  -> pipeline size is heavily bounded to a certain processor, so pipeline size shall be choosed when inheriting a Processor class

# TODO Make the processor class ABC so the concrete processor implementations would be properly created from abstract classes (like uvm)
from examples.SingleCoreProcessor import *

proc = SingleCoreProcessor()

proc.load_program()
proc.exec_program()
