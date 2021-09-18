from CodeAnalysis.syntaxkind import SyntaxKind
from CodeAnalysis.syntaxnode import SyntaxNode


class SyntaxToken(SyntaxNode):
    def __init__(self, kind: SyntaxKind, position: int, text: str, value: object):
        self._kind = kind
        self._position = position
        self._text = text
        self._value = value

    @property
    def kind(self) -> SyntaxKind:
        return self._kind

    def get_children(self) -> list:
        return []

    @property
    def position(self) -> int:
        return self._position

    @property
    def text(self) -> str:
        return self._text

    @property
    def value(self) -> object:
        return self._value
