# -*- coding: utf-8 -*
"""novelWriter Main Tree Class

 novelWriter – Main Tree Class
===============================
 Wrapper class for the tree in the main GUI

 File History:
 Created: 2017-10-03 [0.4.0]

"""

import logging as logger
import nw
import nw.const as NWC
import gi
gi.require_version("Gtk","3.0")

from gi.repository import Gtk

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
        self.mainConf   = nw.CONFIG
        self.theBook    = theBook
        self.iterMap    = {}
        
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
        self.colTitle   = Gtk.TreeViewColumn(title="Title")
        self.rendTitle  = Gtk.CellRendererText()
        self.colTitle.set_expand(True)
        self.colTitle.pack_start(self.rendTitle,True)
        self.colTitle.add_attribute(self.rendTitle,"text",0)
        self.colTitle.set_attributes(self.rendTitle,markup=0)
        
        # File Number
        self.colNumber  = Gtk.TreeViewColumn(title="Count")
        self.rendNumber = Gtk.CellRendererText()
        self.colNumber.pack_start(self.rendNumber,False)
        self.colNumber.add_attribute(self.rendNumber,"text",1)
        
        # Word Count
        self.colWords   = Gtk.TreeViewColumn(title="Words")
        self.rendWords  = Gtk.CellRendererText()
        self.colWords.pack_start(self.rendWords,False)
        self.colWords.add_attribute(self.rendWords,"text",2)
        self.colWords.set_attributes(self.rendWords,markup=2)
        
        # Add to TreeView
        self.append_column(self.colTitle)
        self.append_column(self.colNumber)
        self.append_column(self.colWords)
        
        return
    
    def loadContent(self):
        
        self.treeSelect.set_mode(Gtk.SelectionMode.NONE)
        self.treeStore.clear()
        
        for treeItem in self.theBook.theTree:
            
            itemName   = treeItem[NWC.BookTree.NAME]
            itemLevel  = treeItem[NWC.BookTree.LEVEL]
            itemHandle = treeItem[NWC.BookTree.HANDLE]
            itemParent = treeItem[NWC.BookTree.PARENT]
            
            if itemParent == None:
                parIter = None
            else:
                if itemParent in self.iterMap:
                    parIter = self.iterMap[itemParent]
                else:
                    logger.error("Item encountered before its parent")
                    parIter = None
            
            if itemLevel == NWC.ItemLevel.ROOT:
                itemTitle = "<b>%s</b>" % itemName
            else:
                itemTitle = itemName
            
            treeEntry = [itemTitle,"0","0",itemName,itemHandle]
            tmpIter   = self.treeStore.append(parIter,treeEntry)
            self.iterMap[itemHandle] = tmpIter
        
        self.expand_all()
        self.treeSelect.set_mode(Gtk.SelectionMode.SINGLE)
        
        return
    
# End Class GuiMainTree
