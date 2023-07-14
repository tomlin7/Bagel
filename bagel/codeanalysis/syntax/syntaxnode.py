from .syntaxkind import SyntaxKind


class SyntaxNode:
    @property
    def kind(self):
        return SyntaxKind.BADTOKEN

    def get_children(self):
        return []
