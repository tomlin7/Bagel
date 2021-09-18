import os

import colorama
from colorama import Fore

from CodeAnalysis.evaluator import Evaluator
from CodeAnalysis.syntaxtoken import SyntaxToken
from CodeAnalysis.syntaxtree import SyntaxTree

colorama.init(autoreset=True)
showtree = False


def pretty_print(node, indent="", is_last=True):
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
    except IndexError:
        last_child = None

    for child in node.get_children():
        pretty_print(child, indent, last_child == child)


while True:
    line = input("» ")

    # ideas
    # a = input("» ")
    # a = input("› ")
    # a = input("¶ ")
    # a = input("~ ")
    # a = input("⇝ ")
    # a = input("⇢ ")
    # a = input("⇻ ")
    # a = input("⇾ ")
    # a = input("∢ ")
    # a = input("∝ ")
    # a = input("⊱ ")

    # a = input("⊶ ")
    # a = input("⊷ ")
    # a = input("⊸ ")

    # a = input("⋉ ")
    # a = input("⋯ ")
    # a = input("⨊ ")
    # a = input("⨭ ")
    # a = input("⫻ ")

    if line is None or line == "":
        break

    if line == "#showtree":
        showtree = not showtree
        print("Showing parser trees" if showtree else "Not showing parser trees")
        continue
    elif line == "#cls":
        os.system('cls')
        continue

    syntax_tree = SyntaxTree.parse(line)

    if showtree:
        pretty_print(syntax_tree.root)

    if not len(syntax_tree.diagnostics) > 0:
        evaluator = Evaluator(syntax_tree.root)
        result = evaluator.evaluate()
        print(str(result))
    else:
        for _diagnostic in syntax_tree.diagnostics:
            print(Fore.RED + _diagnostic)
