# -*- coding: utf-8 -*
"""novelWriter Characters Tree Class

 novelWriter – Characters Tree Class
=====================================
 Wrapper class for the characters tree

 File History:
 Created: 2017-10-08 [0.4.0]

"""

import logging as logger
import nw
import nw.const as NWC
import gi
gi.require_version("Gtk","3.0")

from gi.repository import Gtk

class GuiCharsTree(Gtk.TreeView):

    # Constants
    COL_TITLE      = 0
    COL_IMPORTANCE = 1
    COL_ROLE       = 2
    COL_COMMENT    = 3
    COL_HANDLE     = 4
    
    def __init__(self, theBook):
        
        Gtk.TreeView.__init__(self)
        
        # Connect to GUI
        self.mainConf   = nw.CONFIG
        self.theBook    = theBook
        self.iterMap    = {}
        
        self.set_name("treeChars")
        self.set_headers_visible(True)
        
        # Core Objects
        self.treeSelect = self.get_selection()
        self.treeStore  = Gtk.TreeStore(str,str,str,str,str)
        self.set_model(self.treeStore)
        
        # Title Column
        self.colTitle  = Gtk.TreeViewColumn(title="Character Name")
        self.rendTitle = Gtk.CellRendererText()
        self.colTitle.pack_start(self.rendTitle,True)
        self.colTitle.add_attribute(self.rendTitle,"text",0)
        self.colTitle.set_attributes(self.rendTitle,markup=0)
        
        # Importance
        self.colImport  = Gtk.TreeViewColumn(title="Importance")
        self.rendImport = Gtk.CellRendererText()
        self.colImport.pack_start(self.rendImport,False)
        self.colImport.add_attribute(self.rendImport,"text",1)
        
        # Role
        self.colRole  = Gtk.TreeViewColumn(title="Role")
        self.rendRole = Gtk.CellRendererText()
        self.colRole.pack_start(self.rendRole,False)
        self.colRole.add_attribute(self.rendRole,"text",2)

        # Comment
        self.colComment  = Gtk.TreeViewColumn(title="Comment")
        self.rendComment = Gtk.CellRendererText()
        self.colComment.pack_start(self.rendComment,False)
        self.colComment.add_attribute(self.rendComment,"text",3)
        
        # Add to TreeView
        self.append_column(self.colTitle)
        self.append_column(self.colImport)
        self.append_column(self.colRole)
        self.append_column(self.colComment)
        
        return
    
    def loadContent(self):
        
        self.treeSelect.set_mode(Gtk.SelectionMode.NONE)
        self.treeStore.clear()
        
        self.expand_all()
        self.treeSelect.set_mode(Gtk.SelectionMode.SINGLE)
        
        return
    
# End Class GuiCharsTree
