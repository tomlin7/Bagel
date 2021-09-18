from CodeAnalysis.expression_syntax import ExpressionSyntax
from CodeAnalysis.syntaxkind import SyntaxKind


class NumberExpressionSyntax(ExpressionSyntax):
    def __init__(self, number_token):
        self._number_token = number_token

    @property
    def kind(self):
        return SyntaxKind.NumberExpression

    def get_children(self):
        return [self.number_token]

    @property
    def number_token(self):
        return self._number_token
