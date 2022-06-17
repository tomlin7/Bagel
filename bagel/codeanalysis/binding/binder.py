from enum import Enum
from typing import List

from ..syntax.binary_expression_syntax import BinaryExpressionSyntax
from ..syntax.expression_syntax import ExpressionSyntax
from ..syntax.literal_expression_syntax import LiteralExpressionSyntax
from ..syntax.syntaxkind import SyntaxKind
from ..syntax.unary_expression_syntax import UnaryExpressionSyntax


class BoundNodeKind(Enum):
    LITERALEXPRESSION = 0
    UNARYEXPRESSION = 1
    BINARYEXPRESSION = 2

class BoundNode:
    _kind: BoundNodeKind

    @property
    def kind(self) -> BoundNodeKind:
        return self._kind

class BoundExpression(BoundNode):
    _type: object

    @property
    def type(self):
        return self._type

class BoundUnaryOperatorKind(Enum):
    IDENTITY = 0
    NEGATION = 1

class BoundLiteralExpression(BoundExpression):
    _value: object

    def __init__(self, value: object):
        self._value = value
    
    @property
    def kind(self) -> BoundNodeKind:
        return BoundNodeKind.LITERALEXPRESSION

    @property
    def type(self):
        return type(self._value)
    
    @property
    def value(self):
        return self._value

class BoundUnaryExpression(BoundExpression):
    _operator_kind: BoundUnaryOperatorKind
    _operand: BoundExpression

    def __init__(self, operator_kind: BoundUnaryOperatorKind, operand: BoundExpression):
        self._operator_kind = operator_kind
        self._operand = operand
    
    @property
    def kind(self) -> BoundNodeKind:
        return BoundNodeKind.UNARYEXPRESSION
    
    @property
    def type(self):
        return self._operand.type
    
    @property
    def operator_kind(self) -> BoundUnaryOperatorKind:
        return self._operator_kind
    
    @property
    def operand(self) -> BoundExpression:
        return self._operand

class BoundBinaryOperatorKind(Enum):
    ADDITION = 0
    SUBTRACTION = 1
    MULTIPLICATION = 2
    DIVISION = 3

class BoundBinaryExpression(BoundExpression):
    _left: BoundExpression
    _operator_kind: BoundUnaryOperatorKind
    _right: BoundExpression

    def __init__(self, left: BoundExpression, operator_kind: BoundBinaryOperatorKind, right: BoundExpression):
        self._left = left
        self._operator_kind = operator_kind
        self._right = right
    
    @property
    def kind(self) -> BoundNodeKind:
        return BoundNodeKind.BINARYEXPRESSION

    @property
    def type(self):
        return self._left.type
        
    @property
    def left(self) -> BoundExpression:
        return self._left

    @property
    def operator_kind(self) -> BoundUnaryOperatorKind:
        return self._operator_kind
    
    @property
    def right(self) -> BoundExpression:
        return self._right

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
