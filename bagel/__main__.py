import os

import colorama
from colorama import Fore

from codeanalysis.binding.binder import Binder

from codeanalysis.evaluator import Evaluator
from codeanalysis.syntax.syntaxnode import SyntaxNode
from codeanalysis.syntax.syntaxtoken import SyntaxToken
from codeanalysis.syntax.syntaxtree import SyntaxTree

colorama.init(autoreset=True)
SHOW_TREE = False


def pretty_print(node: SyntaxNode, indent: str = "", is_last: bool = True):
    marker = '└──' if is_last else '├──'

    print(indent, end="")
    print(marker, end="")
    print(node.kind.name, end="")

    if type(node) is SyntaxToken:
        if node.value is not None:
            print(" ", end="")
            print(node.value, end="")

    print()

    indent += '   ' if is_last else '│   '

    try:
        last_child = node.get_children()[-1]
    except IndexError:
        last_child = None

    for child in node.get_children():
        pretty_print(child, indent, last_child == child)


while True:
    line = input("» ")

    if line is None or line == "":
        break

    if line == "#showtree":
        SHOW_TREE = not SHOW_TREE
        print("Showing parser trees" if SHOW_TREE else "Not showing parser trees")
        continue
    elif line == "#cls":
        os.system('cls')
        continue

    syntax_tree = SyntaxTree.parse(line)
    binder = Binder()
    bound_expression = binder.bind_expression(syntax_tree.root)

    diagnostics = syntax_tree.diagnostics + binder.diagnostics

    if SHOW_TREE:
        pretty_print(syntax_tree.root)

    if not any(syntax_tree.diagnostics):
        evaluator = Evaluator(bound_expression)
        result = evaluator.evaluate()
        print(result)
    else:
        for _diagnostic in syntax_tree.diagnostics:
            print(Fore.RED + _diagnostic)
