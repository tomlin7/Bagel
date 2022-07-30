from .boundnodekind import BoundNodeKind
from .boundunaryoperatorkind import BoundUnaryOperatorKind
from .boundexpression import BoundExpression

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