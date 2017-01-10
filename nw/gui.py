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
from nw.editor     import Editor

class GUI():

    def __init__(self):

        self.guiLoaded  = False

        # Define Core Objects
        self.mainConf   = CONFIG
        self.guiBuilder = BUILDER
        self.guiBuilder.add_from_file(path.join(self.mainConf.guiPath,"novelWriter.glade"))

        self.getObject  = self.guiBuilder.get_object
        self.winMain    = self.getObject("winMain")

        # Prepare GUI Classes
        self.guiTimer  = None #Timer()
        self.webEditor = Editor(self.guiTimer)

        # Set Up Event Handlers
        guiHandlers = {
            "onDestroyWindow" : self.onGuiDestroy, # Close Program
            "onMainWinChange" : self.onWinChange,  # Window Size Change
        }
        self.guiBuilder.connect_signals(guiHandlers)

        # Set Panes
        self.getObject("panedContent").set_position(self.mainConf.mainPane)
        self.getObject("panedSide").set_position(self.mainConf.mainPane)

        # Prepare Editor
        self.getObject("scrollEditor").add(self.webEditor)

        # Prepare Main Window
        self.winMain.set_title(self.mainConf.appName)
        self.winMain.resize(self.mainConf.winWidth,self.mainConf.winHeight)
        self.winMain.set_position(Gtk.WindowPosition.CENTER)
        self.winMain.show_all()

        self.guiLoaded = True

        return

    ##
    #  Main Window Events
    ##

    # Close Program
    def onGuiDestroy(self, guiObject):
        logger.debug("Exiting")
        mainPane = self.getObject("panedContent").get_position()
        sidePane = self.getObject("panedSide").get_position()
        self.mainConf.setMainPane(mainPane)
        self.mainConf.setSidePane(sidePane)
        self.mainConf.saveConfig()
        Gtk.main_quit()
        return

    def onWinChange(self, guiObject, guiEvent):
        self.mainConf.setWinSize(guiEvent.width,guiEvent.height)
        return

# End Class GUI
