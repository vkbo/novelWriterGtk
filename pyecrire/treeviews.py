# -*- coding: utf-8 -*

##
#  pyÉcrire – Data Tree Classed
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Manages all the TreeViews of the GUI as well as lists for comboboxes
##

import logging as logger

import gi
gi.require_version('Gtk', '3.0')

from gi.repository        import Gtk
from pyecrire.constants   import *
from pyecrire.datalist    import DataList
from pyecrire.datawrapper import DataWrapper
from pyecrire.functions   import makeSceneNumber

# Set to true to show sorting in all treeviews
debugShowSort = True

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
        self.allBooks = DataList(self.mainConf.dataPath,NAME_BOOK)
        self.allUnivs = DataList(self.mainConf.dataPath,NAME_UNIV)

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

        tmpItem = DataWrapper(NAME_UNIV)
        for itemHandle in self.allUnivs.dataList.keys():
            tmpItem.setDataPath(self.allUnivs.dataList[itemHandle])
            tmpItem.loadDetails()

            tmpIter = self.treeStore.append(None,["<b>"+tmpItem.title+"</b>",None,None,itemHandle])
            self.iterMap[itemHandle] = tmpIter

            tmpIter = self.listUnivs.append([tmpItem.title,itemHandle])
            self.univMap[itemHandle] = tmpIter

        tmpItem = DataWrapper(NAME_BOOK)
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
        if debugShowSort:
            cellCol2 = Gtk.CellRendererText()
            treeCol2 = self.treeView.get_column(2)
            treeCol2.set_visible(True)
            treeCol2.pack_start(cellCol2,False)
            treeCol2.add_attribute(cellCol2,"text",2)

        # Data Maps and Lists
        self.allPlots  = DataList(self.mainConf.dataPath,NAME_PLOT)
        self.allScenes = DataList(self.mainConf.dataPath,NAME_SCNE)

        self.iterMap = {}
        self.chapMap = {}

        return

    def loadContent(self, bookPath):

        self.treeStore.clear()

        pltSort = makeSceneNumber(GRP_PLOT,0,0,0)
        scnSort = makeSceneNumber(GRP_SCNE,0,0,0)
        pltIter = self.treeStore.append(None,["<b>Plots</b>",0,pltSort,""])
        scnIter = self.treeStore.append(None,["<b>Scenes</b>",0,scnSort,""])

        if bookPath == "" or bookPath is None: return

        self.allScenes.setDataPath(bookPath)
        self.allScenes.makeList()

        self.iterMap = {}
        self.chapMap = {}

        tmpItem = DataWrapper(NAME_SCNE)
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

        self.treeView.expand_all()

        return

    def getPath(self, itemHandle):
        if itemHandle in self.allPlots.dataList:  return self.allPlots.dataList[itemHandle]
        if itemHandle in self.allScenes.dataList: return self.allScenes.dataList[itemHandle]
        return None

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
        if debugShowSort:
            cellCol2 = Gtk.CellRendererText()
            treeCol2 = self.treeView.get_column(2)
            treeCol2.set_visible(True)
            treeCol2.pack_start(cellCol2,False)
            treeCol2.add_attribute(cellCol2,"text",2)

        # Data Maps and Lists
        self.allHists = DataList(self.mainConf.dataPath,NAME_HIST)
        self.allChars = DataList(self.mainConf.dataPath,NAME_CHAR)

        self.iterMap = {}

        return

    def loadContent(self, univPath):

        self.treeStore.clear()

        pltSort = makeSceneNumber(GRP_HIST,0,0,0)
        scnSort = makeSceneNumber(GRP_CHAR,0,0,0)
        pltIter = self.treeStore.append(None,["<b>History</b>",0,pltSort,""])
        scnIter = self.treeStore.append(None,["<b>Characters</b>",0,scnSort,""])

        if univPath == "" or univPath is None: return

        self.allChars.setDataPath(univPath)
        self.allChars.makeList()

        self.iterMap = {}

        return

    def getPath(self, itemHandle):
        if itemHandle in self.allHists.dataList: return self.allHists.dataList[itemHandle]
        if itemHandle in self.allChars.dataList: return self.allChars.dataList[itemHandle]
        return None

# End Class UniverseTree


