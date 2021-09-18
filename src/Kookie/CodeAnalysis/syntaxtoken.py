from CodeAnalysis.syntaxnode import SyntaxNode


class SyntaxToken(SyntaxNode):
    def __init__(self, kind, position, text, value):
        self._kind = kind
        self._position = position
        self._text = text
        self._value = value

    @property
    def kind(self):
        return self._kind

    def get_children(self):
        return []

    @property
    def position(self):
        return self._position

    @property
    def text(self):
        return self._text

    @property
    def value(self):
        return self._value
