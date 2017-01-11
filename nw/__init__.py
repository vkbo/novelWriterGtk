# -*- coding: utf-8 -*

##
#  novelWriter – Init File
# ~~~~~~~~~~~~~~~~~~~~~~~~~
#  Application initialisation
##

import logging as logger

import gi
gi.require_version("Gtk","3.0")

from gi.repository import Gtk
from os            import path
from nw.config     import Config

logger.basicConfig(format="%(levelname)s: %(message)s",level=logger.DEBUG)

# Global Classes
CONFIG  = Config()
BUILDER = Gtk.Builder()

BUILDER.add_from_file(path.join(CONFIG.guiPath,"novelWriter.glade"))
BUILDER.add_from_file(path.join(CONFIG.guiPath,"dlgEditBook.glade"))

# End novelWriter Initialisation
