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

class ItemType(Enum):
    
    BOOK        = 10
    CHARS       = 20
    PLOTS       = 30
    NOTES       = 40

class BookType(Enum):
    
    FRONTMATTER = 11
    PROLOGUE    = 12
    CHAPTER     = 13
    EPILOGUE    = 14
    BACKMATTER  = 15

class ItemClass(Enum):
    
    CONTAINER = 0
    DOCUMENT  = 1
    DIVIDER   = 2

class ItemLevel(Enum):
    
    ROOT = 0
    ITEM = 1
    FILE = 2

class BookTree(Enum):
    
    CLASS      = 0
    LEVEL      = 1
    TYPE       = 2
    HANDLE     = 3
    PARENT     = 4
    NAME       = 5
    SUBTYPE    = 6
    NUMBER     = 7
    COMPILE    = 8
    COMMENT    = 9
    IMPORTANCE = 10
    ROLE       = 11

class ChapterTree(Enum):
    
    TYPE    = 0
    NUMBER  = 1
    COMPILE = 2
    COMMENT = 3

class CharTree(Enum):
    
    IMPORTANCE = 0
    ROLE       = 1
    COMMENT    = 2

class PlotTree(Enum):
    
    IMPORTANCE = 0
    COMMENT    = 1

class NBTabs(Enum):
    
    BOOK   = 0
    CHARS  = 1
    EDITOR = 2
    PLOTS  = 3
