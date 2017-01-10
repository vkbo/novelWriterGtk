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

logger.basicConfig(format="%(levelname)s: %(message)s",level=logger.DEBUG)

# Global Classes
#CONFIG  = Config()
BUILDER = Gtk.Builder()

# End novelWriter Initialisation
