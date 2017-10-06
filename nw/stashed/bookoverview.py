# -*- coding: utf-8 -*
"""novelWriter Book Overview Window

novelWriter – Book Overview Window
==================================
Shows the scene list with more details than the main window

File History:
Created: 2017-02-11 [0.4.0]

"""

import logging as logger
import nw
import gi
gi.require_version("Gtk","3.0")

from gi.repository import Gtk
from os            import path
from time          import time
from nw.functions  import makeSortString

# Set to true to show sorting in treeview
debugShowSort = True

class BookOverview():

    def __init__(self, theBook):

        """
        Tree Store Structure:
        Col 1 : String : Scene title
        Col 2 : String : Scene number
        Col 3 : String : Word count
        Col 4 : String : Edit time
        Col 5 : String : Word rate
        Col 6 : String : List sorting column
        """

        # Constants
        self.COL_TITLE  = 0
        self.COL_NUMBER = 1
        self.COL_WORDS  = 2
        self.COL_TIMER  = 3
        self.COL_RATE   = 4
        self.COL_SORT   = 5

        # Connect to GUI
        self.mainConf   = nw.CONFIG
        self.winBuilder = Gtk.Builder()
        self.winObject  = self.winBuilder.get_object

        self.theBook    = theBook
        self.treeView   = None
        self.treeStore  = None
        self.treeSort   = None

        self.isRunning  = False

        return

    def showGUI(self):

        guiFile = path.join(self.mainConf.guiPath,"winBookOverview.glade")
        self.winBuilder.add_from_file(guiFile)
        winBookOverview = self.winObject("winBookOverview")

        # Core objects
        self.treeView   = self.winObject("treeBook")
        self.treeStore  = Gtk.TreeStore(str,str,str,str,str,str)
        self.treeSort   = Gtk.TreeModelSort(model=self.treeStore)

        # Data Sorting
        self.treeSort.set_sort_column_id(self.COL_SORT,Gtk.SortType.ASCENDING)
        self.treeView.set_model(self.treeSort)

        # Columns
        cellCol0 = Gtk.CellRendererText()
        cellCol1 = Gtk.CellRendererText()
        cellCol2 = Gtk.CellRendererText()
        cellCol3 = Gtk.CellRendererText()
        cellCol4 = Gtk.CellRendererText()
        treeCol0 = self.treeView.get_column(0)
        treeCol1 = self.treeView.get_column(1)
        treeCol2 = self.treeView.get_column(2)
        treeCol3 = self.treeView.get_column(3)
        treeCol4 = self.treeView.get_column(4)

        treeCol0.pack_start(cellCol0,True)
        treeCol1.pack_start(cellCol1,False)
        treeCol2.pack_start(cellCol2,False)
        treeCol3.pack_start(cellCol3,False)
        treeCol4.pack_start(cellCol4,False)
        treeCol0.add_attribute(cellCol0,"text",0)
        treeCol1.add_attribute(cellCol1,"text",1)
        treeCol2.add_attribute(cellCol2,"text",2)
        treeCol3.add_attribute(cellCol3,"text",3)
        treeCol4.add_attribute(cellCol4,"text",4)
        treeCol0.set_attributes(cellCol0,markup=0)
        treeCol2.set_attributes(cellCol2,markup=2)

        cellCol2.set_alignment(1.0,0.5)

        # Enable to Show Sorting
        if debugShowSort:
            cellCol5 = Gtk.CellRendererText()
            treeCol5 = self.treeView.get_column(5)
            treeCol5.set_visible(True)
            treeCol5.pack_start(cellCol5,False)
            treeCol5.add_attribute(cellCol5,"text",5)

        guiHandlers = {
            "onClickBookOverviewDestroy" : self.destroyGUI,
        }
        self.winBuilder.connect_signals(guiHandlers)

        winBookOverview.show_all()

        self.isRunning = True
        self.loadContent()

        return

    def destroyGUI(self, guiObject=None):
        if not self.isRunning: return
        self.winObject("winBookOverview").destroy()
        self.isRunning = False
        return

    def loadContent(self):

        # self.treeSelect.set_mode(Gtk.SelectionMode.NONE)
        self.treeStore.clear()

        if not self.theBook.bookLoaded:
            logger.debug("BookOverview.loadContent: No book loaded")
            return

        self.iterMap   = {}
        self.chapMap   = {}
        self.chapCount = {}

        self.chapCount[makeSortString(0,0,0)] = 0
        sceneIndex = self.theBook.getSceneIndex()

        for itemHandle in sceneIndex.keys():

            itemData   = sceneIndex[itemHandle]

            tmpTitle   = itemData[nw.SCIDX_TITLE]
            tmpWords   = itemData[nw.SCIDX_WORDS]
            tmpSection = itemData[nw.SCIDX_SECTION]
            tmpChapter = itemData[nw.SCIDX_CHAPTER]
            tmpNumber  = itemData[nw.SCIDX_NUMBER]
            tmpTime    = itemData[nw.SCIDX_TIME]

            scnNum     = makeSortString(tmpSection,tmpChapter,tmpNumber)
            scnSec     = makeSortString(tmpSection,tmpChapter,0)

            if scnSec in self.chapMap:
                parIter = self.chapMap[scnSec]
                self.chapCount[scnSec] += 1
            else:
                if tmpSection == nw.SCN_NONE: scnChapter = "<b>Unassigned</b>"
                if tmpSection == nw.SCN_PRO:  scnChapter = "<b>Prologue</b>"
                if tmpSection == nw.SCN_CHAP: scnChapter = "<b>Chapter %d</b>" % tmpChapter
                if tmpSection == nw.SCN_EPI:  scnChapter = "<b>Epilogue</b>"
                if tmpSection == nw.SCN_ARCH: scnChapter = "<b>Archived</b>"
                parIter = self.treeStore.append(None,[scnChapter,None,None,None,None,scnSec])
                self.chapMap[scnSec]   = parIter
                self.chapCount[scnSec] = 1

            if tmpSection == nw.SCN_ARCH:
                tmpTitle = "<span foreground='red'>"+str(tmpTitle)+"</span>"

            tmpData = [tmpTitle,str(tmpNumber),str(tmpWords),str(tmpTime),"",scnNum]
            tmpIter = self.treeStore.append(parIter,tmpData)
            self.iterMap[itemHandle] = tmpIter

        self.treeView.expand_all()
        # self.sumWords()
        # self.treeSelect.set_mode(Gtk.SelectionMode.SINGLE)

        return

# End Class BookOverview
