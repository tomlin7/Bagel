from CodeAnalysis.syntaxkind import SyntaxKind


class SyntaxNode:
    @property
    def kind(self):
        return SyntaxKind.BadToken

    def get_children(self):
        return []
