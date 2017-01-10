# -*- coding: utf-8 -*

##
#  novelWriter – Main GUI Class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Sets up the main GUI and holds action and event functions
##

import logging as logger

import gi
gi.require_version("Gtk","3.0")

from gi.repository import Gtk
from os            import path
from nw            import *

class GUI():

    def __init__(self):

        self.guiLoaded  = False

        # Define Core Objects
        self.mainConf   = CONFIG
        self.guiBuilder = BUILDER
        self.guiBuilder.add_from_file(path.join(self.mainConf.guiPath,"novelWriter.glade"))

        self.getObject  = self.guiBuilder.get_object
        self.winMain    = self.getObject("winMain")

        # Set Up Event Handlers
        guiHandlers = {
            "onDestroyWindow" : self.onGuiDestroy,
        }
        self.guiBuilder.connect_signals(guiHandlers)

        # Prepare Main Window
        self.winMain.set_title(self.mainConf.appName)
        self.winMain.resize(self.mainConf.winWidth,self.mainConf.winHeight)
        self.winMain.set_position(Gtk.WindowPosition.CENTER)
        self.winMain.show_all()

        self.guiLoaded = True

        return

    # Close Program
    def onGuiDestroy(self, guiObject):
        logger.debug("Exiting")
        Gtk.main_quit()
        return

# End Class GUI
