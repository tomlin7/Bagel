from .binding import (BoundBinaryExpression, BoundBinaryOperatorKind,
                             BoundExpression, BoundLiteralExpression,
                             BoundUnaryExpression, BoundUnaryOperatorKind)


class Evaluator:
    _root: BoundExpression

    def __init__(self, root: BoundExpression):
        self._root = root

    def evaluate(self) -> object:
        return self.evaluate_expression(self._root)

    def evaluate_expression(self, node: BoundExpression) -> object:
        if isinstance(node, BoundLiteralExpression):
            return node.value

        if isinstance(node, BoundUnaryExpression):
            operand = int(self.evaluate_expression(node.operand))

            match node.operator_kind:
                case BoundUnaryOperatorKind.IDENTITY:
                    return operand
                case BoundUnaryOperatorKind.NEGATION:
                    return -operand
                case _:
                    raise Exception(f"Unexpected unary operator {node.operator_kind}")

        if isinstance(node, BoundBinaryExpression):
            left = int(self.evaluate_expression(node.left))
            right = int(self.evaluate_expression(node.right))

            match node.operator_kind:
                case BoundBinaryOperatorKind.ADDITION:
                    return left + right
                case BoundBinaryOperatorKind.SUBTRACTION:
                    return left - right
                case BoundBinaryOperatorKind.MULTIPLICATION:
                    return left * right
                case BoundBinaryOperatorKind.DIVISION:
                    return left / right
                case _:
                    raise Exception(f"Unexpected binary operator {node.operator_kind}")

        raise Exception(f"Unexpected node {node.kind}")
