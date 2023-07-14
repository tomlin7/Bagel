from .boundnodekind import BoundNodeKind


class BoundNode:
    _kind: BoundNodeKind

    @property
    def kind(self) -> BoundNodeKind:
        return self._kind
