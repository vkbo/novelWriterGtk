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
import gi
gi.require_version("Gtk","3.0")

from gi.repository import Gtk

class GuiMainTree(Gtk.TreeView):

    # Constants
    COL_TITLE  = 0
    COL_NUMBER = 1
    COL_WORDS  = 2
    COL_SORT   = 3
    
    ROOT_BOOK  = 0
    ROOT_CHARS = 1
    ROOT_PLOTS = 3
    ROOT_NOTES = 4

    def __init__(self):
        
        Gtk.TreeView.__init__(self)

        # Connect to GUI
        self.mainConf   = nw.CONFIG
        self.iterMap    = {}

        self.set_name("treeLeft")
        self.set_margin_top(40)
        self.set_margin_bottom(4)
        self.set_margin_left(12)
        self.set_margin_right(12)
        self.set_headers_visible(False)

        # Core objects
        self.treeSelect = self.get_selection()
        self.treeStore  = Gtk.TreeStore(str,str,str,str)
        self.treeSort   = Gtk.TreeModelSort(model=self.treeStore)

        # Data Sorting
        self.treeSort.set_sort_column_id(3,Gtk.SortType.ASCENDING)
        self.set_model(self.treeSort)
        
        # Columns

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

        # Sorting
        self.colSort   = Gtk.TreeViewColumn()

        # Add to TreeView
        self.append_column(self.colTitle)
        self.append_column(self.colNumber)
        self.append_column(self.colWords)
        self.append_column(self.colSort)





        # Enable to Show Sorting
        # if debugShowSort:
        #     cellCol3 = Gtk.CellRendererText()
        #     treeCol3 = self.treeView.get_column(3)
        #     treeCol3.set_visible(True)
        #     treeCol3.pack_start(cellCol3,False)
        #     treeCol3.add_attribute(cellCol3,"text",3)
        
        self.loadContent()

        return

    def loadContent(self):

        self.treeSelect.set_mode(Gtk.SelectionMode.NONE)
        self.treeStore.clear()

        tmpIter = self.treeStore.append(None,["<b>Book</b>","1","[0]","Stuff"])
        tmpIter = self.treeStore.append(tmpIter,["Prologue","1","[0]","Stuff"])
        tmpIter = self.treeStore.append(tmpIter,["Scene 1","","[0]","Stuff"])
        tmpIter = self.treeStore.append(None,["<b>Characters</b>","0","[0]","Stuff"])
        tmpIter = self.treeStore.append(None,["<b>Plots</b>","0","[0]","Stuff"])
        tmpIter = self.treeStore.append(None,["<b>Notes</b>","0","[0]","Stuff"])

        self.expand_all()
        self.treeSelect.set_mode(Gtk.SelectionMode.SINGLE)

        return

# End Class GuiMainTree
