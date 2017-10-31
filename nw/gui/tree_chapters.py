# -*- coding: utf-8 -*
"""novelWriter Chapters Tree Class

 novelWriter – Chapters Tree Class
===================================
 Wrapper class for the chapters tree

 File History:
 Created: 2017-10-09 [0.4.0]

"""

import logging
import nw
import gi
gi.require_version("Gtk","3.0")

from gi.repository import Gtk
from nw.file.book  import BookItem

logger = logging.getLogger(__name__)

class GuiChaptersTree(Gtk.TreeView):
    
    # Constants
    COL_TYPE       = 0
    COL_NUMBER     = 1
    COL_TITLE      = 2
    COL_COMPILE    = 3
    COL_COMMENT    = 4
    COL_HANDLE     = 5
    
    def __init__(self, theBook):
        
        Gtk.TreeView.__init__(self)
        logger.verbose("GUI: Building chapter tree")
        
        # Connect to GUI
        self.mainConf = nw.CONFIG
        self.theBook  = theBook
        self.iterMap  = {}
        
        self.set_name("treeChapters")
        self.set_headers_visible(True)
        
        # Core Objects
        self.treeSelect = self.get_selection()
        self.listStore  = Gtk.ListStore(str,int,str,bool,str,str)
        self.set_model(self.listStore)
        
        # Type
        self.colType  = Gtk.TreeViewColumn(title="Type")
        self.listType = Gtk.ListStore(str)
        for subType in BookItem.validSubTypes:
            self.listType.append([subType])
        self.rendType = Gtk.CellRendererCombo()
        self.rendType.set_property("model",self.listType)
        self.rendType.set_property("editable",True)
        self.rendType.set_property("has-entry",False)
        self.rendType.set_property("text-column",0)
        self.colType.pack_start(self.rendType,True)
        self.colType.add_attribute(self.rendType,"text",0)
        
        # Number
        self.colNumber  = Gtk.TreeViewColumn(title="#")
        self.rendNumber = Gtk.CellRendererText()
        self.rendNumber.set_property("editable",True)
        self.colNumber.pack_start(self.rendNumber,False)
        self.colNumber.add_attribute(self.rendNumber,"text",1)
        
        # Title
        self.colTitle  = Gtk.TreeViewColumn(title="Title")
        self.rendTitle = Gtk.CellRendererText()
        self.rendTitle.set_property("editable",True)
        self.colTitle.pack_start(self.rendTitle,False)
        self.colTitle.add_attribute(self.rendTitle,"text",2)
        
        # Compile
        self.colCompile  = Gtk.TreeViewColumn(title="Compile")
        self.rendCompile = Gtk.CellRendererToggle()
        self.rendCompile.set_radio(False)
        self.rendCompile.set_activatable(True)
        self.colCompile.pack_start(self.rendCompile,False)
        self.colCompile.add_attribute(self.rendCompile,"active",3)
        
        # Comment
        self.colComment  = Gtk.TreeViewColumn(title="Comment")
        self.rendComment = Gtk.CellRendererText()
        self.rendComment.set_property("editable",True)
        self.colComment.pack_start(self.rendComment,False)
        self.colComment.add_attribute(self.rendComment,"text",4)
        
        # Add to TreeView
        self.append_column(self.colType)
        self.append_column(self.colNumber)
        self.append_column(self.colTitle)
        self.append_column(self.colCompile)
        self.append_column(self.colComment)
        
        return
    
    def loadContent(self):
        
        logger.debug("GUI: Loading chapter tree content")
        
        # Store currently selected item
        selHandle = None
        listModel, pathList = self.treeSelect.get_selected_rows()
        for pathItem in pathList:
            listIter  = listModel.get_iter(pathItem)
            selHandle = listModel.get_value(listIter,self.COL_HANDLE)
        
        # Make unselectable and clear
        self.treeSelect.set_mode(Gtk.SelectionMode.NONE)
        self.listStore.clear()
        
        # Populate tree
        for treeHandle in self.theBook.theTree.treeOrder:
            
            treeItem    = self.theBook.getItem(treeHandle)
            
            itemHandle  = treeItem["handle"]
            itemParent  = treeItem["parent"]

            itemName    = treeItem["entry"].itemName
            itemClass   = treeItem["entry"].itemClass
            itemLevel   = treeItem["entry"].itemLevel
            itemType    = treeItem["entry"].itemType
            
            if not itemClass == "CONTAINER": continue
            if not itemLevel == "ITEM":      continue
            if not itemType  == "BOOK":      continue
            
            logger.vverbose("GUI: Adding %s '%s'" % (itemLevel,itemName))
            
            itemSubType = treeItem["entry"].itemSubType
            itemNumber  = treeItem["entry"].itemNumber
            itemCompile = treeItem["entry"].itemCompile
            itemComment = treeItem["entry"].itemComment
            
            tmpIter = self.listStore.append([
                itemSubType,
                itemNumber,
                itemName,
                itemCompile,
                itemComment,
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
