# -*- coding: utf-8 -*

##
#  pyÉcrire – Data Tree Classed
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Wrapper classes for all the Gtk.TreeView objects in the main GUI.
#  All manipulation of content as well as loading of data is handled here.
#  Meta data related to the files listed are also kept as hidden columns and
#  in additional dictionaries and lists as they are needed by the main GUI.
#  This includes plain lists needed for combo boxes.
##

import logging as logger

import gi
gi.require_version("Gtk","3.0")

from gi.repository        import Gtk
from pyecrire             import *
from pyecrire.datalist    import DataList
from pyecrire.datawrapper import DataWrapper
from pyecrire.functions   import makeSceneNumber, reformatDate, formatTime, dateFromString

# Set to true to show sorting in all treeviews
debugShowSort = False

class ProjectTree():

    def __init__(self):

        """
        Tree Store Structure:
        Col 1 : String : Book title or universe title
        Col 2 : String : Book status
        Col 3 : String : List sorting column
        Col 4 : String : Book handle
        """

        # Connect to GUI
        self.mainConf   = CONFIG
        self.getObject  = BUILDER.get_object

        # Core objects
        self.treeView   = self.getObject("treeProject")
        self.treeSelect = self.getObject("treeProjectSelect")
        self.treeStore  = Gtk.TreeStore(str,str,str,str)
        self.treeSort   = Gtk.TreeModelSort(model=self.treeStore)

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

        self.treeSelect.set_mode(Gtk.SelectionMode.NONE)
        self.treeStore.clear()

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

        self.treeSelect.set_mode(Gtk.SelectionMode.SINGLE)

        return

    def getPath(self, itemHandle):
        if itemHandle in self.allBooks.dataList: return self.allBooks.dataList[itemHandle]
        if itemHandle in self.allUnivs.dataList: return self.allUnivs.dataList[itemHandle]
        return None

    def getType(self, itemHandle):
        if itemHandle in self.allBooks.dataList: return NAME_BOOK
        if itemHandle in self.allUnivs.dataList: return NAME_UNIV
        return NAME_NONE

    def getIter(self, itemHandle):
        if itemHandle in self.iterMap:  return self.aiterMap[itemHandle]
        return None

# End Class ProjectTree

