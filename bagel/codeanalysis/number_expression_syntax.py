from .expression_syntax import ExpressionSyntax
from .syntaxkind import SyntaxKind
from .syntaxtoken import SyntaxToken


class NumberExpressionSyntax(ExpressionSyntax):
    def __init__(self, number_token: SyntaxToken):
        self._number_token = number_token

    @property
    def kind(self) -> SyntaxKind:
        return SyntaxKind.NumberExpression

    def get_children(self) -> list:
        return [self.number_token]

    @property
    def number_token(self) -> SyntaxToken:
        return self._number_token
