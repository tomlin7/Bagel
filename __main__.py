import enum

import colorama
from colorama import Fore

colorama.init(autoreset=True)

class SyntaxKind(enum.Enum):
    NumberToken = 1
    WhiteSpaceToken = 2
    PlusToken = 3
    MinusToken = 4
    StarToken = 5
    SlashToken = 6
    OpenParenthesisToken = 7
    CloseParenthesisToken = 8
    BadToken = 9
    EndOfFileToken = 10


class SyntaxToken:
    kind: SyntaxKind
    position: int
    text: str
    value: any

    def __init__(self, kind, position, text, value):
        self.kind = kind
        self.position = position
        self.text = text
        self.value = value



class Lexer:
    def __init__(self, text):
        self._text = text
        self._position = 0
    
    @property
    def current(self):
        if self._position >= len(self._text):
            return '\0'
        return self._text[self._position]

    def next(self):
        self._position += 1

    def next_token(self):
        # <numbers>
        # + - * /
        # <whitespace>

        if self._position >= len(self._text):
            return SyntaxToken(SyntaxKind.EndOfFileToken, self._position, '\0', None)

        if self.current.isdigit():
            start = self._position

            while (self.current.isdigit()):
                self.next()
            
            length = self._position - start
            text = self._text[start:length + start]
            try:
                value = int(text)
            except ValueError:
                print("ERROR: Invalid number!")
            return SyntaxToken(SyntaxKind.NumberToken, start, text, value)

        if self.current.isspace():
            start = self._position

            while (self.current.isspace()):
                self.next()
            
            length = self._position - start
            text = self._text[start:length + start]
            return SyntaxToken(SyntaxKind.WhiteSpaceToken, start, text, None)

        if self.current == '+':
            self._position += 1
            return SyntaxToken(SyntaxKind.PlusToken, self._position, '+', None)
        elif self.current == '-':
            self._position += 1
            return SyntaxToken(SyntaxKind.MinusToken, self._position, '-', None)
        elif self.current == '*':
            self._position += 1
            return SyntaxToken(SyntaxKind.StarToken, self._position, '*', None)
        elif self.current == '/':
            self._position += 1
            return SyntaxToken(SyntaxKind.SlashToken, self._position, '/', None)
        elif self.current == '(':
            self._position += 1
            return SyntaxToken(SyntaxKind.OpenParenthesisToken, self._position, '(', None)
        elif self.current == ')':
            self._position += 1
            return SyntaxToken(SyntaxKind.CloseParenthesisToken, self._position, ')', None)

        self._position += 1
        return SyntaxToken(SyntaxKind.BadToken, self._position, self._text[self._position - 1:1], None)

class Colors:
    @staticmethod
    def get_color(kind):
        if kind in [SyntaxKind.PlusToken, SyntaxKind.MinusToken, SyntaxKind.StarToken, SyntaxKind.SlashToken]:
            return Fore.GREEN
        elif kind in [SyntaxKind.NumberToken]:
            return Fore.YELLOW
        elif kind in [SyntaxKind.OpenParenthesisToken, SyntaxKind.CloseParenthesisToken]:
            return Fore.BLUE
        elif kind in [SyntaxKind.WhiteSpaceToken, SyntaxKind.EndOfFileToken]:
            return Fore.LIGHTBLACK_EX
        else:
            return Fore.RED

while True:
    line = input("> ")

    if line is None or line == "":
        break

    lexer = Lexer(line)
    while True:
        token = lexer.next_token()
        if token.kind == SyntaxKind.EndOfFileToken:
            break
            
        print(Colors.get_color(token.kind) + f"{token.kind}: '{token.text}' {token.value if token.value is not None else ''}")