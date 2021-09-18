from colorama import Fore


class ConsoleColor:
    @property
    def Red(self): return Fore.RED

    @property
    def Green(self): return Fore.GREEN

    @property
    def Yellow(self): return Fore.YELLOW

    @property
    def Blue(self): return Fore.BLUE

    @property
    def Magenta(self): return Fore.MAGENTA

    @property
    def Cyan(self): return Fore.CYAN

    @property
    def White(self): return Fore.WHITE

    @property
    def Black(self): return Fore.BLACK

    @property
    def DarkGrey(self): return Fore.LIGHTBLACK_EX

    @property
    def Default(self): return Fore.RESET
