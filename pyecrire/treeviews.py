# -*- coding: utf-8 -*

import logging as logger

import gi
gi.require_version('Gtk', '3.0')

from gi.repository        import Gtk
from pyecrire.datalist    import DataList
from pyecrire.datawrapper import DataWrapper
from pyecrire.functions   import makeSceneNumber

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


class BookTree():

    def __init__(self, builder, config):

        """
        Tree Store Structure:
        Col 1 : String  : Plot or scene title
        Col 2 : Integer : Word count
        Col 3 : String  : List sorting column
        Col 4 : String  : File handle
        """

        # Connect to GUI
        self.guiBuilder = builder
        self.mainConf   = config
        self.getObject  = self.guiBuilder.get_object

        # Core objects
        self.treeView  = self.getObject("treeMain")
        self.treeStore = Gtk.TreeStore(str,int,str,str)
        self.treeSort  = Gtk.TreeModelSort(model=self.treeStore)

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

        cellCol1.set_alignment(0.95,0.5)

        # Enable to Show Sorting
        cellCol2 = Gtk.CellRendererText()
        treeCol2 = self.treeView.get_column(2)
        treeCol2.set_visible(True)
        treeCol2.pack_start(cellCol2,False)
        treeCol2.add_attribute(cellCol2,"text",2)

        # Data Maps and Lists
        self.allScenes = DataList(self.mainConf.dataPath,"Scene")

        self.iterMap = {}
        self.chapMap = {}

        return

    def loadContent(self, bookHandle, bookPath):

        self.treeStore.clear()

        pltSort = makeSceneNumber(0,0,0,0)
        scnSort = makeSceneNumber(0,0,0,0)
        pltIter = self.treeStore.append(None,["<b>Plot</b>",0,pltSort,""])
        scnIter = self.treeStore.append(None,["<b>Scenes</b>",0,scnSort,""])

        if bookHandle == "" or bookHandle is None: return

        self.allScenes.setDataPath(bookPath)
        self.allScenes.makeList()

        self.iterMap = {}
        self.chapMap = {}

        tmpItem = DataWrapper("Scene")
        for itemHandle in self.allScenes.dataList.keys():
            tmpItem.setDataPath(self.allScenes.dataList[itemHandle])
            tmpItem.loadDetails()

            scnNum = makeSceneNumber(1,tmpItem.section,tmpItem.chapter,tmpItem.number)
            scnSec = makeSceneNumber(1,tmpItem.section,tmpItem.chapter,0)

            if tmpItem.section == 0:
                parIter = scnIter
            else:
                if scnSec in self.chapMap:
                    parIter = self.chapMap[scnSec]
                else:
                    if tmpItem.section == 1: scnChapter = "<b>Prologue</b>"
                    if tmpItem.section == 2: scnChapter = "<b>Chapter %d</b>" % tmpItem.chapter
                    if tmpItem.section == 3: scnChapter = "<b>Epilogue</b>"

                    parIter = self.treeStore.append(scnIter,[scnChapter,None,scnSec,None])
                    self.chapMap[scnSec] = parIter

            tmpIter = self.treeStore.append(parIter,[tmpItem.title,tmpItem.words,scnNum,itemHandle])
            self.chapMap[itemHandle] = tmpIter

        self.getObject("treeMain").expand_all()

        return

# End Class BookTree


class UniverseTree():

    def __init__(self, builder, config):

        """
        Tree Store Structure:
        Col 1 : String  : History or character title
        Col 2 : Integer : Word count
        Col 3 : String  : List sorting column
        Col 4 : String  : File handle
        """

        # Connect to GUI
        self.guiBuilder = builder
        self.mainConf   = config
        self.getObject  = self.guiBuilder.get_object

        # Core objects
        self.treeView  = self.getObject("treeUniverse")
        self.treeStore = Gtk.TreeStore(str,int,str,str)
        self.treeSort  = Gtk.TreeModelSort(model=self.treeStore)

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

        cellCol1.set_alignment(0.95,0.5)

        # Enable to Show Sorting
        cellCol2 = Gtk.CellRendererText()
        treeCol2 = self.treeView.get_column(2)
        treeCol2.set_visible(True)
        treeCol2.pack_start(cellCol2,False)
        treeCol2.add_attribute(cellCol2,"text",2)

        # Data Maps and Lists
        self.allChars = DataList(self.mainConf.dataPath,"Character")

        self.iterMap = {}

        return

    def loadContent(self, univHandle, univPath):

        self.treeStore.clear()

        pltSort = makeSceneNumber(0,0,0,0)
        scnSort = makeSceneNumber(0,0,0,0)
        pltIter = self.treeStore.append(None,["<b>History</b>",0,pltSort,""])
        scnIter = self.treeStore.append(None,["<b>Characters</b>",0,scnSort,""])

        if univHandle == "" or univHandle is None: return

        self.allChars.setDataPath(univPath)
        self.allChars.makeList()

        self.iterMap = {}

        return


# End Class UniverseTree