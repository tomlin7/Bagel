from .expression_syntax import ExpressionSyntax
from .syntaxkind import SyntaxKind
from .syntaxtoken import SyntaxToken


class UnaryExpressionSyntax(ExpressionSyntax):
    def __init__(self, operator_token: SyntaxToken, operand: ExpressionSyntax):
        self._operator_token = operator_token
        self._operand = operand

    @property
    def kind(self) -> SyntaxKind:
        return SyntaxKind.UNARYEXPRESSION

    def get_children(self) -> list:
        # can be an array too
        return [self.operator_token, self.operand]

    @property
    def operator_token(self) -> SyntaxToken:
        return self._operator_token

    @property
    def operand(self) -> ExpressionSyntax:
        return self._operand
