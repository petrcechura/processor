from enum import *

#TODO
# make the ErrorHandler somehow common to all classes inside one processor
# ... maybe singleton? Or Factory?
class ErrorHandler:

    prefix : str

    progress_print : bool = False
    warnings_print : bool = True
    errors_print : bool = True

    clock_cycle : int = 0

    class Severity(Enum):
        INFO = 0,
        WARNING = 1,
        ERROR = 2

    def clock(self):
        self.clock_cycle = self.clock_cycle + 1

    def __init__(self, prefix : str) -> None:
        self.prefix = prefix
        self.setProgressPrintingOn(1)
        self.setWarningPrintingOn(1)
        self.setErrorPrintingOn(1)

        self.clock_cycle = 0

    def progress(self, s : str = 'undefined progress'):
        if self.progress_print:
            print("CLK({}) P: {}: {}".format(self.clock_cycle, self.prefix, s))

    def warning(self, s : str = 'undefined warning'):
        if self.warnings_print:
            print("CLK({}) WARNING: {}: {}".format(self.clock_cycle, self.prefix, s))

    def error(self, s : str = 'undefined error'):
        if self.errors_print:
            print("CLK({}) ERROR: {}: {}".format(self.clock_cycle, self.prefix, s))
        exit()

    def setProgressPrintingOn(self, on = 1):
        self.progress_print = on

    def setWarningPrintingOn(self, on = 1):
        self.warnings_print = on

    def setErrorPrintingOn(self, on = 1):
        self.errors_print = on