class SceneTree():

    def __init__(self, builder, config):

        """
        Tree Store Structure:
        Col 1 : String  : Scene title
        Col 2 : String  : Scene number
        Col 3 : String  : Point of view character
        Col 4 : Integer : Word count
        Col 5 : String  : List sorting column
        Col 5 : String  : File handle
        """

        # Connect to GUI
        self.guiBuilder = builder
        self.mainConf   = config
        self.getObject  = self.guiBuilder.get_object

        # Core objects
        self.treeView  = self.getObject("treeScenes")
        self.treeStore = Gtk.TreeStore(str,str,str,int,str,str)
        self.treeSort  = Gtk.TreeModelSort(model=self.treeStore)

        # Data Sorting
        self.treeSort.set_sort_column_id(4,Gtk.SortType.ASCENDING)
        self.treeView.set_model(self.treeSort)

        # Columns
        cellCol0 = Gtk.CellRendererText()
        cellCol1 = Gtk.CellRendererText()
        cellCol2 = Gtk.CellRendererText()
        cellCol3 = Gtk.CellRendererText()
        treeCol0 = self.treeView.get_column(0)
        treeCol1 = self.treeView.get_column(1)
        treeCol2 = self.treeView.get_column(2)
        treeCol3 = self.treeView.get_column(3)

        treeCol0.pack_start(cellCol0,True)
        treeCol1.pack_start(cellCol1,False)
        treeCol2.pack_start(cellCol2,False)
        treeCol3.pack_start(cellCol3,False)
        treeCol0.add_attribute(cellCol0,"text",0)
        treeCol1.add_attribute(cellCol1,"text",1)
        treeCol2.add_attribute(cellCol2,"text",2)
        treeCol3.add_attribute(cellCol3,"text",3)
        treeCol0.set_attributes(cellCol0,markup=0)

        cellCol3.set_alignment(0.95,0.5)

        # Enable to Show Sorting
        if debugShowSort:
            cellCol4 = Gtk.CellRendererText()
            treeCol4 = self.treeView.get_column(4)
            treeCol4.set_visible(True)
            treeCol4.pack_start(cellCol4,False)
            treeCol4.add_attribute(cellCol4,"text",4)

        # Data Maps and Lists
        self.allScenes = DataList(self.mainConf.dataPath,NAME_SCNE)

        self.iterMap   = {}
        self.chapMap   = {}
        self.chapCount = {}

        return

    def loadContent(self, bookPath):

        self.treeStore.clear()

        if bookPath == "" or bookPath is None: return

        self.allScenes.setDataPath(bookPath)
        self.allScenes.makeList()

        self.iterMap   = {}
        self.chapMap   = {}
        self.chapCount = {}

        scnRoot = makeSceneNumber(GRP_SCNE,0,0,0)
        self.chapCount[scnRoot] = 0

        tmpItem = DataWrapper(NAME_SCNE)
        for itemHandle in self.allScenes.dataList.keys():
            tmpItem.setDataPath(self.allScenes.dataList[itemHandle])
            tmpItem.loadDetails()

            scnNum = makeSceneNumber(GRP_SCNE,tmpItem.section,tmpItem.chapter,tmpItem.number)
            scnSec = makeSceneNumber(GRP_SCNE,tmpItem.section,tmpItem.chapter,0)

            if tmpItem.section == 0:
                parIter = None
                self.chapCount[scnSec] += 1
            else:
                if scnSec in self.chapMap:
                    parIter = self.chapMap[scnSec]
                    self.chapCount[scnSec] += 1
                else:
                    if tmpItem.section == 1: scnChapter = "<b>Prologue</b>"
                    if tmpItem.section == 2: scnChapter = "<b>Chapter %d</b>" % tmpItem.chapter
                    if tmpItem.section == 3: scnChapter = "<b>Epilogue</b>"
                    parIter = self.treeStore.append(None,[scnChapter,None,None,None,scnSec,None])
                    self.chapMap[scnSec]  = parIter
                    self.chapCount[scnSec] = 1

            scnTitle  = tmpItem.title
            scnNumber = str(tmpItem.number)
            scnPOV    = tmpItem.pov
            scnWords  = tmpItem.words
            tmpIter   = self.treeStore.append(parIter,[scnTitle,scnNumber,scnPOV,scnWords,scnNum,itemHandle])
            self.iterMap[itemHandle] = tmpIter

        self.treeView.expand_all()

        return

    def getPath(self, itemHandle):
        if itemHandle in self.allScenes.dataList: return self.allScenes.dataList[itemHandle]
        return None

# End Class SceneTree
