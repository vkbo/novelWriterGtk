# -*- coding: utf-8 -*

import logging as logger

import gi
gi.require_version('Gtk', '3.0')

from gi.repository     import Gtk
from pyecrire.datalist import DataList
from pyecrire.datawrapper import DataWrapper

class ProjectTree():

    def __init__(self, builder, config):

        """
        Tree Store Structure:
        Col 1 : String : Book title or universe title
        Col 2 : String : Book status
        Col 3 : String : List sorting column
        Col 4 : String : Book handle
        """

        # Connect to GUI
        self.guiBuilder = builder
        self.mainConf   = config
        self.getObject  = self.guiBuilder.get_object

        # Core objects
        self.treeView  = self.getObject("treeBooks")
        self.treeStore = Gtk.TreeStore(str,str,str,str)
        self.treeSort  = Gtk.TreeModelSort(model=self.treeStore)

        # Additional Lists for Combo Boxes
        self.listUnivs = Gtk.ListStore(str,str)
        self.listBooks = Gtk.ListStore(str,str)

        # Data Sorting
        self.treeSort.set_sort_column_id(2,Gtk.SortType.ASCENDING)
        self.treeView.set_model(self.treeSort)

        # Columns
        cellCol0 = Gtk.CellRendererText()
        cellCol1 = Gtk.CellRendererText()
        treeCol0 = self.treeView.get_column(0)
        treeCol1 = self.treeView.get_column(1)

        treeCol0.pack_start(cellCol0,True)
        treeCol1.pack_start(cellCol1,False)
        treeCol0.add_attribute(cellCol0,"text",0)
        treeCol1.add_attribute(cellCol1,"text",1)
        treeCol0.set_attributes(cellCol0,markup=0)

        # Data Maps and Lists
        self.allBooks = DataList(self.mainConf.dataPath,"Book")
        self.allUnivs = DataList(self.mainConf.dataPath,"Universe")

        self.iterMap = {}
        self.univMap = {}
        self.bookMap = {}

        return

    def loadContent(self):

        self.allBooks.makeList()
        self.allUnivs.makeList()
        self.iterMap = {}
        self.univMap = {}
        self.bookMap = {}

        tmpItem = DataWrapper("Universe")
        for itemHandle in self.allUnivs.dataList.keys():
            tmpItem.setDataPath(self.allUnivs.dataList[itemHandle])
            tmpItem.loadDetails()

            tmpIter = self.treeStore.append(None,["<b>"+tmpItem.title+"</b>",None,None,itemHandle])
            self.iterMap[itemHandle] = tmpIter

            tmpIter = self.listUnivs.append([tmpItem.title,itemHandle])
            self.univMap[itemHandle] = tmpIter

        tmpItem = DataWrapper("Book")
        for itemHandle in self.allBooks.dataList.keys():
            tmpItem.setDataPath(self.allBooks.dataList[itemHandle])
            tmpItem.loadDetails()

            if tmpItem.parent in self.iterMap:
                parIter = self.iterMap[tmpItem.parent]
            else:
                parIter = None

            tmpIter = self.treeStore.append(parIter,[tmpItem.title,None,None,itemHandle])
            self.iterMap[itemHandle] = tmpIter

            tmpIter = self.listBooks.append([tmpItem.title,itemHandle])
            self.bookMap[itemHandle] = tmpIter

        return

    def getPath(self, itemHandle):
        if itemHandle in self.allBooks.dataList: return self.allBooks.dataList[itemHandle]
        if itemHandle in self.allUnivs.dataList: return self.allUnivs.dataList[itemHandle]
        return None


# End Class ProjectTree