class BookTree():

    def __init__(self):

        """
        Tree Store Structure:
        Col 1 : String : Plot or scene title
        Col 2 : String : Word count
        Col 3 : String : List sorting column
        Col 4 : String : File handle
        Col 5 : Bool   : Editable title
        """

        self.COL_TITLE  = 0
        self.COL_WORDS  = 1
        self.COL_SORT   = 2
        self.COL_HANDLE = 3
        self.COL_EDIT   = 4

        # Connect to GUI
        self.mainConf   = CONFIG
        self.getObject  = BUILDER.get_object

        # Core objects
        self.treeView   = self.getObject("treeBook")
        self.treeSelect = self.getObject("treeBookSelect")
        self.treeStore  = Gtk.TreeStore(str,str,str,str,bool)
        self.treeSort   = Gtk.TreeModelSort(model=self.treeStore)

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
        treeCol0.set_attributes(cellCol0,markup=0,editable=4)
        treeCol1.set_attributes(cellCol1,markup=1)

        cellCol1.set_alignment(1.0,0.5)
        self.editCell = cellCol0

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

        self.treeSelect.set_mode(Gtk.SelectionMode.NONE)
        self.treeStore.clear()

        pltSort = makeSceneNumber(GRP_PLOT,0,0,0)
        scnSort = makeSceneNumber(GRP_SCNE,0,0,0)
        pltIter = self.treeStore.append(None,["<b>Plots</b>",None,pltSort,"",False])
        scnIter = self.treeStore.append(None,["<b>Scenes</b>",None,scnSort,"",False])

        if bookPath == "" or bookPath is None: return

        self.allPlots.setDataPath(bookPath)
        self.allScenes.setDataPath(bookPath)

        self.allPlots.makeList()
        self.allScenes.makeList()

        self.iterMap = {}
        self.chapMap = {}

        tmpItem = DataWrapper(NAME_PLOT)
        for itemHandle in self.allPlots.dataList.keys():
            tmpItem.setDataPath(self.allPlots.dataList[itemHandle])
            tmpItem.loadDetails()

            pltNum = makeSceneNumber(GRP_PLOT,0,0,tmpItem.number)
            tmpIter = self.treeStore.append(pltIter,[tmpItem.title,str(tmpItem.words),pltNum,itemHandle,True])
            self.iterMap[itemHandle] = tmpIter

        tmpItem = DataWrapper(NAME_SCNE)
        for itemHandle in self.allScenes.dataList.keys():
            tmpItem.setDataPath(self.allScenes.dataList[itemHandle])
            tmpItem.loadDetails()

            scnNum = makeSceneNumber(GRP_SCNE,tmpItem.section,tmpItem.chapter,tmpItem.number)
            scnSec = makeSceneNumber(GRP_SCNE,tmpItem.section,tmpItem.chapter,0)

            if tmpItem.section == 0:
                parIter = scnIter
            else:
                if scnSec in self.chapMap:
                    parIter = self.chapMap[scnSec]
                else:
                    if tmpItem.section == 1: scnChapter = "<b>Prologue</b>"
                    if tmpItem.section == 2: scnChapter = "<b>Chapter %d</b>" % tmpItem.chapter
                    if tmpItem.section == 3: scnChapter = "<b>Epilogue</b>"

                    parIter = self.treeStore.append(scnIter,[scnChapter,None,scnSec,None,False])
                    self.chapMap[scnSec] = parIter

            tmpIter = self.treeStore.append(parIter,[tmpItem.title,str(tmpItem.words),scnNum,itemHandle,True])
            self.iterMap[itemHandle] = tmpIter

        self.treeView.expand_all()
        self.sumWords()
        self.treeSelect.set_mode(Gtk.SelectionMode.SINGLE)

        return

    def sumWords(self):
        for chIter in self.chapMap.items():
            if self.treeStore.iter_has_child(chIter[1]):
                nChildren = self.treeStore.iter_n_children(chIter[1])
                wordSum   = 0
                for n in range(nChildren):
                    scnIter  = self.treeStore.iter_nth_child(chIter[1],n)
                    wordSum += int(self.treeStore.get_value(scnIter,self.COL_WORDS))
                wordCount = "<span foreground='blue'>"+str(wordSum)+"</span>"
                self.treeStore.set_value(chIter[1],self.COL_WORDS,wordCount)
        return

    def getPath(self, itemHandle):
        if itemHandle in self.allPlots.dataList:  return self.allPlots.dataList[itemHandle]
        if itemHandle in self.allScenes.dataList: return self.allScenes.dataList[itemHandle]
        return None

    def getType(self, itemHandle):
        if itemHandle in self.allPlots.dataList:  return NAME_PLOT
        if itemHandle in self.allScenes.dataList: return NAME_SCNE
        return NAME_NONE

    def getIter(self, itemHandle):
        if itemHandle in self.iterMap: return self.iterMap[itemHandle]
        return None

    def setValue(self, itemHandle, colIdx, newValue):
        iterHandle = self.getIter(itemHandle)
        if iterHandle is not None:
            self.treeStore.set_value(iterHandle,colIdx,str(newValue))
        return

# End Class BookTree

