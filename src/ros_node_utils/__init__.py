__version__ = '2.0.0'

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from .nodes import *
from .conversions import *
