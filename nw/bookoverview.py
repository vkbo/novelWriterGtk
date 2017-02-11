# -*- coding: utf-8 -*

##
#  novelWriter – Book Overview Window
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Shows the scene list with more details than the main window
##

import logging as logger

import gi
gi.require_version("Gtk","3.0")

from gi.repository import Gtk
from os            import path
from time          import time
from nw            import *

class BookOverview():

    def __init__(self, theBook):

        # Connect to GUI
        self.mainConf   = CONFIG
        self.winBuilder = Gtk.Builder()
        self.winObject  = self.winBuilder.get_object

        self.theBook    = theBook
        self.treeView   = None
        self.treeStore  = None
        self.treeSort   = None

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
        self.treeSort.set_sort_column_id(5,Gtk.SortType.ASCENDING)
        self.treeView.set_model(self.treeSort)

        # Columns
        cellCol0 = Gtk.CellRendererText()
        cellCol1 = Gtk.CellRendererText()
        cellCol2 = Gtk.CellRendererText()
        cellCol3 = Gtk.CellRendererText()
        cellCol4 = Gtk.CellRendererText()
        cellCol5 = Gtk.CellRendererText()
        treeCol0 = self.treeView.get_column(0)
        treeCol1 = self.treeView.get_column(1)
        treeCol2 = self.treeView.get_column(2)
        treeCol3 = self.treeView.get_column(3)
        treeCol4 = self.treeView.get_column(4)
        treeCol5 = self.treeView.get_column(5)

        treeCol0.pack_start(cellCol0,True)
        treeCol1.pack_start(cellCol1,False)
        treeCol2.pack_start(cellCol2,False)
        treeCol3.pack_start(cellCol3,False)
        treeCol4.pack_start(cellCol4,False)
        treeCol5.pack_start(cellCol5,False)
        treeCol0.add_attribute(cellCol0,"text",0)
        treeCol1.add_attribute(cellCol1,"text",1)
        treeCol2.add_attribute(cellCol2,"text",2)
        treeCol3.add_attribute(cellCol3,"text",3)
        treeCol4.add_attribute(cellCol4,"text",4)
        treeCol5.add_attribute(cellCol5,"text",5)

        guiHandlers = {
            "onClickBookOverviewDestroy" : self.destroyGUI,
        }
        self.winBuilder.connect_signals(guiHandlers)

        winBookOverview.show_all()

        self.isRunning = True

        return

    def destroyGUI(self, guiObject=None):
        if not self.isRunning: return
        self.winObject("winBookOverview").destroy()
        return

# End Class BookOverview
