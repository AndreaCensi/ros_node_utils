__version__ = '1.1.1'

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from .nodes import *
from .conversions import *
