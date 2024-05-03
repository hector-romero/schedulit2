import sys

from schedulit.settings.settings import *
from schedulit.settings.environment import *

TESTING = 'test' in sys.argv
if TESTING:  # pragma: no cover
    from schedulit.settings.test import *
