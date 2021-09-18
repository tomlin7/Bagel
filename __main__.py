import enum, os

import colorama
from colorama import Fore

colorama.init(autoreset=True)
clear = lambda: os.system('cls')

# 1 + 2 * 3
#
#     +
#    / \
#   1   *
#      / \
#     2   3

# 1 + 2 + 3
#
#       +
#      / \
#     +   3
#    / \
#   1   2




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

class SyntaxNode:
    @property
    def kind(self):
        pass

    def get_children(self):
        return []

class SyntaxToken(SyntaxNode):
    def __init__(self, kind, position, text, value):
        self._kind = kind
        self._position = position
        self._text = text
        self._value = value
    
    @property
    def kind(self):
        return self._kind

    def get_children(self):
        return []
    
    @property
    def position(self):
        return self._position
    @property
    def text(self):
        return self._text
    @property
    def value(self):
        return self._value

class Lexer:
    def __init__(self, text):
        self._text = text
        self._position = 0
        self._diagnostics = []
    
    @property
    def diagnostics(self):
        return self._diagnostics

    @property
    def current(self):
        if self._position >= len(self._text):
            return '\0'
        return self._text[self._position]

    def next(self):
        self._position += 1

    def next_token(self):
        # <numbers>
        # + - * /
        # <whitespace>

        if self._position >= len(self._text):
            return SyntaxToken(SyntaxKind.EndOfFileToken, self._position, '\0', None)

        if self.current.isdigit():
            start = self._position

            while (self.current.isdigit()):
                self.next()
            
            length = self._position - start
            text = self._text[start:length + start]
            try:
                value = int(text)
            except ValueError:
                self._diagnostics.append(f"The number {self._text} isn't a valid int.")
            return SyntaxToken(SyntaxKind.NumberToken, start, text, value)

        if self.current.isspace():
            start = self._position

            while (self.current.isspace()):
                self.next()
            
            length = self._position - start
            text = self._text[start:length + start]
            return SyntaxToken(SyntaxKind.WhiteSpaceToken, start, text, None)

        if self.current == '+':
            self._position += 1
            return SyntaxToken(SyntaxKind.PlusToken, self._position, '+', None)
        elif self.current == '-':
            self._position += 1
            return SyntaxToken(SyntaxKind.MinusToken, self._position, '-', None)
        elif self.current == '*':
            self._position += 1
            return SyntaxToken(SyntaxKind.StarToken, self._position, '*', None)
        elif self.current == '/':
            self._position += 1
            return SyntaxToken(SyntaxKind.SlashToken, self._position, '/', None)
        elif self.current == '(':
            self._position += 1
            return SyntaxToken(SyntaxKind.OpenParenthesisToken, self._position, '(', None)
        elif self.current == ')':
            self._position += 1
            return SyntaxToken(SyntaxKind.CloseParenthesisToken, self._position, ')', None)

        self._diagnostics.append(f"ERROR: bad character input: '{self.current}'")
        self._position += 1
        return SyntaxToken(SyntaxKind.BadToken, self._position, self._text[self._position - 1:1], None)

class ExpressionSyntax(SyntaxNode):
    pass

class NumberExpressionSyntax(ExpressionSyntax):
    def __init__(self, number_token):
        self._number_token = number_token
    
    @property
    def kind(self):
        return SyntaxKind.NumberExpression

    def get_children(self):
        return [self.number_token]

    @property
    def number_token(self):
        return self._number_token

class BinaryExpressionSyntax(ExpressionSyntax):
    def __init__(self, left, operator_token, right):
        self._left = left
        self._operator_token = operator_token
        self._right = right

    @property
    def kind(self):
        return SyntaxKind.BinaryExpression

    def get_children(self):
        # can be an array too
        return [self.left, self.operator_token, self.right]

    @property
    def left(self):
        return self._left
    @property
    def operator_token(self):
        return self._operator_token
    @property
    def right(self):
        return self._right

class ParenthesizedExpressionSyntax(ExpressionSyntax):
    def __init__(self, open_parenthesis_token, expression, close_parenthesis_token):
        self._open_parenthesis_token = open_parenthesis_token
        self._expression = expression
        self._close_parenthesis_token = close_parenthesis_token

    @property
    def kind(self):
        return SyntaxKind.ParenthesizedExpression

    def get_children(self):
        return [self.open_parenthesis_token, self.expression, self.close_parenthesis_token]

    @property
    def open_parenthesis_token(self):
        return self._open_parenthesis_token
    @property
    def expression(self):
        return self._expression
    @property
    def close_parenthesis_token(self):
        return self._close_parenthesis_token

class SyntaxTree:
    def __init__(self, diagnostics, root, end_of_file_token):
        self._diagnostics = diagnostics
        self._root = root
        self._end_of_file_token = end_of_file_token
    
    @property
    def diagnostics(self):
        return self._diagnostics
    @property
    def root(self):
        return self._root
    @property
    def end_of_file_token(self):
        return self._end_of_file_token   

    @staticmethod
    def parse(text):
        parser = Parser(text)
        return parser.parse() 

