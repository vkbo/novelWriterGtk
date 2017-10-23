# -*- coding: utf-8 -*
"""novelWriter Main Tree Class

 novelWriter – Main Tree Class
===============================
 Wrapper class for the tree in the main GUI

 File History:
 Created: 2017-10-03 [0.4.0]

"""

import logging
import nw
import gi
gi.require_version("Gtk","3.0")

from gi.repository import Gtk, Pango
from nw.file.item  import BookItem

logger = logging.getLogger(__name__)

class GuiMainTree(Gtk.TreeView):
    
    # Constants
    COL_TITLE  = 0
    COL_NUMBER = 1
    COL_WORDS  = 2
    COL_NAME   = 3
    COL_HANDLE = 4
    
    def __init__(self, theBook):
        
        Gtk.TreeView.__init__(self)
        
        # Connect to GUI
        self.mainConf = nw.CONFIG
        self.theBook  = theBook
        self.iterMap  = {}
        
        self.set_name("treeLeft")
        self.set_margin_top(40)
        self.set_margin_bottom(4)
        self.set_margin_left(12)
        self.set_margin_right(12)
        self.set_headers_visible(False)
        
        # Core objects
        self.treeSelect = self.get_selection()
        self.treeStore  = Gtk.TreeStore(str,str,str,str,str)
        self.set_model(self.treeStore)
        
        # Title
        self.colTitle  = Gtk.TreeViewColumn(title="Title")
        self.rendTitle = Gtk.CellRendererText()
        self.rendTitle.set_property("ellipsize",Pango.EllipsizeMode.END)
        self.colTitle.set_expand(True)
        self.colTitle.pack_start(self.rendTitle,True)
        self.colTitle.add_attribute(self.rendTitle,"text",0)
        self.colTitle.set_attributes(self.rendTitle,markup=0)
        
        # File Number
        self.colNumber  = Gtk.TreeViewColumn(title="Count")
        self.rendNumber = Gtk.CellRendererText()
        # self.colNumber.pack_start(self.rendNumber,False)
        # self.colNumber.add_attribute(self.rendNumber,"text",1)
        
        # Word Count
        self.colWords  = Gtk.TreeViewColumn(title="Words")
        self.rendWords = Gtk.CellRendererText()
        self.rendWords.set_alignment(1.0,1.0)
        self.colWords.pack_start(self.rendWords,False)
        self.colWords.add_attribute(self.rendWords,"text",2)
        self.colWords.set_attributes(self.rendWords,markup=2)
        
        # Add to TreeView
        self.append_column(self.colTitle)
        self.append_column(self.colNumber)
        self.append_column(self.colWords)
        
        #
        # Context Menu
        #
        
        self.menuContext = Gtk.Menu()
        menuItem = Gtk.MenuItem("Add Scene File")
        self.menuContext.append(menuItem)
        self.menuItemMoveScene = Gtk.MenuItem("Move Scene to")
        self.menuContext.append(self.menuItemMoveScene)
        # menuItem.show()
        
        return
    
    def loadContent(self):
        
        logger.debug("Loading main tree content")
        
        # Store currently selected item
        selHandle = None
        listModel, pathList = self.treeSelect.get_selected_rows()
        for pathItem in pathList:
            listIter  = listModel.get_iter(pathItem)
            selHandle = listModel.get_value(listIter,self.COL_HANDLE)
        
        # Make unselectable and clear
        self.treeSelect.set_mode(Gtk.SelectionMode.NONE)
        self.treeStore.clear()
        
        for treeHandle in self.theBook.theTree.treeOrder:
            
            treeItem   = self.theBook.getItem(treeHandle)
            
            itemHandle = treeItem["handle"]
            itemParent = treeItem["parent"]
            
            itemName   = treeItem["entry"].itemName
            itemLevel  = treeItem["entry"].itemLevel
            itemClass  = treeItem["entry"].itemClass
            
            logger.vverbose("Adding %s '%s'" % (itemLevel,itemName))
            
            wordCount  = treeItem["entry"].metaWordCount
            
            if itemParent is None:
                parIter = None
            else:
                if itemParent in self.iterMap:
                    parIter = self.iterMap[itemParent]
                else:
                    logger.error("Item encountered before its parent")
                    parIter = None
            
            if itemClass == BookItem.CLS_CONT:
                itemTitle = "<b>%s</b>" % itemName
            else:
                itemTitle = itemName
            
            if itemLevel == BookItem.LEV_FILE:
                if wordCount is None:
                    wordCount = "<i>0</i>"
                else:
                    wordCount = "<i>%s</i>" % str(wordCount)
            else:
                wordCount = None
            
            treeEntry = [itemTitle,"0",wordCount,itemName,itemHandle]
            tmpIter   = self.treeStore.append(parIter,treeEntry)
            self.iterMap[itemHandle] = tmpIter
        
        # Expand all nodes, and reactivate
        # TODO: Should restore previous expanded state, or update tree rater than repopulate
        self.expand_all()
        self.treeSelect.set_mode(Gtk.SelectionMode.SINGLE)
        
        # Restore selected item state
        if selHandle is not None:
            newIter = self.getIter(selHandle)
            self.treeSelect.select_iter(newIter)
        
        return
    
    def getIter(self, itemHandle):
        return self.iterMap[itemHandle]
    
# End Class GuiMainTree
