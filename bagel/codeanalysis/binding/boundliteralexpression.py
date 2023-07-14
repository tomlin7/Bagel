from .boundexpression import BoundExpression
from .boundnodekind import BoundNodeKind


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
