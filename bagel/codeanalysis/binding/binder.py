from typing import List

from ..syntax.binary_expression_syntax import BinaryExpressionSyntax
from ..syntax.expression_syntax import ExpressionSyntax
from ..syntax.literal_expression_syntax import LiteralExpressionSyntax
from ..syntax.syntaxkind import SyntaxKind
from ..syntax.unary_expression_syntax import UnaryExpressionSyntax

from .boundexpression import BoundExpression
from .boundbinaryexpression import BoundBinaryExpression
from .boundunaryexpression import BoundUnaryExpression
from .boundliteralexpression import BoundLiteralExpression
from .boundunaryoperatorkind import BoundUnaryOperatorKind
from .boundbinaryoperatorkind import BoundBinaryOperatorKind


class Binder:
    _diagnostics: List[str]

    def __init__(self):
        self._diagnostics = []

    @property
    def diagnostics(self) -> List[str]:
        return self._diagnostics

    def bind_expression(self, syntax: ExpressionSyntax) -> BoundExpression:
        match syntax.kind:
            case SyntaxKind.LITERALEXPRESSION:
                return self.bind_literal_expression(syntax)
            case SyntaxKind.UNARYEXPRESSION:
                return self.bind_unary_expression(syntax)
            case SyntaxKind.BINARYEXPRESSION:
                return self.bind_binary_expression(syntax)
            case _:
                raise Exception(f"Unexpected syntax {syntax.kind}")

    def bind_literal_expression(self, syntax: LiteralExpressionSyntax) -> BoundLiteralExpression:
        value = syntax.literal_token.value or 0
        return BoundLiteralExpression(value)

    def bind_unary_expression(self, syntax: UnaryExpressionSyntax) -> BoundUnaryExpression:
        bound_operand = self.bind_expression(syntax.operand)
        bound_operator_kind = self.bind_unary_operator_kind(syntax.operator_token.kind, bound_operand.type)

        if bound_operator_kind is None:
            self._diagnostics.append(f"Unary operator {syntax.operator_token.text} is not defined for type {bound_operand.type}.")
            return bound_operand
        
        return BoundUnaryExpression(bound_operator_kind, bound_operand)

    def bind_binary_expression(self, syntax: BinaryExpressionSyntax) -> BoundBinaryExpression:
        bound_left = self.bind_expression(syntax.left)
        bound_right = self.bind_expression(syntax.right)
        bound_operator_kind = self.bind_binary_operator_kind(syntax.operator_token.kind, bound_left.type, bound_right.type)
        if bound_operator_kind is None:
            self._diagnostics.append(f"Binary operator {syntax.operator_token.text} is not defined for types {bound_left.type} and {bound_right.type}.")
            return bound_left
        
        return BoundBinaryExpression(bound_left, bound_operator_kind, bound_right)
    
    def bind_unary_operator_kind(self, kind: SyntaxKind, operand_type: int) -> BoundUnaryOperatorKind | None:
        if operand_type != int:
            return

        match kind:
            case SyntaxKind.PLUSTOKEN:
                return BoundUnaryOperatorKind.IDENTITY
            case SyntaxKind.MINUSTOKEN:
                return BoundUnaryOperatorKind.NEGATION
            case _:
                raise Exception(f"Unexpected unary operator kind {kind}")
    
    def bind_binary_operator_kind(self, kind: SyntaxKind, left_type: int, right_type: int) -> BoundBinaryOperatorKind | None:
        if left_type != int or right_type != int:
            return

        match kind:
            case SyntaxKind.PLUSTOKEN:
                return BoundBinaryOperatorKind.ADDITION
            case SyntaxKind.MINUSTOKEN:
                return BoundBinaryOperatorKind.SUBTRACTION
            case SyntaxKind.STARTOKEN:
                return BoundBinaryOperatorKind.MULTIPLICATION
            case SyntaxKind.SLASHTOKEN:
                return BoundBinaryOperatorKind.DIVISION
            case _:
                raise Exception(f"Unexpected binary operator kind {kind}")
