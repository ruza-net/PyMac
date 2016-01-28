import pymac.macro
import pymac.utils

from pymac.macro import *
from pymac.utils import *

from pymac.walker import *

from pymac.builtin_macros import *


__author__ = 'Jan Růžička'
__email__ = 'jan.ruzicka01@gmail.com'

__version__ = '0.1'


__all__ = macro.__all__ + utils.__all__


def activate():
    import sys
    from pymac import utils
    from pymac import macros, Macro
    from pymac import import_hook

    sys.meta_path.insert(0, import_hook.FileWithMacros())
