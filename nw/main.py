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

from gi.repository   import Gtk, Gdk
from time            import sleep
from os              import path

from nw.gui.winmain  import GuiWinMain
from nw.file         import DataStore

logger  = logging.getLogger(__name__)

class NovelWriter():

    def __init__(self):
        
        # Define Core Objects
        self.mainConf = nw.CONFIG
        self.theBook  = DataStore()
        
        self.theBook.createBook()
        
        # Build the GUI
        logger.debug("Assembling the main GUI")
        self.winMain   = GuiWinMain()
        # self.webEditor = self.winMain.webEditor
        self.cssMain   = Gtk.CssProvider()
        
        # Load StyleSheet
        self.cssMain.load_from_path(
            path.join(self.mainConf.themePath,self.mainConf.theTheme,"gtkstyles.css")
        )
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),self.cssMain,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        
        # Set Up Event Handlers
        self.winMain.connect("delete-event",self.onApplicationQuit)
        
        
        self.winMain.treeLeft.treeSelect.connect("changed",self.onLeftTreeSelect)

        return


    ##
    #  Event Handlers
    ##
    
    def onLeftTreeSelect(self, guiObject):

        listModel, pathList = guiObject.get_selected_rows()
        for pathItem in pathList:
            listIter   = listModel.get_iter(pathItem)
            itemHandle = listModel.get_value(listIter,0)
            
            print(listIter)
            print(itemHandle)

        return

    def onApplicationQuit(self, guiObject, guiEvent):

        logger.info("Beginning shutdown procedure")

        logger.info("Exiting")
        Gtk.main_quit()

        return

# End Class NovelWriter
