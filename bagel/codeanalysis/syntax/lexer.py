from curses.ascii import isalpha

from .syntaxfacts import SyntaxFacts
from .syntaxkind import SyntaxKind
from .syntaxtoken import SyntaxToken


class Lexer:
    _text: str
    _diagnostics: list

    def __init__(self, text: str):
        self._text = text
        self._position = 0
        self._diagnostics = []

    @property
    def diagnostics(self) -> list:
        return self._diagnostics

    @property
    def current(self) -> str:
        if self._position >= len(self._text):
            return '\0'
        return self._text[self._position]

    @staticmethod
    def isletter(c: str) -> bool:
        return c.isalpha() or c == '_'
        
    def next(self) -> None:
        self._position += 1

    def lex(self) -> SyntaxToken:
        if self._position >= len(self._text):
            return SyntaxToken(SyntaxKind.EOFTOKEN, self._position, '\0', None)

        if self.current.isdigit():
            start = self._position

            while self.current.isdigit():
                self.next()

            length = self._position - start
            text = self._text[start:length + start]
            try:
                value = int(text)
            except ValueError:
                self._diagnostics.append(f"The number {self._text} isn't a valid int.")
            return SyntaxToken(SyntaxKind.NUMBERTOKEN, start, text, value)

        if self.current.isspace():
            start = self._position

            while self.current.isspace():
                self.next()

            length = self._position - start
            text = self._text[start:length + start]
            return SyntaxToken(SyntaxKind.WHITESPACETOKEN, start, text, None)

        if self.isletter(self.current):
            start = self._position

            while self.isletter(self.current):
                self.next()

            length = self._position - start
            text = self._text[start:length + start]
            kind = SyntaxFacts.get_keyword_kind(text)
            return SyntaxToken(kind, start, text, None)
        

        match self.current:
            case '+':
                self._position += 1
                return SyntaxToken(SyntaxKind.PLUSTOKEN, self._position, '+', None)
            case '-':
                self._position += 1
                return SyntaxToken(SyntaxKind.MINUSTOKEN, self._position, '-', None)
            case '*':
                self._position += 1
                return SyntaxToken(SyntaxKind.STARTOKEN, self._position, '*', None)
            case '/':
                self._position += 1
                return SyntaxToken(SyntaxKind.SLASHTOKEN, self._position, '/', None)
            case '(':
                self._position += 1
                return SyntaxToken(SyntaxKind.OPENPARENTOKEN, self._position, '(', None)
            case ')':
                self._position += 1
                return SyntaxToken(SyntaxKind.CLOSEPARENTOKEN, self._position, ')', None)

        self._diagnostics.append(f"ERROR: bad character input: '{self.current}'")
        self._position += 1
        return SyntaxToken(
            SyntaxKind.BADTOKEN, self._position, self._text[self._position - 1:1], None)
