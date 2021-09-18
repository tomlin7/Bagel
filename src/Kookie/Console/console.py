from Console.consolecolor import ConsoleColor


class Console:
    def __init__(self):
        self.foreground_color = ConsoleColor().Default
    
    def write(self, *args):
        print(self.foreground_color + ''.join(args))

    def reset(self):
        self.foreground_color = ConsoleColor().Default
