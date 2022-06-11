import enum


class SyntaxKind(enum.Enum):
    NumberToken = 1
    WhiteSpaceToken = 2
    PlusToken = 3
    MinusToken = 4
    StarToken = 5
    SlashToken = 6
    OpenParenthesisToken = 7
    CloseParenthesisToken = 8
    BadToken = 9
    EndOfFileToken = 10
    NumberExpression = 11
    BinaryExpression = 12
    ParenthesizedExpression = 13
