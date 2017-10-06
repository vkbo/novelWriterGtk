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

class TreeNodes(Enum):
    
    BOOK      = 10
    CHARS     = 20
    PLOTS     = 30
    NOTES     = 40
    
    BOOK_PRO  = 11
    BOOK_CHAP = 12
    BOOK_EPI  = 13
    
    CHAR_MAIN = 21
    CHAR_SEC  = 22
    CHAR_MIN  = 23
    
    PLOT_MAIN = 31
    PLOT_SUB  = 32
    PLOT_MIN  = 33
    