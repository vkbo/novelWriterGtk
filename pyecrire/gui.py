# -*- coding: utf-8 -*
#
#  pyÉcrire – Main GUI Class
#
##

import logging as logger

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit', '3.0')

from gi.repository             import Gtk, GLib, WebKit
from time                      import sleep
from pyecrire.editor           import Editor
from pyecrire.timer            import Timer
from pyecrire.data.project     import Project
from pyecrire.data.datalist    import DataList
from pyecrire.data.datawrapper import DataWrapper

class GUI():

    def __init__(self, config):

        self.guiLoaded = False

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
            "onChangeTreeBooks"        : self.onSelectBook,
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
            "onClickSceneAdd"          : self.onSceneAdd,
            "onClickSceneRemove"       : self.onSceneRemove,
            "onClickSceneUp"           : self.onSceneUp,
            "onClickSceneDown"         : self.onSceneDown,
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
        #self.detailsPane  = self.getObject("detailsNoteBook")
        #self.detailsPane.set_show_tabs(False)
        #self.detailsPane.set_current_page(1)

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
        self.allScenes     = DataList(self.mainConf.dataPath,"Scenes")

        # Gtk ListStore and TreeStore
        self.bookStore  = Gtk.TreeStore(str,str,str)
        self.fileStore  = Gtk.TreeStore(str,int,str)
        self.univStore  = Gtk.TreeStore(str,int,str)
        self.sceneStore = Gtk.TreeStore(str,int,str,int,str)
        self.univList   = Gtk.ListStore(str,str)
        self.bookType   = Gtk.ListStore(str)

        # Handle to List Item Map
        self.mapBookStore = {}
        self.mapUnivStore = {}
        self.mapUnivList  = {}

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
        treeMainCol0.set_attributes(cellMainCol0,markup=0)

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
        treeUnivCol0.set_attributes(cellUnivCol0,markup=0)

        ## Scenes Tree
        treeScene     = self.getObject("treeScenes")
        treeScene.set_model(self.sceneStore)
        cellSceneCol0 = Gtk.CellRendererText()
        cellSceneCol1 = Gtk.CellRendererText()
        cellSceneCol2 = Gtk.CellRendererText()
        cellSceneCol3 = Gtk.CellRendererText()
        treeSceneCol0 = treeScene.get_column(0)
        treeSceneCol1 = treeScene.get_column(1)
        treeSceneCol2 = treeScene.get_column(2)
        treeSceneCol3 = treeScene.get_column(3)
        treeSceneCol0.pack_start(cellSceneCol0,True)
        treeSceneCol1.pack_start(cellSceneCol1,False)
        treeSceneCol2.pack_start(cellSceneCol2,False)
        treeSceneCol3.pack_start(cellSceneCol3,False)
        treeSceneCol0.add_attribute(cellSceneCol0,"text",0)
        treeSceneCol1.add_attribute(cellSceneCol1,"text",1)
        treeSceneCol2.add_attribute(cellSceneCol2,"text",2)
        treeSceneCol3.add_attribute(cellSceneCol3,"text",3)
        treeSceneCol0.set_attributes(cellSceneCol0,markup=0)

        ## Book Details Universe List
        cmbDetailsBookUniverse  = self.getObject("cmbBookUniverse")
        cmbDetailsBookUniverse.set_model(self.univList)

        # Load Project Data
        self.loadProjects()
        self.loadBookFiles()
        self.loadUnivFiles()

        # Default Values
        self.editType = self.EDIT_BOOK

        # Prepare Main Window
        self.winMain.set_title(self.mainConf.appName)
        self.winMain.resize(self.mainConf.winWidth,self.mainConf.winHeight)
        self.winMain.set_position(Gtk.WindowPosition.CENTER)
        self.winMain.show_all()

        self.guiLoaded = True

        return


    def loadProjects(self):

        self.allBooks.makeList()
        self.allUniverses.makeList()

        self.mapBookStore = {}
        self.mapUnivStore = {}
        self.mapUnivList  = {}

        tmpItem = DataWrapper("Universe")
        for itemHandle in self.allUniverses.dataList.keys():
            tmpItem.setDataPath(self.allUniverses.dataList[itemHandle])
            tmpItem.loadDetails()
            tmpIter = self.bookStore.append(None,["<b>"+tmpItem.title+"</b>",None,itemHandle])
            self.mapUnivStore[itemHandle] = tmpIter
            tmpIter = self.univList.append([tmpItem.title,itemHandle])
            self.mapUnivList[itemHandle]  = tmpIter

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


    def loadScenes(self):

        if self.projData.bookHandle == "": return

        bookPath = self.allBooks.getItem(self.projData.bookHandle)

        self.allScenes.setDataPath(bookPath)
        self.allScenes.makeList()

        return


    def loadBookFiles(self, bookHandle = ""):

        self.fileStore.clear()
        self.fileStore.append(None,["<b>Files</b>",0,""])
        self.fileStore.append(None,["<b>Scenes</b>",0,""])

        if bookHandle == "": return

        return


    def loadUnivFiles(self, universeHandle = ""):

        self.univStore.clear()
        self.univStore.append(None,["<b>Files</b>",0,""])
        self.univStore.append(None,["<b>Characters</b>",0,""])

        if universeHandle == "": return

        return


    def displayBook(self):

        self.getObject("entryBookTitle").set_text(self.projData.bookTitle)
        self.getObject("cmbBookUniverse").set_active_iter(self.mapUnivList[self.projData.theBook.parent])

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

    def onSelectBook(self, guiObject):

        logger.debug("Select Book")
        if not self.guiLoaded: return

        (listModel, pathList) = guiObject.get_selected_rows()
        for pathItem in pathList:
            listIter   = listModel.get_iter(pathItem)
            itemHandle = listModel.get_value(listIter,2)

        if len(pathItem) == 1:
            self.getObject("treeBooks").expand_row(pathItem,False)

        if len(pathItem) == 2:
            parIter   = listModel.get_iter(pathItem[0])
            parHandle = listModel.get_value(parIter,2)
            itemPath  = self.allBooks.getItem(itemHandle)
            parPath   = self.allUniverses.getItem(parHandle)
            self.projData.loadProject(itemPath,itemHandle,parPath,parHandle)
            self.displayBook()
            self.loadScenes()

        return


    def onFileSave(self, guiObject):
        logger.debug("Saving")

        if self.editType == self.EDIT_BOOK:

            bookTitle      = self.getObject("entryBookTitle").get_text()
            chkNewUniverse = self.getObject("chkNewUniverse")

            self.projData.createBook(bookTitle)

            if chkNewUniverse.get_active():
                universeTitle = self.getObject("entryBookUniverse").get_text()
                self.projData.createUniverse(universeTitle)
            else:
                univIdx  = self.getObject("cmbBookUniverse").get_active()
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


    def onSceneAdd(self, guiObject):

        if self.projData.bookHandle == "": return

        sceneNum = self.allScenes.dataLen + 1
        self.sceneStore.append(None,["New Scene",sceneNum,"",0,""])

        return


    def onSceneRemove(self, guiObject):
        return


    def onSceneUp(self, guiObject):
        return


    def onSceneDown(self, guiObject):
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
            self.getObject("entryBookUniverse").set_can_focus(True)
        else:
            self.getObject("entryBookUniverse").set_can_focus(False)
        return


# End Class GUI