class UniverseTree():

    def __init__(self):

        """
        Tree Store Structure:
        Col 1 : String : History or character title
        Col 2 : String : Word count
        Col 3 : String : List sorting column
        Col 4 : String : File handle
        """

        self.COL_TITLE  = 0
        self.COL_WORDS  = 1
        self.COL_SORT   = 2
        self.COL_HANDLE = 3

        # Connect to GUI
        self.mainConf   = CONFIG
        self.getObject  = BUILDER.get_object

        # Core objects
        self.treeView   = self.getObject("treeUniverse")
        self.treeSelect = self.getObject("treeUniverseSelect")
        self.treeStore  = Gtk.TreeStore(str,str,str,str)
        self.treeSort   = Gtk.TreeModelSort(model=self.treeStore)

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

        cellCol1.set_alignment(1.0,0.5)

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

        self.treeSelect.set_mode(Gtk.SelectionMode.NONE)
        self.treeStore.clear()

        pltSort = makeSceneNumber(GRP_HIST,0,0,0)
        scnSort = makeSceneNumber(GRP_CHAR,0,0,0)
        pltIter = self.treeStore.append(None,["<b>History</b>",None,pltSort,""])
        scnIter = self.treeStore.append(None,["<b>Characters</b>",None,scnSort,""])

        if univPath == "" or univPath is None: return

        self.allChars.setDataPath(univPath)
        self.allChars.makeList()

        self.iterMap = {}
        self.treeSelect.set_mode(Gtk.SelectionMode.SINGLE)

        return

    def getPath(self, itemHandle):
        if itemHandle in self.allHists.dataList: return self.allHists.dataList[itemHandle]
        if itemHandle in self.allChars.dataList: return self.allChars.dataList[itemHandle]
        return None

    def getType(self, itemHandle):
        if itemHandle in self.allHists.dataList: return NAME_HIST
        if itemHandle in self.allChars.dataList: return NAME_CHAR
        return NAME_NONE

    def getIter(self, itemHandle):
        if itemHandle in self.iterMap:  return self.aiterMap[itemHandle]
        return None

    def setValue(self, itemHandle, colIdx, newValue):
        iterHandle = self.getIter(itemHandle)
        if iterHandle is not None:
            self.treeStore.set_value(iterHandle,colIdx,str(newValue))
        return

# End Class UniverseTree

class SceneTree():

    def __init__(self):

        """
        Tree Store Structure:
        Col 1 : String  : Scene title
        Col 2 : String  : Scene number
        Col 3 : String  : Point of view character
        Col 4 : Integer : Word count
        Col 5 : String  : List sorting column
        Col 5 : String  : File handle
        """

        self.COL_TITLE  = 0
        self.COL_NUMBER = 1
        self.COL_POV    = 2
        self.COL_WORDS  = 3
        self.COL_SORT   = 4
        self.COL_HANDLE = 5

        # Connect to GUI
        self.mainConf   = CONFIG
        self.getObject  = BUILDER.get_object

        # Core objects
        self.treeView   = self.getObject("treeScenes")
        self.treeSelect = self.getObject("treeScenesSelect")
        self.treeStore  = Gtk.TreeStore(str,str,str,str,str,str)
        self.treeSort   = Gtk.TreeModelSort(model=self.treeStore)

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
        treeCol3.set_attributes(cellCol3,markup=3)

        cellCol3.set_alignment(1.0,0.5)

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

        self.treeSelect.set_mode(Gtk.SelectionMode.NONE)
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
                    self.chapMap[scnSec]   = parIter
                    self.chapCount[scnSec] = 1

            scnTitle  = tmpItem.title
            scnNumber = str(tmpItem.number)
            scnPOV    = tmpItem.pov
            scnWords  = str(tmpItem.words)
            tmpIter   = self.treeStore.append(parIter,[scnTitle,scnNumber,scnPOV,scnWords,scnNum,itemHandle])
            self.iterMap[itemHandle] = tmpIter

        self.treeView.expand_all()
        self.sumWords()
        self.treeSelect.set_mode(Gtk.SelectionMode.SINGLE)

        return

    def clearContent(self):

        self.treeStore.clear()

        self.iterMap   = {}
        self.chapMap   = {}
        self.chapCount = {}

        return

    def sumWords(self):
        for chIter in self.chapMap.items():
            if self.treeStore.iter_has_child(chIter[1]):
                nChildren = self.treeStore.iter_n_children(chIter[1])
                wordSum   = 0
                for n in range(nChildren):
                    scnIter  = self.treeStore.iter_nth_child(chIter[1],n)
                    wordSum += int(self.treeStore.get_value(scnIter,self.COL_WORDS))
                wordCount = "<span foreground='blue'>"+str(wordSum)+"</span>"
                self.treeStore.set_value(chIter[1],self.COL_WORDS,wordCount)
        return

    def getPath(self, itemHandle):
        if itemHandle in self.allScenes.dataList: return self.allScenes.dataList[itemHandle]
        return None

    def getIter(self, itemHandle):
        if itemHandle in self.iterMap:  return self.iterMap[itemHandle]
        return None

    def setValue(self, itemHandle, colIdx, newValue):
        iterHandle = self.getIter(itemHandle)
        if iterHandle is not None:
            self.treeStore.set_value(iterHandle,colIdx,str(newValue))
        return

