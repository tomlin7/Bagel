from CodeAnalysis.expression_syntax import ExpressionSyntax
from CodeAnalysis.syntaxkind import SyntaxKind


class BinaryExpressionSyntax(ExpressionSyntax):
    def __init__(self, left, operator_token, right):
        self._left = left
        self._operator_token = operator_token
        self._right = right

    @property
    def kind(self):
        return SyntaxKind.BinaryExpression

    def get_children(self):
        # can be an array too
        return [self.left, self.operator_token, self.right]

    @property
    def left(self):
        return self._left

    @property
    def operator_token(self):
        return self._operator_token

    @property
    def right(self):
        return self._right
