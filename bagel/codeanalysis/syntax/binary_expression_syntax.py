from .expression_syntax import ExpressionSyntax
from .syntaxkind import SyntaxKind
from .syntaxtoken import SyntaxToken


class BinaryExpressionSyntax(ExpressionSyntax):
    def __init__(self, left: ExpressionSyntax, operator_token: SyntaxToken, right: ExpressionSyntax):
        self._left = left
        self._operator_token = operator_token
        self._right = right

    @property
    def kind(self) -> SyntaxKind:
        return SyntaxKind.BinaryExpression

    def get_children(self) -> list:
        # can be an array too
        return [self.left, self.operator_token, self.right]

    @property
    def left(self) -> ExpressionSyntax:
        return self._left

    @property
    def operator_token(self) -> SyntaxToken:
        return self._operator_token

    @property
    def right(self) -> ExpressionSyntax:
        return self._right