class Parser:
    def __init__(self, text):
        self._diagnostics = []
        self._position = 0
        self._tokens = []
        
        lexer = Lexer(text)
        token = lexer.next_token()
        
        self._tokens.append(token)

        while token.kind != SyntaxKind.EndOfFileToken:
            token = lexer.next_token()

            if token.kind not in [SyntaxKind.WhiteSpaceToken, SyntaxKind.BadToken]:
                self._tokens.append(token)
        
        self._diagnostics += lexer.diagnostics
    
    @property
    def diagnostics(self):
        return self._diagnostics
    
    def peek(self, offset=0):
        index = self._position + offset
        if index >= len(self._tokens):
            return self._tokens[len(self._tokens) - 1]

        return self._tokens[index]

    @property
    def current(self):
        return self.peek()

    def next_token(self):
        current = self.current
        self._position += 1
        return current
    
    def match(self, kind):
        if self.current.kind == kind:
            return self.next_token()
        
        self._diagnostics.append(f"ERROR: Unexpected token <'{self.current.kind}'>, expected <{kind}>")
        return SyntaxToken(kind, self.current.position, None, None)

    def parse(self):
        expression = self.parse_term()
        end_of_file_token = self.match(SyntaxKind.EndOfFileToken)
        return SyntaxTree(self._diagnostics, expression, end_of_file_token)
    
    def parse_expression(self):
        return self.parse_term()
    
    def parse_term(self):
        left = self.parse_factor()

        while self.current.kind in [SyntaxKind.PlusToken, SyntaxKind.MinusToken]:
            operator_token = self.next_token()
            right = self.parse_factor()
            left = BinaryExpressionSyntax(left, operator_token, right)
        
        return left

    # parse_multiplicative_expression
    def parse_factor(self):
        left = self.parse_primary_expression()

        while self.current.kind in [SyntaxKind.StarToken, SyntaxKind.SlashToken]:
            operator_token = self.next_token()
            right = self.parse_primary_expression()
            left = BinaryExpressionSyntax(left, operator_token, right)
        
        return left


    def parse_primary_expression(self):
        if self.current.kind == SyntaxKind.OpenParenthesisToken:
            left = self.next_token()
            expression = self.parse_expression()
            right = self.match(SyntaxKind.CloseParenthesisToken)
            return ParenthesizedExpressionSyntax(left, expression, right)

        number_token = self.match(SyntaxKind.NumberToken)
        return NumberExpressionSyntax(number_token)
    
    def parse_binary_expression(self):
        pass

class Evaluator:
    def __init__(self, root):
        self._root = root

    def evaluate(self):
        return self.evaluate_expression(self._root)

    def evaluate_expression(self, node):
        # binary expression
        # number expression

        if type(node) is NumberExpressionSyntax:
            return int(node.number_token.value)

        if type(node) is BinaryExpressionSyntax:
            left = self.evaluate_expression(node.left)
            right = self.evaluate_expression(node.right)

            if node.operator_token.kind == SyntaxKind.PlusToken:
                return left + right
            elif node.operator_token.kind == SyntaxKind.MinusToken:
                return left - right
            elif node.operator_token.kind == SyntaxKind.StarToken:
                return left * right
            elif node.operator_token.kind == SyntaxKind.SlashToken:
                return left / right
            else:
                raise Exception(f"Unexpected binary operator {node.operator_token.kind}")

        if type(node) is ParenthesizedExpressionSyntax:
            return self.evaluate_expression(node.expression)

        raise Exception(f"Unexpected node {node.kind}")

class Colors:
    @staticmethod
    def get_color(kind):
        if kind in [SyntaxKind.PlusToken, SyntaxKind.MinusToken, SyntaxKind.StarToken, SyntaxKind.SlashToken]:
            return Fore.GREEN
        elif kind in [SyntaxKind.NumberToken]:
            return Fore.YELLOW
        elif kind in [SyntaxKind.OpenParenthesisToken, SyntaxKind.CloseParenthesisToken]:
            return Fore.BLUE
        elif kind in [SyntaxKind.WhiteSpaceToken, SyntaxKind.EndOfFileToken]:
            return Fore.LIGHTBLACK_EX
        else:
            return Fore.RED

class ConsoleColor:
    @property
    def Red(self): return Fore.RED
    @property
    def Green(self): return Fore.GREEN
    @property
    def Yellow(self): return Fore.YELLOW
    @property
    def Blue(self): return Fore.BLUE
    @property
    def Magenta(self): return Fore.MAGENTA
    @property
    def Cyan(self): return Fore.CYAN
    @property
    def White(self): return Fore.WHITE
    @property
    def Black(self): return Fore.BLACK
    @property
    def DarkGrey(self): return Fore.LIGHTBLACK_EX
    @property
    def Default(self): return Fore.RESET

class Console:
    def __init__(self):
        self.foreground_color = ConsoleColor().Default
    
    def write(self, *args):
        print(self.foreground_color + ''.join(args))

    def reset(self):
        self.foreground_color = ConsoleColor().Default

def pretty_print(node, indent="", is_last=True):
    # └──
    # ├──
    # │ 

    marker = '└──' if is_last else '├──'

    print(indent, end="")
    print(marker, end="")
    print(node.kind.name, end="")
    
    if type(node) is SyntaxToken:
        if node.value is not None:
            print(" ", end="")
            print(node.value, end="")

    print()

    indent += '    ' if is_last else '│   '

    try:
        last_child = node.get_children()[-1]
    except:
        last_child = None

    for child in node.get_children():
        pretty_print(child, indent, last_child == child)

# console = Console()
# consoleColor = ConsoleColor()

showtree = False
while True:
    line = input("> ")

    if line is None or line == "":
        break

    if line == "#showtree":
        showtree = not showtree
        print("Showing parser trees" if showtree else "Not showing parser trees")
        continue
    elif line == "#cls":
        clear()
        continue

    syntax_tree = SyntaxTree.parse(line)

    if showtree:
        # color = console.foreground_color
        # console.foreground_color = consoleColor.DarkGrey

        pretty_print(syntax_tree.root)
        # console.foreground_color = color

    if not len(syntax_tree.diagnostics) > 0:
        evaluator = Evaluator(syntax_tree.root)
        result = evaluator.evaluate()
        print(str(result))
    else:
        for _diagnostic in syntax_tree.diagnostics:
            print(Fore.RED + _diagnostic)