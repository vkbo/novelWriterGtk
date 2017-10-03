# -*- coding: utf-8 -*
"""novelWriter GUI Main Window

novelWriter – GUI Main Window
=============================
Class holding the main window

File History:
Created: 2017-10-03 [0.4.0]

"""

import logging
import nw
import gi
gi.require_version("Gtk","3.0")

from gi.repository   import Gtk, GLib

logger = logging.getLogger(__name__)

class GUIwinMain(Gtk.ApplicationWindow):
    
    def __init__(self):
        Gtk.ApplicationWindow.__init__(self, title="Hello World")
        
        self.mainConf = nw.CONFIG
        # self.connect("delete-event",self.onWindowsDestroy)
        
        self.set_title(self.mainConf.appName)
        self.resize(self.mainConf.winWidth,self.mainConf.winHeight)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.show_all()
        
        return

    def onWindowsDestroy(self, guiObject, guiStuff):

        logger.info("Beginning shutdown procedure")

        logger.info("Exiting")
        Gtk.main_quit()

        return

# End Class GUIwinMain
