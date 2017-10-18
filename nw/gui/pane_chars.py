# -*- coding: utf-8 -*
"""novelWriter GUI Characters Pane

 novelWriter – GUI Characters Pane
===================================
 Main wrapper class for the GUI characters editor

 File History:
 Created: 2017-10-08 [0.4.0]

"""

import logging
import nw
import gi
gi.require_version("Gtk","3.0")

from gi.repository     import Gtk, Pango
from os                import path
from nw.gui.tree_chars import GuiCharsTree

logger = logging.getLogger(__name__)

class GuiCharsPane(Gtk.Alignment):
    
    def __init__(self, theBook):
        
        Gtk.Alignment.__init__(self)
        
        self.theBook = theBook
        
        # Book Alignment
        self.set_name("alignBook")
        self.set_padding(40,40,40,40)
        
        # Main Vertical Box
        self.boxChars = Gtk.Box()
        self.boxChars.set_name("boxChars")
        self.boxChars.set_orientation(Gtk.Orientation.VERTICAL)
        self.boxChars.set_spacing(8)
        self.add(self.boxChars)
        
        # Top Horisontal Box
        self.boxTop = Gtk.Box()
        self.boxTop.set_name("boxCharsTop")
        self.boxTop.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.boxTop.set_spacing(100)
        self.boxChars.pack_start(self.boxTop,False,False,0)
        
        # Top Title
        self.lblChars = Gtk.Label()
        self.lblChars.set_name("lblChars")
        self.lblChars.set_label("Characters")
        self.lblChars.set_xalign(0.0)
        self.lblChars.set_yalign(0.0)
        self.boxTop.pack_start(self.lblChars,True,True,0)
        
        # Characters ToolBar
        self.tbChars = Gtk.Toolbar()
        self.tbChars.set_name("tbChars")
        self.tbChars.set_icon_size(2)
        self.tbChars.set_halign(Gtk.Align.START)
        self.btnCharsAdd = Gtk.ToolButton()
        self.btnCharsDel = Gtk.ToolButton()
        self.btnCharsAdd.set_label("Add")
        self.btnCharsDel.set_label("Remove")
        self.btnCharsAdd.set_homogeneous(False)
        self.btnCharsDel.set_homogeneous(False)
        self.tbChars.insert(self.btnCharsAdd,0)
        self.tbChars.insert(self.btnCharsDel,1)
        self.boxChars.pack_start(self.tbChars,False,True,0)
        
        # Characters Tree
        self.treeChars = GuiCharsTree(self.theBook)
        self.boxChars.pack_start(self.treeChars,True,True,0)
        
        return
    
# End Class GuiCharsPane
