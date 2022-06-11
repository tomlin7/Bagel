from .binary_expression_syntax import BinaryExpressionSyntax
from .expression_syntax import ExpressionSyntax
from .number_expression_syntax import NumberExpressionSyntax
from .parenthesized_expression_syntax import ParenthesizedExpressionSyntax
from .syntaxkind import SyntaxKind


class Evaluator:
    def __init__(self, root: ExpressionSyntax):
        self._root = root

    def evaluate(self) -> int:
        return self.evaluate_expression(self._root)

    def evaluate_expression(self, node: ExpressionSyntax) -> int:
        if type(node) is NumberExpressionSyntax:
            return int(node.number_token.value)

        if type(node) is BinaryExpressionSyntax:
            left = self.evaluate_expression(node.left)
            right = self.evaluate_expression(node.right)

            if node.operator_token.kind == SyntaxKind.PlusToken:
                return left + right
            elif node.operator_token.kind == SyntaxKind.MinusToken:
                return left - right
            elif node.operator_token.kind == SyntaxKind.StarToken:
                return left * right
            elif node.operator_token.kind == SyntaxKind.SlashToken:
                return left / right
            else:
                raise Exception(f"Unexpected binary operator {node.operator_token.kind}")

        if type(node) is ParenthesizedExpressionSyntax:
            return self.evaluate_expression(node.expression)

        raise Exception(f"Unexpected node {node.kind}")
