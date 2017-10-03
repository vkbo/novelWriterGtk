# -*- coding: utf-8 -*
"""novelWriter Main Class

novelWriter – Main Class
============================
Sets up the main GUI and holds action and event functions

File History:
Created:   2017-01-10 [0.1.0]
Rewrittem: 2017-10-03 [0.4.0]

"""

import logging
import nw
import gi
gi.require_version("Gtk","3.0")

from gi.repository   import Gtk, GLib
from time            import sleep
from os              import path

from nw.gui.winmain  import GUIwinMain

logger  = logging.getLogger(__name__)

class NovelWriter():

    def __init__(self):

        self.guiLoaded    = False

        # Define Core Objects
        self.mainConf     = nw.CONFIG

        # Build the GUI
        logger.debug("Assembling the main GUI")
        self.winMain      = GUIwinMain()
        
        # Set Up Event Handlers
        self.winMain.connect("delete-event",self.onApplicationQuit)

        self.guiLoaded = True

        return


    ##
    #  Event Handlers
    ##

    def onApplicationQuit(self, guiObject, guiEvent):

        logger.info("Beginning shutdown procedure")

        logger.info("Exiting")
        Gtk.main_quit()

        return

# End Class NovelWriter
