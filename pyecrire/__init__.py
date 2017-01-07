# -*- coding: utf-8 -*

##
#  pyÉcrire – Init File
# ~~~~~~~~~~~~~~~~~~~~~~
#  Inits pyÉcrire and set program constants and core objects
##

import logging as logger

import gi
gi.require_version("Gtk","3.0")

from gi.repository   import Gtk
from pyecrire.config import Config

logger.basicConfig(format="%(levelname)s: %(message)s",level=logger.DEBUG)

# Global Classes
CONFIG    = Config()
BUILDER   = Gtk.Builder()

# Main name types
NAME_NONE = "None"
NAME_BOOK = "Book"
NAME_UNIV = "Universe"
NAME_PLOT = "Plot"
NAME_SCNE = "Scene"
NAME_HIST = "History"
NAME_CHAR = "Character"

# Name is container of file
TYPE_NONE = 0  # Unknown datatype
TYPE_CONT = 1  # Container, with files
TYPE_FILE = 2  # File

# Sort order of groups in tree views
GRP_PLOT  = 0
GRP_SCNE  = 1
GRP_HIST  = 0
GRP_CHAR  = 1

# Tab Numbers
TABS_PROJ = 0
TABS_BOOK = 1
TABS_UNIV = 2
TABM_BOOK = 0
TABM_UNIV = 1
TABM_EDIT = 2
TABM_SRCE = 3
