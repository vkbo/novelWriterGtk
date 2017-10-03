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
from nw.gui.editor   import GuiEditor
from nw.gui.maintree import GuiMainTree

logger = logging.getLogger(__name__)

class GuiWinMain(Gtk.ApplicationWindow):
    
    def __init__(self):
        Gtk.ApplicationWindow.__init__(self, title="Hello World")
        
        self.mainConf = nw.CONFIG
        # self.connect("delete-event",self.onWindowsDestroy)

        # The outer vertical box
        # - Added to main window
        self.boxOuter = Gtk.Box()
        self.boxOuter.set_name("boxOuter")
        self.boxOuter.set_orientation(Gtk.Orientation.VERTICAL)
        self.boxOuter.set_spacing = 0
        self.add(self.boxOuter)

        # Pane between tree view and main content
        # - Added to outer box
        self.panedOuter = Gtk.Paned()
        self.panedOuter.set_name("panedOuter")
        self.panedOuter.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.panedOuter.set_position(300)
        # self.panedOuter.set_wide_handle(True)
        self.boxOuter.pack_start(self.panedOuter,True,True,0)

        # Vertical box to hold tree view and buttons
        # - Added to left outer pane
        self.boxLeft = Gtk.Box()
        self.boxLeft.set_name("boxLeft")
        self.boxLeft.set_orientation(Gtk.Orientation.VERTICAL)
        self.boxLeft.set_spacing(0)
        self.panedOuter.pack1(self.boxLeft,True,False)
        
        # The main tree view
        # - Added to left vertical box
        # - Tree store is not added here, just the container.
        self.treeLeft = Gtk.TreeView()
        self.treeLeft.set_name("treeLeft")
        self.treeLeft.set_margin_top(12)
        self.treeLeft.set_margin_bottom(4)
        self.treeLeft.set_margin_left(12)
        self.treeLeft.set_margin_right(12)
        self.boxLeft.pack_start(self.treeLeft,True,True,0)
        self.mainTree = GuiMainTree(self.treeLeft)
        
        # Tree view toolbar
        self.tbLeft = Gtk.Toolbar()
        self.tbLeft.set_icon_size(2)
        self.tbLeft.set_margin_top(4)
        self.tbLeft.set_margin_bottom(12)
        self.tbLeft.set_margin_left(12)
        self.tbLeft.set_margin_right(12)
        self.btnLeftAddCont = Gtk.ToolButton(icon_name="gtk-directory")
        self.tbLeft.insert(self.btnLeftAddCont,0)
        self.boxLeft.pack_start(self.tbLeft,False,True,0)

        # Pane between main content and timeline
        # - Added to right pane of panedOuter
        self.panedContent = Gtk.Paned()
        self.panedContent.set_name("panedContent")
        self.panedContent.set_orientation(Gtk.Orientation.VERTICAL)
        self.panedContent.set_position(600)
        self.panedOuter.pack2(self.panedContent,True,True)
        
        
        self.scrlContent = Gtk.ScrolledWindow()
        self.scrlContent.set_name("scrlContent")
        self.panedContent.pack1(self.scrlContent,True,False)
        
        self.webEditor = GuiEditor()
        self.scrlContent.add(self.webEditor)
        
        self.scrlTimeLine = Gtk.ScrolledWindow()
        self.scrlTimeLine.set_name("scrlTimeLine")
        self.panedContent.pack2(self.scrlTimeLine,True,False)

        # self.btnTest = Gtk.Button(label="Test")
        # self.boxOuter.pack_start(self.btnTest,False,True,0)
        
        self.set_title(self.mainConf.appName)
        self.resize(self.mainConf.winWidth,self.mainConf.winHeight)
        self.set_position(Gtk.WindowPosition.CENTER)
        # self.set_css_name("winMain")

        self.show_all()
        
        return

    def onWindowsDestroy(self, guiObject, guiStuff):

        logger.info("Beginning shutdown procedure")

        logger.info("Exiting")
        Gtk.main_quit()

        return

# End Class GUIwinMain
