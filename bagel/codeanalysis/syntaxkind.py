import enum


class SyntaxKind(enum.Enum):
    # Tokens
    BadToken = 0
    EndOfFileToken = 1
    WhiteSpaceToken = 2
    NumberToken = 3
    PlusToken = 4
    MinusToken = 5
    StarToken = 6
    SlashToken = 7
    OpenParenthesisToken = 8
    CloseParenthesisToken = 9
    
    # Expressions
    LiteralExpression = 10
    BinaryExpression = 11
    ParenthesizedExpression = 12
