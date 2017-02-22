# -*- coding: utf-8 -*
"""novelWriter Init

novelWriter – Init File
=======================
Application initialisation

File History:
Created: 2017-01-10 [0.1.0]

"""

import logging as logger
import gi

gi.require_version("Gtk","3.0")

from gi.repository import Gtk, GdkPixbuf
from os            import path
from nw.config     import Config

__author__     = "Veronica Berglyd Olsen"
__copyright__  = "Copyright 2016-2017, Veronica Berglyd Olsen"
__credits__    = ["Veronica Berglyd Olsen"]
__license__    = "GPLv3"
__version__    = "0.4.0"
__date__       = "2017"
__maintainer__ = "Veronica Berglyd Olsen"
__email__      = "code@jadzia626.net"
__status__     = "Development"

# ================================================================================================ #
# Begin Initialisation

logger.basicConfig(
    format  = "[%(asctime)s] %(levelname)s: %(message)s",
    level   = logger.DEBUG,
    datefmt = "%H:%M:%S",
)

# Global Classes
CONFIG  = Config()
BUILDER = Gtk.Builder()

BUILDER.add_from_file(path.join(CONFIG.guiPath,"novelWriter.glade"))
CONFIG.setBuilder(BUILDER)
CONFIG.updateRecentList()

# End Initialisation
# ================================================================================================ #
# Begin Global Constant

# Date Formats
DATE_NUM1 = 0
DATE_NUM2 = 1
DATE_TIME = 2
DATE_DATE = 3
DATE_FULL = 4

# Tab Indices
MAIN_DETAILS = 0
MAIN_EDITOR  = 1
MAIN_SOURCE  = 2

# Scene Index Columns
SCIDX_TITLE   = 0
SCIDX_NUMBER  = 1
SCIDX_WORDS   = 2
SCIDX_SECTION = 3
SCIDX_CHAPTER = 4
SCIDX_TIME    = 5
SCIDX_COUNT   = 6

# Scene Sections
SCN_NONE = 0
SCN_PRO  = 1
SCN_CHAP = 2
SCN_EPI  = 3
SCN_ARCH = 4

# Word or Char Count
COUNT_ONLOAD = 0
COUNT_ADDED  = 1
COUNT_LATEST = 2

# Actions
ACTION_NONE   = 0
ACTION_CANCEL = 1
ACTION_LOAD   = 2
ACTION_SAVE   = 3
ACTION_EDIT   = 4
ACTION_NEW    = 5

# Editor Paste Type
PASTE_PLAIN = 0
PASTE_CLEAN = 1

# StatusBar LED Colours
LED_GREY   = "icon-grey"
LED_GREEN  = "icon-green"
LED_YELLOW = "icon-yellow"
LED_RED    = "icon-red"
LED_BLUE   = "icon-blue"

# End Global Constants
# ================================================================================================ #
