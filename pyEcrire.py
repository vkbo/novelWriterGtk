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

import gi
gi.require_version('Gtk', '3.0')

from gi.repository   import Gtk

# pyÉcrire classes
from pyecrire.functions import *
from pyecrire.gui       import GUI
from pyecrire.config    import Config
from pyecrire.datastore import Universe

def main():

    mainWin      = GUI()
    mainConf     = Config()
    dataUniverse = Universe(mainConf)
    Gtk.main()

if __name__ == "__main__":
    main()
