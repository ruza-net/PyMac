from ast import *


__author__ = 'Jan Růžička'
__email__ = 'jan.ruzicka01@gmail.com'

__version__ = '0.1'


__all__ = ['Macro', 'macros', 'expand_macros']


class Macros:
    def __init__(self):
        self.registry = {}

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __contains__(self, item):
        return item in self.registry


macros = Macros()


class Macro:
    def __init__(self, func):
        macros.registry[func.__name__] = func

        self.func = func

    def expand(self, tree):
        return self.func(tree)


def expand_macros(tree):
    new_tree = MacroExpander().visit(tree)

    return new_tree


class MacroExpander(NodeTransformer):
    def visit_Call(self, node):
        new_tree = node

        new_tree.args = [self.visit(x) for x in node.args]

        return new_tree

    def visit_Subscript(self, node):
        if node.value.id in macros and type(node.slice) is Index:
            return macros.registry[node.value.id](node.slice.value)

    def generic_visit(self, node):
        new_tree = node

        if hasattr(node, 'value'):
            new_tree.value = self.visit(node.value)

        elif hasattr(node, 'elts'):
            new_tree.elts = [self.visit(x) for x in node.elts]

        elif hasattr(node, 'body'):
            new_tree.body = [self.visit(x) for x in node.body]

        return new_tree
