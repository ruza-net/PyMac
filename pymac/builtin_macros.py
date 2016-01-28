import ast as ast_module

from pymac import *
from pymac.utils import *

__author__ = 'Jan Růžička'
__email__ = 'jan.ruzicka01@gmail.com'

__version__ = '0.1'


@Macro
def ast(tree):
    return as_ast(tree)


@Macro
def u(tree):
    return Wrapped(tree)


@Walker
def u_search(node, skip, modify, **kw):
    if type(node) is ast_module.Subscript and type(node.value) is ast_module.Name and node.value.id == 'u':
        skip()
        modify()

        return expand_macros(node)


@Walker
def macro_search(node, skip, modify, **kw):
    if type(node) is ast_module.Subscript and type(node.value) is ast_module.Name and node.value.id in macros:
        skip()
        modify()

        return expand_macros(node)


@Macro
def q(tree):
    tree = u_search.walk(tree)

    return as_ast(tree)


@Macro
def dump(tree):
    new_tree = macro_search.walk(tree)

    return ast_module.Call(ast_module.Name(id='dump', ctx=ast_module.Load()), [new_tree], [])
