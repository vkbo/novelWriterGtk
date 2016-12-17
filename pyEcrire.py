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
from gi.repository import Gtk

import pyecrire
from pyecrire.gui import GUI

if __name__ == "__main__":
    #win = GUI()
    #win.show_all()

    #guiBuilder = Gtk.Builder()
    #guiBuilder.add_from_file("pyecrire/gui.glade")
    #builder.connect_signals(Handler())

    mainWin = GUI()
    #mainWin = GUI(guiBuilder.get_object("mainWin"))
    #mainWin.show_all()
    #mainWin.connect("destroy", Gtk.main_quit)
    #mainWin.resize(1000,700)

    Gtk.main()
