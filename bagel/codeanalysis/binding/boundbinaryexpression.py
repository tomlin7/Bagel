from .boundexpression import BoundExpression
from .boundnodekind import BoundNodeKind
from .boundunaryoperatorkind import BoundUnaryOperatorKind
from .boundbinaryoperatorkind import BoundBinaryOperatorKind

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
