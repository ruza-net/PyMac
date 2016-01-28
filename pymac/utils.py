from ast import *

__author__ = 'Jan Růžička'
__email__ = 'jan.ruzicka01@gmail.com'

__version__ = '0.1'

__all__ = ['Wrapped', 'as_ast', 'dict_con']


class Wrapped(AST):
    def __init__(self, contents):
        super(Wrapped, self).__init__()

        self._fields = ('contents',)
        self.contents = contents


def dict_con(*dicts):
    final = {}

    for d in dicts:
        if type(d) is dict:
            for k, v in d.items():
                final[k] = v

    return final


def as_ast(value):
    if type(value) in {int, float}:
        tree = Num(n=value)

    elif type(value) is str:
        tree = Str(s=value)

    elif type(value) is list:
        tree = List(elts=list(map(as_ast, value)), ctx=Load())

    elif type(value) is tuple:
        tree = Tuple(elts=list(map(as_ast, value)), ctx=Load())

    elif type(value) is set:
        tree = Set(elts=list(map(as_ast, value)))

    elif type(value) is dict:
        tree = Dict(keys=list(map(as_ast, value.keys())), values=list(map(as_ast, value.values())))

    elif value is None:
        tree = Name(id='None')

    elif value is True:
        tree = Name(id='True')

    elif value is False:
        tree = Name(id='False')

    elif type(value) is Wrapped:
        tree = value.contents

    elif isinstance(value, AST):
        fields = [keyword(x, as_ast(y)) for x, y in iter_fields(value)]

        tree = Call(Name(id=value.__class__.__name__, ctx=Load()), [], fields)

    else:
        print('Warning: don\'t know how to convert:  {}  to AST, performing implicit Call to its __class__!'.format(
            value))

        tree = Call(Name(id=value.__class__.__name__))

    return tree
