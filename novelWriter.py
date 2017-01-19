#!/usr/bin/env python3
# -*- coding: utf-8 -*

##
#  novelWriter – Version Dev0.4
# ==============================
#  Simple text editor for structuring and writing novels
#  By: Veronica Berglyd Olsen
##

import gi
gi.require_version("Gtk","3.0")

from gi.repository import Gtk
from nw.gui        import GUI

if __name__ == "__main__":
    GUI()
    Gtk.main()

# End Main File
