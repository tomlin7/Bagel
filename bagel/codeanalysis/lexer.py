from .syntaxkind import SyntaxKind
from .syntaxtoken import SyntaxToken


class Lexer:
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

    def next(self) -> None:
        self._position += 1

    def next_token(self) -> SyntaxToken:
        if self._position >= len(self._text):
            return SyntaxToken(SyntaxKind.EndOfFileToken, self._position, '\0', None)

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
            return SyntaxToken(SyntaxKind.NumberToken, start, text, value)

        if self.current.isspace():
            start = self._position

            while self.current.isspace():
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

        self._diagnostics.append(f"ERROR: bad character input: '{self.current}'")
        self._position += 1
        return SyntaxToken(SyntaxKind.BadToken, self._position, self._text[self._position - 1:1], None)