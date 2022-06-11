from .expression_syntax import ExpressionSyntax
from .syntaxkind import SyntaxKind
from .syntaxtoken import SyntaxToken


class ParenthesizedExpressionSyntax(ExpressionSyntax):
    def __init__(self, open_parenthesis_token: SyntaxToken, expression: ExpressionSyntax,
                 close_parenthesis_token: SyntaxToken):
        self._open_parenthesis_token = open_parenthesis_token
        self._expression = expression
        self._close_parenthesis_token = close_parenthesis_token

    @property
    def kind(self) -> SyntaxKind:
        return SyntaxKind.ParenthesizedExpression

    def get_children(self) -> list:
        return [self.open_parenthesis_token, self.expression, self.close_parenthesis_token]

    @property
    def open_parenthesis_token(self) -> SyntaxToken:
        return self._open_parenthesis_token

    @property
    def expression(self) -> ExpressionSyntax:
        return self._expression

    @property
    def close_parenthesis_token(self) -> SyntaxToken:
        return self._close_parenthesis_token
