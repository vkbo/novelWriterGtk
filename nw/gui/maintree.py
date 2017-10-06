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

class GuiMainTree():

    def __init__(self, treeView):

        # Constants
        self.COL_TITLE  = 0
        self.COL_NUMBER = 1
        self.COL_WORDS  = 2
        self.COL_SORT   = 3

        # Connect to GUI
        self.mainConf   = nw.CONFIG

        # Core objects
        self.treeView   = treeView
        self.treeSelect = Gtk.TreeSelection()
        self.treeStore  = Gtk.TreeStore(str,str,str,str)
        self.treeSort   = Gtk.TreeModelSort(model=self.treeStore)

        # Data Sorting
        self.treeSort.set_sort_column_id(3,Gtk.SortType.ASCENDING)
        self.treeView.set_model(self.treeSort)
        
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
        self.treeView.append_column(self.colTitle)
        self.treeView.append_column(self.colNumber)
        self.treeView.append_column(self.colWords)
        self.treeView.append_column(self.colSort)





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

        # self.treeSelect.set_mode(Gtk.SelectionMode.NONE)
        self.treeStore.clear()

        tmpIter = self.treeStore.append(None,["<b>Book</b>","0","[0]","Stuff"])
        tmpIter = self.treeStore.append(tmpIter,["Prologue","0.1","[0]","Stuff"])
        tmpIter = self.treeStore.append(None,["<b>Characters</b>","1","[0]","Stuff"])
        tmpIter = self.treeStore.append(None,["<b>Plots</b>","2","[0]","Stuff"])
        tmpIter = self.treeStore.append(None,["<b>Notes</b>","3","[0]","Stuff"])

        self.treeView.expand_all()
        # self.treeSelect.set_mode(Gtk.SelectionMode.SINGLE)

        return

# End Class GuiMainTree
