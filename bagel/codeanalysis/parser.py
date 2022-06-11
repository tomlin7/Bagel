from .binary_expression_syntax import BinaryExpressionSyntax
from .expression_syntax import ExpressionSyntax
from .lexer import Lexer
from .number_expression_syntax import NumberExpressionSyntax
from .parenthesized_expression_syntax import ParenthesizedExpressionSyntax
from .syntaxkind import SyntaxKind
from .syntaxtoken import SyntaxToken
from .syntaxtree import SyntaxTree


class Parser:
    def __init__(self, text: str):
        self._diagnostics = []
        self._position = 0
        self._tokens = []

        lexer = Lexer(text)
        token = lexer.next_token()

        self._tokens.append(token)

        while token.kind != SyntaxKind.EndOfFileToken:
            token = lexer.next_token()

            if token.kind not in [SyntaxKind.WhiteSpaceToken, SyntaxKind.BadToken]:
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

    def match(self, kind: SyntaxKind) -> SyntaxToken:
        if self.current.kind == kind:
            return self.next_token()

        self._diagnostics.append(f"ERROR: Unexpected token <'{self.current.kind}'>, expected <{kind}>")
        return SyntaxToken(kind, self.current.position, None, None)

    def parse(self) -> SyntaxTree:
        expression = self.parse_term()
        end_of_file_token = self.match(SyntaxKind.EndOfFileToken)
        return SyntaxTree(self._diagnostics, expression, end_of_file_token)

    def parse_expression(self) -> ExpressionSyntax:
        return self.parse_term()

    def parse_term(self) -> ExpressionSyntax:
        left = self.parse_factor()

        while self.current.kind in [SyntaxKind.PlusToken, SyntaxKind.MinusToken]:
            operator_token = self.next_token()
            right = self.parse_factor()
            left = BinaryExpressionSyntax(left, operator_token, right)

        return left

    def parse_factor(self) -> ExpressionSyntax:
        left = self.parse_primary_expression()

        while self.current.kind in [SyntaxKind.StarToken, SyntaxKind.SlashToken]:
            operator_token = self.next_token()
            right = self.parse_primary_expression()
            left = BinaryExpressionSyntax(left, operator_token, right)

        return left

    def parse_primary_expression(self) -> ExpressionSyntax:
        if self.current.kind == SyntaxKind.OpenParenthesisToken:
            left = self.next_token()
            expression = self.parse_expression()
            right = self.match(SyntaxKind.CloseParenthesisToken)
            return ParenthesizedExpressionSyntax(left, expression, right)

        number_token = self.match(SyntaxKind.NumberToken)
        return NumberExpressionSyntax(number_token)
