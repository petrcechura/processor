

#TODO
class ErrorHandler:

    prefix : str

    def __init__(self, prefix : str) -> None:
        self.prefix = prefix

    # 0 = note
    # 1 = warning
    # 2 = error
    def handle(self, s : str = 'undefined error', severity : int = 0):
        print("{}: {}".format(self.prefix, s))