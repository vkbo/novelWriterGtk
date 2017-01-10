#!/usr/bin/env python3
# -*- coding: utf-8 -*

##
#  novelWriter
# =============
#  Simple text editor for structuring and writing novels
#  By: Veronica Berglyd Olsen
##

__version__ = "0.1"
__author__  = "Veronica Berglyd Olsen"

import gi
gi.require_version("Gtk","3.0")

from gi.repository import Gtk
from nw.gui        import GUI

if __name__ == "__main__":
    novelWriter = GUI()
    Gtk.main()

# End Main File
