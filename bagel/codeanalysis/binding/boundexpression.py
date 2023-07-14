from .boundnode import BoundNode


class BoundExpression(BoundNode):
    _type: object

    @property
    def type(self):
        return self._type
