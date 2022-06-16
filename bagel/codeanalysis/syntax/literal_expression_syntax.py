from .expression_syntax import ExpressionSyntax
from .syntaxkind import SyntaxKind
from .syntaxtoken import SyntaxToken


class LiteralExpressionSyntax(ExpressionSyntax):
    _literal_token: SyntaxToken
    
    def __init__(self, literal_token: SyntaxToken):
        self._literal_token = literal_token

    @property
    def kind(self) -> SyntaxKind:
        return SyntaxKind.LITERALEXPRESSION

    def get_children(self) -> list:
        return [self.literal_token]

    @property
    def literal_token(self) -> SyntaxToken:
        return self._literal_token