# End Class SceneTree

class FileVersionTree():

    def __init__(self):

        """
        Tree Store Structure:
        Col 1 : String  : File date
        Col 2 : String  : File name
        """

        # Connect to GUI
        self.mainConf   = CONFIG
        self.getObject  = BUILDER.get_object

        # Core objects
        self.treeView   = self.getObject("treeVersion")
        self.treeSelect = self.getObject("treeVersionSelect")
        self.treeStore  = Gtk.TreeStore(str,str)
        self.treeSort   = Gtk.TreeModelSort(model=self.treeStore)

        # Data Sorting
        self.treeSort.set_sort_column_id(1,Gtk.SortType.DESCENDING)
        self.treeView.set_model(self.treeSort)

        # Columns
        cellCol0 = Gtk.CellRendererText()
        treeCol0 = self.treeView.get_column(0)

        treeCol0.pack_start(cellCol0,True)
        treeCol0.add_attribute(cellCol0,"text",0)

        # Enable to Show Sorting
        if debugShowSort:
            cellCol1 = Gtk.CellRendererText()
            treeCol1 = self.treeView.get_column(1)
            treeCol1.set_visible(True)
            treeCol1.pack_start(cellCol1,False)
            treeCol1.add_attribute(cellCol1,"text",1)

        return

    def loadContent(self, fileList):

        self.treeSelect.set_mode(Gtk.SelectionMode.NONE)
        self.treeStore.clear()

        for itemHandle in fileList.keys():
            self.treeStore.append(None,[reformatDate(itemHandle),itemHandle])

        self.treeSelect.set_mode(Gtk.SelectionMode.SINGLE)

        return

    def clearTree(self):
        self.treeStore.clear()
        return

# End Class FileVersionTree

class TimeTree():

    def __init__(self):

        """
        Tree Store Structure:
        Col 1 : String  : Date
        Col 2 : String  : Time
        Col 3 : String  : Words
        Col 4 : String  : Sort
        """

        # Connect to GUI
        self.mainConf   = CONFIG
        self.getObject  = BUILDER.get_object

        # Core objects
        self.treeView   = self.getObject("treeTimes")
        self.treeSelect = self.getObject("treeTimesSelect")
        self.treeStore  = Gtk.TreeStore(str,str,str,str)
        self.treeSort   = Gtk.TreeModelSort(model=self.treeStore)

        # Data Sorting
        self.treeSort.set_sort_column_id(3,Gtk.SortType.DESCENDING)
        self.treeView.set_model(self.treeSort)

        # Columns
        cellCol0 = Gtk.CellRendererText()
        cellCol1 = Gtk.CellRendererText()
        cellCol2 = Gtk.CellRendererText()
        treeCol0 = self.treeView.get_column(0)
        treeCol1 = self.treeView.get_column(1)
        treeCol2 = self.treeView.get_column(2)

        treeCol0.pack_start(cellCol0,True)
        treeCol1.pack_start(cellCol1,False)
        treeCol2.pack_start(cellCol2,False)
        treeCol0.add_attribute(cellCol0,"text",0)
        treeCol1.add_attribute(cellCol1,"text",1)
        treeCol2.add_attribute(cellCol2,"text",2)

        cellCol2.set_alignment(1.0,0.5)

        # Enable to Show Sorting
        if debugShowSort:
            cellCol3 = Gtk.CellRendererText()
            treeCol3 = self.treeView.get_column(3)
            treeCol3.set_visible(True)
            treeCol3.pack_start(cellCol3,False)
            treeCol3.add_attribute(cellCol3,"text",3)

        return

    def loadContent(self, timeList):

        self.treeSelect.set_mode(Gtk.SelectionMode.NONE)
        self.treeStore.clear()

        for timeSet in timeList:
            timeDate  = timeSet[0][6:8]+"/"+timeSet[0][4:6]
            timeVal   = formatTime(float(timeSet[1]))
            timeWords = timeSet[2]
            timeSort  = timeSet[0]
            self.treeStore.append(None,[timeDate,timeVal,timeWords,timeSort])

        self.treeSelect.set_mode(Gtk.SelectionMode.SINGLE)

        return

    def clearTree(self):
        self.treeStore.clear()
        return

# End Class TimeTree

