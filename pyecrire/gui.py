# -*- coding: utf-8 -*
#
#  pyÉcrire – Main GUI Class
#
##

import logging as logger

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit', '3.0')

from gi.repository      import Gtk, GLib, WebKit
from time               import sleep
from pyecrire.editor    import Editor
from pyecrire.timer     import Timer
from pyecrire.project   import *
from pyecrire.datastore import *
from pyecrire.datalist  import *

class GUI():

    def __init__(self, config):

        # Constants
        self.EDIT_FILE      = 0
        self.EDIT_BOOK      = 1
        self.EDIT_SCENE     = 2
        self.EDIT_UNIVERSE  = 3
        self.EDIT_CHARACTER = 4

        # Define Core Objects
        self.mainConf   = config
        self.projData   = Project(self.mainConf)

        # Initialise GUI
        self.guiBuilder = Gtk.Builder()
        self.guiBuilder.add_from_file("pyecrire/gui/winMain.glade")

        self.getObject  = self.guiBuilder.get_object
        self.winMain    = self.getObject("winMain")

        # Prepare GUI Classes
        self.webEditor  = Editor(self.winMain)
        self.guiTimer   = Timer(self.guiBuilder,self.mainConf)

        # Set Up Event Handlers
        guiHandlers = {
            "onDestroyWindow"          : self.guiDestroy,
            "onEventKeyPress"          : self.eventWinKeyPress,
            "onEventWinChange"         : self.eventWinChange,
            "onSwitchPageMainNoteBook" : self.eventTabChange,
            "onSwitchPageSideNoteBook" : self.eventTreeChange,
            "onClickNew"               : self.projData.newProject,
            "onClickSave"              : self.onFileSave,
            "onClickEditBold"          : self.webEditor.onEditAction,
            "onClickEditItalic"        : self.webEditor.onEditAction,
            "onClickEditUnderline"     : self.webEditor.onEditAction,
            "onClickEditStrikeThrough" : self.webEditor.onEditAction,
            "onClickEditColour"        : self.webEditor.onEditColour,
            "onClickTimerStart"        : self.guiTimer.onTimerStart,
            "onClickTimerPause"        : self.guiTimer.onTimerPause,
            "onClickTimerStop"         : self.guiTimer.onTimerStop,
            "onToggleNewUniverse"      : self.onToggleNewUniverse,
            "onMenuActionHelpAbout"    : self.onActionShowAbout,
            "onMenuActionFileSave"     : self.onFileSave,
            "onMenuActionFileQuit"     : self.guiDestroy,
        }
        self.guiBuilder.connect_signals(guiHandlers)

        # Prepare Panes
        self.guiPaned     = self.getObject("innerPaned")
        self.guiPaned.set_position(self.mainConf.winPane)

        # Prepare Details Pane and Default Document Type
        self.detailsPane  = self.getObject("detailsNoteBook")
        self.detailsPane.set_show_tabs(False)
        self.detailsPane.set_current_page(1)

        # Prepare Editor
        self.scrollEditor = self.getObject("scrollEditor")
        self.scrollEditor.add(self.webEditor)

        # Prepare Statusbar
        self.statusBar  = self.getObject("mainStatus")
        self.statusCID  = self.statusBar.get_context_id("Main")
        self.progStatus = self.getObject("progressStatus")

        # Set Up Timers
        self.timerID    = GLib.timeout_add(200, self.guiTimer.onTick)
        self.autoTaskID = GLib.timeout_add_seconds(30,self.autoTasks)

        ##
        #  Content
        ##

        # Data Lists
        self.allBooks      = DataList(self.mainConf.dataPath,"Book")
        self.allUniverses  = DataList(self.mainConf.dataPath,"Universe")
        self.allCharacters = DataList(self.mainConf.dataPath,"Characters")

        # Handle to List Item Map
        self.mapBookStore = {}
        self.mapUnivStore = {}

        # Gtk ListStore and TreeStore
        self.bookStore = Gtk.TreeStore(str,str,str)
        self.fileStore = Gtk.TreeStore(str,int,str)
        self.univStore = Gtk.TreeStore(str,int,str)
        self.univList  = Gtk.ListStore(str,str)

        ## Books Tree
        treeBooks     = self.getObject("treeBooks")
        treeBooks.set_model(self.bookStore)
        cellBooksCol0 = Gtk.CellRendererText()
        cellBooksCol1 = Gtk.CellRendererText()
        treeBooksCol0 = treeBooks.get_column(0)
        treeBooksCol1 = treeBooks.get_column(1)
        treeBooksCol0.pack_start(cellBooksCol0,True)
        treeBooksCol1.pack_start(cellBooksCol1,False)
        treeBooksCol0.add_attribute(cellBooksCol0,"text",0)
        treeBooksCol1.add_attribute(cellBooksCol1,"text",1)
        treeBooksCol0.set_attributes(cellBooksCol0,markup=0)

        ## Files Tree
        treeMain     = self.getObject("treeMain")
        treeMain.set_model(self.fileStore)
        cellMainCol0 = Gtk.CellRendererText()
        cellMainCol1 = Gtk.CellRendererText()
        treeMainCol0 = treeMain.get_column(0)
        treeMainCol1 = treeMain.get_column(1)
        treeMainCol0.pack_start(cellMainCol0,True)
        treeMainCol1.pack_start(cellMainCol1,False)
        treeMainCol0.add_attribute(cellMainCol0,"text",0)
        treeMainCol1.add_attribute(cellMainCol1,"text",1)

        ## Universe Files Tree
        treeUniv     = self.getObject("treeUniverse")
        treeUniv.set_model(self.univStore)
        cellUnivCol0 = Gtk.CellRendererText()
        cellUnivCol1 = Gtk.CellRendererText()
        treeUnivCol0 = treeUniv.get_column(0)
        treeUnivCol1 = treeUniv.get_column(1)
        treeUnivCol0.pack_start(cellUnivCol0,True)
        treeUnivCol1.pack_start(cellUnivCol1,False)
        treeUnivCol0.add_attribute(cellUnivCol0,"text",0)
        treeUnivCol1.add_attribute(cellUnivCol1,"text",1)

        ## Book Details Universe List
        cmbDetailsBookUniverse  = self.getObject("cmbDetailsBookUniverse")
        cmbDetailsBookUniverse.set_model(self.univList)

        # Load Project Data
        self.loadProjects()

        # Default Values
        self.editType = self.EDIT_BOOK

        # Prepare Main Window
        self.winMain.set_title(self.mainConf.appName)
        self.winMain.resize(self.mainConf.winWidth,self.mainConf.winHeight)
        self.winMain.set_position(Gtk.WindowPosition.CENTER)
        self.winMain.show_all()

        return


    def loadProjects(self):

        self.allBooks.makeList()
        self.allUniverses.makeList()

        self.mapBookStore = {}
        self.mapUnivStore = {}

        tmpItem = DataWrapper("Universe")
        for itemHandle in self.allUniverses.dataList.keys():
            tmpItem.setDataPath(self.allUniverses.dataList[itemHandle])
            tmpItem.loadDetails()
            tmpIter = self.bookStore.append(None,["<b>"+tmpItem.title+"</b>",None,itemHandle])
            self.mapUnivStore[itemHandle] = tmpIter
            self.univList.append([tmpItem.title,itemHandle])

        tmpItem = DataWrapper("Book")
        for itemHandle in self.allBooks.dataList.keys():
            tmpItem.setDataPath(self.allBooks.dataList[itemHandle])
            tmpItem.loadDetails()
            if self.mapUnivStore.has_key(tmpItem.parent):
                tmpIter = self.bookStore.append(self.mapUnivStore[tmpItem.parent],[tmpItem.title,None,itemHandle])
            else:
                logger.error("Orphanded book found with title '%s'." % tmpItem.title)
            self.mapBookStore[itemHandle] = tmpIter

        return


    # Close Program
    def guiDestroy(self, guiObject):
        logger.debug("Exiting")
        self.mainConf.setWinPane(self.guiPaned.get_position())
        self.mainConf.autoSaveConfig()
        Gtk.main_quit()
        return


    # Automated Tasks
    def autoTasks(self):
        self.mainConf.autoSaveConfig()
        return True


    ##
    #  Actions
    ##

    def onFileSave(self, guiObject):
        logger.debug("Saving")

        if self.editType == self.EDIT_BOOK:

            bookTitle      = self.getObject("entryDetailsBookTitle").get_text()
            chkNewUniverse = self.getObject("chkNewUniverse")

            self.projData.createBook(bookTitle)

            if chkNewUniverse.get_active():
                universeTitle = self.getObject("entryDetailsBookUniverse").get_text()
                self.projData.createUniverse(universeTitle)
            else:
                univIdx  = self.getObject("cmbDetailsBookUniverse").get_active()
                univItem = self.univList[univIdx]
                self.projData.setUniverse(univItem[1],self.allUniverses.getItem(univItem[1]))

        self.projData.saveProject()

        return


    def onActionShowAbout(self, guiObject):

        dlgAbout = Gtk.AboutDialog()
        dlgAbout.set_transient_for(self.winMain)
        dlgAbout.set_program_name(self.mainConf.appName)
        dlgAbout.set_version(self.mainConf.appVersion)
        dlgAbout.set_website(self.mainConf.appURL)
        dlgAbout.run()
        dlgAbout.destroy()
        return


    ##
    #  Events
    ##

    def eventTabChange(self, guiObject, guiChild, tabIdx):
        logger.debug("Tab change")
        if tabIdx == 2:
            print("Source View")
            strSource = self.webEditor.getHtml()
            bufferSource = Gtk.TextBuffer()
            bufferSource.set_text(strSource)
            textSource = self.getObject("textSource")
            textSource.set_buffer(bufferSource)
            print(strSource)
        return

    def eventTreeChange(self, guiObject, guiChild, tabIdx):
        logger.debug("Tree tab change")
        if tabIdx == 0:
            self.editType = self.EDIT_BOOK
        if tabIdx == 1:
            self.editType = self.EDIT_FILE
        if tabIdx == 1:
            self.editType = self.EDIT_CHARACTER
        return

    def eventWinKeyPress(self, guiObject, guiEvent):
        self.guiTimer.resetAutoPause()
        return

    def eventWinChange(self, guiObject, guiEvent):
        self.mainConf.setWinSize(guiEvent.width,guiEvent.height)
        return

    def onToggleNewUniverse(self, guiObject):
        if guiObject.get_active():
            self.bookUniverseNew.set_can_focus(True)
        else:
            self.bookUniverseNew.set_can_focus(False)
        return


