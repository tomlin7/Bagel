from .expression_syntax import ExpressionSyntax
from .syntaxtoken import SyntaxToken


class SyntaxTree:
    def __init__(self, diagnostics: list, root: ExpressionSyntax, end_of_file_token: SyntaxToken):
        self._diagnostics = diagnostics
        self._root = root
        self._end_of_file_token = end_of_file_token

    @property
    def diagnostics(self) -> list:
        return self._diagnostics

    @property
    def root(self) -> ExpressionSyntax:
        return self._root

    @property
    def end_of_file_token(self) -> SyntaxToken:
        return self._end_of_file_token

    @staticmethod
    def parse(text: str) -> object:
        from .parser import Parser
        parser = Parser(text)
        return parser.parse()
