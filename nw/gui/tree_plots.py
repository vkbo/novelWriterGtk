# -*- coding: utf-8 -*
"""novelWriter Plots Tree Class

 novelWriter – Plots Tree Class
================================
 Wrapper class for the plots tree

 File History:
 Created: 2017-10-09 [0.4.0]

"""

import logging
import nw
import gi
gi.require_version("Gtk","3.0")

from gi.repository import Gtk
from nw.functions  import encodeString

logger = logging.getLogger(__name__)

class GuiPlotsTree(Gtk.TreeView):
    
    # Constants
    COL_TITLE      = 0
    COL_IMPORTANCE = 1
    COL_COMMENT    = 2
    COL_HANDLE     = 3
    
    def __init__(self, theBook):
        
        Gtk.TreeView.__init__(self)
        logger.verbose("GUI: Building plots tree")
        
        # Connect to GUI
        self.mainConf = nw.CONFIG
        self.theBook  = theBook
        self.iterMap  = {}
        
        self.set_name("treePlots")
        self.set_headers_visible(True)
        
        # Core Objects
        self.treeSelect = self.get_selection()
        self.listStore  = Gtk.ListStore(str,str,str,str)
        self.set_model(self.listStore)
        
        # Title Column
        self.colName  = Gtk.TreeViewColumn(title="Plot")
        self.rendName = Gtk.CellRendererText()
        self.rendName.set_property("editable",True)
        self.colName.pack_start(self.rendName,True)
        self.colName.add_attribute(self.rendName,"text",0)
        self.colName.set_attributes(self.rendName,markup=0)
        
        self.colImport  = Gtk.TreeViewColumn(title="Importance")
        self.listImport = Gtk.ListStore(str)
        self.listImport.append(["Main"])
        self.listImport.append(["Major"])
        self.listImport.append(["Minor"])
        self.rendImport = Gtk.CellRendererCombo()
        self.rendImport.set_property("model",self.listImport)
        self.rendImport.set_property("editable",True)
        self.rendImport.set_property("has-entry",False)
        self.rendImport.set_property("text-column",0)
        self.colImport.pack_start(self.rendImport,False)
        self.colImport.add_attribute(self.rendImport,"text",1)
        
        # Comment
        self.colComment  = Gtk.TreeViewColumn(title="Comment")
        self.rendComment = Gtk.CellRendererText()
        self.rendComment.set_property("editable",True)
        self.colComment.pack_start(self.rendComment,False)
        self.colComment.add_attribute(self.rendComment,"text",2)
        
        # Add to TreeView
        self.append_column(self.colName)
        self.append_column(self.colImport)
        self.append_column(self.colComment)
        
        return
    
    def loadContent(self):
        
        logger.debug("GUI: Loading plots tree content")
        
        # Store currently selected item
        selHandle = None
        listModel, pathList = self.treeSelect.get_selected_rows()
        for pathItem in pathList:
            listIter  = listModel.get_iter(pathItem)
            selHandle = listModel.get_value(listIter,self.COL_HANDLE)
        
        # Make unselectable and clear
        self.treeSelect.set_mode(Gtk.SelectionMode.NONE)
        self.listStore.clear()
        
        for treeHandle in self.theBook.theTree.treeOrder:
            
            treeItem   = self.theBook.getItem(treeHandle)
            
            itemHandle = treeItem["handle"]
            itemParent = treeItem["parent"]
            
            itemName   = treeItem["entry"].itemName
            itemClass  = treeItem["entry"].itemClass
            itemLevel  = treeItem["entry"].itemLevel
            itemType   = treeItem["entry"].itemType
            
            if not itemClass == "CONTAINER": continue
            if not itemLevel == "ITEM":      continue
            if not itemType  == "PLOT":      continue
            
            logger.vverbose("GUI: Adding %s '%s'" % (itemLevel,itemName))
            
            itemImportance = str(treeItem["entry"].itemImportance)
            itemComment    = treeItem["entry"].itemComment
            
            tmpIter = self.listStore.append([
                encodeString(itemName),
                itemImportance,
                encodeString(itemComment),
                itemHandle
            ])
            self.iterMap[itemHandle] = tmpIter
        
        self.treeSelect.set_mode(Gtk.SelectionMode.SINGLE)
        
        # Restore selected item state
        if selHandle is not None:
            newIter = self.getIter(selHandle)
            self.treeSelect.select_iter(newIter)
        
        return
    
    def getIter(self, itemHandle):
        return self.iterMap[itemHandle]
    
# End Class GuiCharsTree
