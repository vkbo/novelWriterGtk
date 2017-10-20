# -*- coding: utf-8 -*
"""novelWriter Characters Tree Class

 novelWriter – Characters Tree Class
=====================================
 Wrapper class for the characters tree

 File History:
 Created: 2017-10-08 [0.4.0]

"""

import logging
import nw
import gi
gi.require_version("Gtk","3.0")

from gi.repository import Gtk

logger = logging.getLogger(__name__)

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
        self.listStore  = Gtk.ListStore(str,str,str,str,str)
        self.set_model(self.listStore)
        
        # Title Column
        self.colName  = Gtk.TreeViewColumn(title="Character Name")
        self.rendName = Gtk.CellRendererText()
        self.rendName.set_property("editable",True)
        self.colName.pack_start(self.rendName,True)
        self.colName.add_attribute(self.rendName,"text",0)
        self.colName.set_attributes(self.rendName,markup=0)
        
        # Importance
        self.colImport  = Gtk.TreeViewColumn(title="Importance")
        self.rendImport = Gtk.CellRendererText()
        self.rendImport.set_property("editable",True)
        self.colImport.pack_start(self.rendImport,False)
        self.colImport.add_attribute(self.rendImport,"text",1)
        
        # Role
        self.colRole  = Gtk.TreeViewColumn(title="Role")
        self.rendRole = Gtk.CellRendererText()
        self.rendRole.set_property("editable",True)
        self.colRole.pack_start(self.rendRole,False)
        self.colRole.add_attribute(self.rendRole,"text",2)

        # Comment
        self.colComment  = Gtk.TreeViewColumn(title="Comment")
        self.rendComment = Gtk.CellRendererText()
        self.rendComment.set_property("editable",True)
        self.colComment.pack_start(self.rendComment,False)
        self.colComment.add_attribute(self.rendComment,"text",3)
        
        # Add to TreeView
        self.append_column(self.colName)
        self.append_column(self.colImport)
        self.append_column(self.colRole)
        self.append_column(self.colComment)
        
        return
    
    def loadContent(self):
        
        self.treeSelect.set_mode(Gtk.SelectionMode.NONE)
        self.listStore.clear()
        
        for treeHandle in self.theBook.theTree.fullOrder:
            
            treeItem   = self.theBook.getItem(treeHandle)
            
            itemHandle = treeItem["handle"]
            itemParent = treeItem["parent"]
            
            itemName   = treeItem["entry"].itemName
            itemClass  = treeItem["entry"].itemClass
            itemLevel  = treeItem["entry"].itemLevel
            itemType   = treeItem["entry"].itemType
            
            if not itemClass == "CONTAINER": continue
            if not itemLevel == "ITEM":      continue
            if not itemType  == "CHAR":      continue
            
            itemImportance = str(treeItem["entry"].itemImportance)
            itemRole       = treeItem["entry"].itemRole
            itemComment    = treeItem["entry"].itemComment
            
            tmpIter = self.listStore.append([
                itemName,
                itemImportance,
                itemRole,
                itemComment,
                itemHandle
            ])
            self.iterMap[itemHandle] = tmpIter
        
        self.expand_all()
        self.treeSelect.set_mode(Gtk.SelectionMode.SINGLE)
        
        return
    
# End Class GuiCharsTree
