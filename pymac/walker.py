import ast

__author__ = 'Jan Růžička'
__email__ = 'jan.ruzicka01@gmail.com'

__version__ = '0.1'


class Walker:
    def __init__(self, func):
        self.func = func

    def walk(self, tree):
        return self.walk_collect(tree)[0]

    def collect(self, tree):
        return self.walk_collect(tree)[1]

    def walk_collect(self, tree):
        collection = []

        modify_node = [False]
        proceed = [True]

        node = tree  # TODO: Recursively walk over the tree

        def modify():
            modify_node[0] = True

        def collect(what):
            collection.append(what)

        def skip():
            proceed[0] = False

        try:
            new_node = self.func(node=node, collect=collect, skip=skip, modify=modify)

            if modify_node[0]:
                node = new_node

            if proceed[0]:
                try:
                    for x, y in ast.iter_fields(node):
                        if type(y) is list:
                            out = [self.walk_collect(_y) for _y in y]

                            t, c = [x[0] for x in out], [x[1] for x in out]

                        else:
                            t, c = self.walk_collect(y)

                        collection += c
                        setattr(node, x, t)

                except AttributeError:
                    return node, collection

            return node, collection

        except Exception as e:
            raise
