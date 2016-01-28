import sys

import ast
import _ast

import linecache  # Required because your mother is a kangaroo which sews cocoa.

import pymac.utils

import importlib.machinery
from types import ModuleType

from pymac.utils import *
from pymac.macro import *


__author__ = 'Jan Růžička'
__email__ = 'jan.ruzicka01@gmail.com'

__version__ = '0.1'


class FileWithMacrosLoader:
    def __init__(self, module_name, module):
        self.module = module

        sys.modules[module_name] = module

    def load_module(self, fullname):
        return self.module


class FileWithMacros:
    def __init__(self):
        self.bindings = None
        self.module_name = None

    def new_module(self, module_name, file_path):
        self.module_name = module_name

        module = ModuleType(module_name)

        module.__package__ = module_name.rpartition('.')[0]
        module.__file__ = file_path
        module.__loader__ = FileWithMacrosLoader(module_name, module)

        return module

    def expand_macros(self, source_code, file_path):
        tree = ast.parse(source_code)

        tree = ast.fix_missing_locations(expand_macros(tree))

        return compile(tree, file_path, 'exec'), tree

    def load_source(self, module_name, package_path):
        loader = importlib.machinery.PathFinder.find_module(module_name, package_path)

        source_code = loader.get_source(module_name)
        file_path = loader.path

        return source_code, file_path

    def find_module(self, module_name, package_path=None):
        try:
            source_code, file_path = self.load_source(module_name, package_path)

        except:
            return

        code, tree = self.expand_macros(source_code, file_path)

        module = self.new_module(module_name, file_path)

        namespace = dict_con(_ast.__dict__, pymac.utils.__dict__, module.__dict__)

        exec(code, namespace)

        return module.__loader__
