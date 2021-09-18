from CodeAnalysis.expression_syntax import ExpressionSyntax
from CodeAnalysis.syntaxkind import SyntaxKind


class ParenthesizedExpressionSyntax(ExpressionSyntax):
    def __init__(self, open_parenthesis_token, expression, close_parenthesis_token):
        self._open_parenthesis_token = open_parenthesis_token
        self._expression = expression
        self._close_parenthesis_token = close_parenthesis_token

    @property
    def kind(self):
        return SyntaxKind.ParenthesizedExpression

    def get_children(self):
        return [self.open_parenthesis_token, self.expression, self.close_parenthesis_token]

    @property
    def open_parenthesis_token(self):
        return self._open_parenthesis_token

    @property
    def expression(self):
        return self._expression

    @property
    def close_parenthesis_token(self):
        return self._close_parenthesis_token
