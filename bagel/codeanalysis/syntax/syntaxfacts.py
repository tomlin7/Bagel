from .syntaxkind import SyntaxKind


class SyntaxFacts:
    @staticmethod
    def get_unary_operator_precedence(kind: SyntaxKind) -> int:
        match kind:
            case SyntaxKind.PLUSTOKEN | SyntaxKind.MINUSTOKEN:
                return 3
            case _:
                return 0
                
    @staticmethod
    def get_binary_operator_precedence(kind: SyntaxKind) -> int:
        match kind:
            case SyntaxKind.STARTOKEN | SyntaxKind.SLASHTOKEN:
                return 2
            case SyntaxKind.PLUSTOKEN | SyntaxKind.MINUSTOKEN:
                return 1
            case _:
                return 0
