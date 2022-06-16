from .unary_expression_syntax import UnaryExpressionSyntax
from .binary_expression_syntax import BinaryExpressionSyntax
from .expression_syntax import ExpressionSyntax
from .lexer import Lexer
from .literal_expression_syntax import LiteralExpressionSyntax
from .parenthesized_expression_syntax import ParenthesizedExpressionSyntax
from .syntaxkind import SyntaxKind
from .syntaxtoken import SyntaxToken
from .syntaxtree import SyntaxTree
from .syntaxfacts import SyntaxFacts


class Parser:
    _diagnostics: list
    
    def __init__(self, text: str):
        self._diagnostics = []
        self._position = 0
        self._tokens = []

        lexer = Lexer(text)
        token = lexer.lex()

        self._tokens.append(token)

        while token.kind != SyntaxKind.EOFTOKEN:
            token = lexer.lex()

            if token.kind not in [SyntaxKind.WHITESPACETOKEN, SyntaxKind.BADTOKEN]:
                self._tokens.append(token)

        self._diagnostics += lexer.diagnostics

    @property
    def diagnostics(self) -> list:
        return self._diagnostics

    def peek(self, offset: int = 0) -> SyntaxToken:
        index = self._position + offset
        if index >= len(self._tokens):
            return self._tokens[len(self._tokens) - 1]

        return self._tokens[index]

    @property
    def current(self) -> SyntaxToken:
        return self.peek()

    def next_token(self) -> SyntaxToken:
        current = self.current
        self._position += 1
        return current

    def match_token(self, kind: SyntaxKind) -> SyntaxToken:
        if self.current.kind == kind:
            return self.next_token()

        self._diagnostics.append(
            f"ERROR: Unexpected token <'{self.current.kind}'>, expected <{kind}>")
        return SyntaxToken(kind, self.current.position, None, None)

    def parse(self) -> SyntaxTree:
        expression = self.parse_expression()
        end_of_file_token = self.match_token(SyntaxKind.EOFTOKEN)
        return SyntaxTree(self._diagnostics, expression, end_of_file_token)

    def parse_expression(self, parent_precedence: int=0) -> ExpressionSyntax:
        left = None
        unary_operator_precedence = SyntaxFacts.get_unary_operator_precedence(self.current.kind)
        if unary_operator_precedence != 0 and unary_operator_precedence >= parent_precedence:
            operator_token = self.next_token()
            operand = self.parse_expression(unary_operator_precedence)
            left = UnaryExpressionSyntax(operator_token, operand)
        else:
            left = self.parse_primary_expression()

        while True:
            precedence = SyntaxFacts.get_binary_operator_precedence(self.current.kind)
            if not precedence or precedence <= parent_precedence:
                break

            operator_token = self.next_token()
            right = self.parse_expression(precedence)
            left = BinaryExpressionSyntax(left, operator_token, right)

        return left

    def parse_primary_expression(self) -> ExpressionSyntax:
        if self.current.kind == SyntaxKind.OPENPARENTOKEN:
            left = self.next_token()
            expression = self.parse_expression()
            right = self.match_token(SyntaxKind.CLOSEPARENTOKEN)
            return ParenthesizedExpressionSyntax(left, expression, right)

        literal_token = self.match_token(SyntaxKind.NUMBERTOKEN)
        return LiteralExpressionSyntax(literal_token)
