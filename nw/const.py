# -*- coding: utf-8 -*
"""novelWriter Constants

 novelWriter – Constants
=========================
 Constants

 File History:
 Created: 2017-10-07 [0.4.0]

"""

import logging

from enum import Enum

logger = logging.getLogger(__name__)

class NBTabs(Enum):
    
    BOOK   = 0
    CHARS  = 1
    EDITOR = 2
    PLOTS  = 3
