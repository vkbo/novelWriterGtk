# -*- coding: utf-8 -*
"""novelWriter GUI Book Pane

 novelWriter – GUI Book Pane
=================================
 Main wrapper class for the GUI book editor

 File History:
 Created: 2017-10-07 [0.4.0]

"""

import logging
import nw
import nw.const as NWC
import gi
gi.require_version("Gtk","3.0")

from gi.repository       import Gtk, Pango
from os                  import path
from nw.gui.chapterstree import GuiChaptersTree

logger = logging.getLogger(__name__)

class GuiBookPane(Gtk.Alignment):

    def __init__(self, theBook):

        Gtk.Alignment.__init__(self)
        
        self.theBook = theBook
        
        # Book Alignment
        self.set_name("alignBook")
        self.set_padding(40,40,40,40)
        
        # Main Vertical Box
        self.boxBook = Gtk.Box()
        self.boxBook.set_name("boxBook")
        self.boxBook.set_orientation(Gtk.Orientation.VERTICAL)
        self.boxBook.set_spacing(8)
        self.add(self.boxBook)
        
        # Top Horisontal Box
        self.boxTop = Gtk.Box()
        self.boxTop.set_name("boxBookTop")
        self.boxTop.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.boxTop.set_spacing(100)
        self.boxBook.pack_start(self.boxTop,False,False,0)

        # Top Title
        self.lblBook = Gtk.Label()
        self.lblBook.set_name("lblBook")
        self.lblBook.set_label("Book")
        self.lblBook.set_xalign(0.0)
        self.lblBook.set_yalign(0.0)
        self.boxTop.pack_start(self.lblBook,True,True,0)
        
        # Details Vertical Box
        self.boxDetails = Gtk.Box()
        self.boxDetails.set_name("boxBookDetails")
        self.boxDetails.set_orientation(Gtk.Orientation.VERTICAL)
        self.boxDetails.set_spacing(12)
        self.boxTop.add(self.boxDetails)
        
        # Details Book Title
        self.fmeBookTitle = Gtk.Frame()
        self.fmeBookTitle.set_name("fmeBookTitle")
        self.fmeBookTitle.set_label("Book Title")
        self.fmeBookTitle.set_shadow_type(Gtk.ShadowType.NONE)
        self.boxDetails.pack_start(self.fmeBookTitle,False,False,0)
        
        self.alignBookTitle = Gtk.Alignment()
        self.alignBookTitle.set_padding(2,2,12,4)
        self.alignBookTitle.set_size_request(600,-1)
        self.fmeBookTitle.add(self.alignBookTitle)
        
        self.entryBookTitle = Gtk.Entry()
        self.entryBookTitle.set_name("entryBookTitle")
        self.alignBookTitle.add(self.entryBookTitle)
        
        # Book Authors
        self.fmeBookAuthor = Gtk.Frame()
        self.fmeBookAuthor.set_name("fmeBookAuthor")
        self.fmeBookAuthor.set_label("Author(s)")
        self.fmeBookAuthor.set_shadow_type(Gtk.ShadowType.NONE)
        self.boxDetails.pack_start(self.fmeBookAuthor,False,False,0)
        
        self.alignBookAuthor = Gtk.Alignment()
        self.alignBookAuthor.set_padding(2,2,12,4)
        self.alignBookAuthor.set_size_request(600,-1)
        self.fmeBookAuthor.add(self.alignBookAuthor)
        
        self.entryBookAuthor = Gtk.Entry()
        self.entryBookAuthor.set_name("entryBookAuthor")
        self.alignBookAuthor.add(self.entryBookAuthor)
        
        # Chapters ToolBar
        self.tbChapters = Gtk.Toolbar()
        self.tbChapters.set_name("tbChapters")
        self.tbChapters.set_icon_size(2)
        self.tbChapters.set_halign(Gtk.Align.START)
        self.btnChaptersAdd    = Gtk.ToolButton()
        self.btnChaptersRemove = Gtk.ToolButton()
        self.btnChaptersAdd.set_label("Add")
        self.btnChaptersRemove.set_label("Remove")
        self.tbChapters.insert(self.btnChaptersAdd,0)
        self.tbChapters.insert(self.btnChaptersRemove,1)
        self.boxBook.pack_start(self.tbChapters,False,True,0)
        
        # Chapters Tree
        self.treeChapters = GuiChaptersTree(self.theBook)
        self.boxBook.pack_start(self.treeChapters,True,True,0)
        
        return

# End Class GuiBookPane
