from __future__ import absolute_import

import sys
import warnings
from .cmap import API  # noqa





if sys.version_info < (3, 0):
    warnings.warn(
        ('Python 2 is not supported anymore. '
         'Please transition to Python 3 to be able to receive updates and fixes.'),
        UserWarning
    )

__version__ = '0.0.02'
# __all__ = []