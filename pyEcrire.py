#!/usr/bin/env python
# -*- coding: utf-8 -*

##
#  pyÉcrire
# ==========
#
#  Simple text editor for structuring and writing novels
#
#  By: Veronica Berglyd Olsen
##

__version__ = "0.1"
__author__  = "Veronica Berglyd Olsen"

import logging as logger

import gi
gi.require_version('Gtk', '3.0')
from gi.repository      import Gtk

# pyÉcrire classes
from pyecrire.functions import *
from pyecrire.gui       import GUI
from pyecrire.config    import Config

def main():

    # Set up logging and level
    logger.basicConfig(format="%(levelname)s: %(message)s",level=logger.DEBUG)

    # Set up main window
    mainConf = Config()
    mainWin  = GUI(mainConf)

    # Run main gtk loop
    Gtk.main()

if __name__ == "__main__":
    main()

# End Main File
