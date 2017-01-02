# -*- coding: utf-8 -*
#
#  pyÉcrire – Main GUI Class
#
##

import logging as logger

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit', '3.0')

from gi.repository        import Gtk, GLib, WebKit
from time                 import sleep
from pyecrire.editor      import Editor
from pyecrire.timer       import Timer
from pyecrire.project     import Project
from pyecrire.treeviews   import ProjectTree
from pyecrire.datalist    import DataList
from pyecrire.datawrapper import DataWrapper
from pyecrire.functions   import makeSceneNumber

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
        self.bookTree   = ProjectTree(self.guiBuilder,self.mainConf)

        # Set Up Event Handlers
        guiHandlers = {
            "onDestroyWindow"          : self.guiDestroy,
            "onEventKeyPress"          : self.eventWinKeyPress,
            "onEventWinChange"         : self.eventWinChange,
            "onSwitchPageMainNoteBook" : self.eventTabChange,
            "onSwitchPageSideNoteBook" : self.eventTreeChange,
            "onChangeTreeBooks"        : self.onSelectBook,
            "onChangeTreeMain"         : self.onSelectFile,
            "onClickNew"               : self.projData.newProject,
            "onClickSave"              : self.onFileSave,
            "onToggleEditable"         : self.webEditor.onToggleEditable,
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
            "onClickSceneSave"         : self.onSceneSave,
            "onChangeTreeScenes"       : self.onSelectScene,
            "onToggleNewUniverse"      : self.onToggleNewUniverse,
            "onMenuActionHelpAbout"    : self.onActionShowAbout,
            "onMenuActionFileSave"     : self.onFileSave,
            "onMenuActionFileQuit"     : self.guiDestroy,
        }
        self.guiBuilder.connect_signals(guiHandlers)

        # Prepare Panes
        self.guiPaned     = self.getObject("innerPaned")
        self.guiPaned.set_position(self.mainConf.winPane)

        # Prepare Editor
        self.scrollEditor = self.getObject("scrollEditor")
        self.scrollEditor.add(self.webEditor)

        # Prepare Statusbar
        self.statusBar  = self.getObject("mainStatus")
        self.statusCID  = self.statusBar.get_context_id("Main")
        self.progStatus = self.getObject("progressStatus")

        # Set Up Timers
        self.timerID    = GLib.timeout_add(200,self.guiTimer.onTick)
        self.autoTaskID = GLib.timeout_add_seconds(30,self.autoTasks)

        ##
        #  Content
        ##

        # Data Lists
        self.allBooks      = DataList(self.mainConf.dataPath,"Book")
        self.allUniverses  = DataList(self.mainConf.dataPath,"Universe")
        self.allCharacters = DataList(self.mainConf.dataPath,"Character")
        self.allScenes     = DataList(self.mainConf.dataPath,"Scene")

        # Gtk ListStore and TreeStore
        self.fileStore  = Gtk.TreeStore(str,int,str,str)
        self.univStore  = Gtk.TreeStore(str,int,str,str)
        self.sceneStore = Gtk.TreeStore(str,str,str,int,str,str)
        self.bookType   = Gtk.ListStore(str)

        # Handle to List Item Map
        self.mapFilesStore = {}
        self.mapSceneStore = {}
        self.mapUnivList   = {}
        self.mapChapters   = {}

        # Other List Maps
        self.chapterCount  = {}

        # Files Tree
        treeMain     = self.getObject("treeMain")
        sortMain     = Gtk.TreeModelSort(model=self.fileStore)
        sortMain.set_sort_column_id(2,Gtk.SortType.ASCENDING)
        treeMain.set_model(sortMain)
        cellMainCol0 = Gtk.CellRendererText()
        cellMainCol1 = Gtk.CellRendererText()
        #cellMainCol2 = Gtk.CellRendererText()
        treeMainCol0 = treeMain.get_column(0)
        treeMainCol1 = treeMain.get_column(1)
        #treeMainCol2 = treeMain.get_column(2)
        treeMainCol0.pack_start(cellMainCol0,True)
        treeMainCol1.pack_start(cellMainCol1,False)
        #treeMainCol2.pack_start(cellMainCol2,False)
        treeMainCol0.add_attribute(cellMainCol0,"text",0)
        treeMainCol1.add_attribute(cellMainCol1,"text",1)
        #treeMainCol2.add_attribute(cellMainCol2,"text",2)
        treeMainCol0.set_attributes(cellMainCol0,markup=0)
        cellMainCol1.set_alignment(0.95,0.5)

        # Universe Files Tree
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
        cellUnivCol1.set_alignment(0.95,0.5)

        # Scenes Tree
        treeScene     = self.getObject("treeScenes")
        sortScene     = Gtk.TreeModelSort(model=self.sceneStore)
        sortScene.set_sort_column_id(4,Gtk.SortType.ASCENDING)
        treeScene.set_model(sortScene)
        cellSceneCol0 = Gtk.CellRendererText()
        cellSceneCol1 = Gtk.CellRendererText()
        cellSceneCol2 = Gtk.CellRendererText()
        cellSceneCol3 = Gtk.CellRendererText()
        #cellSceneCol4 = Gtk.CellRendererText()
        treeSceneCol0 = treeScene.get_column(0)
        treeSceneCol1 = treeScene.get_column(1)
        treeSceneCol2 = treeScene.get_column(2)
        treeSceneCol3 = treeScene.get_column(3)
        #treeSceneCol4 = treeScene.get_column(4)
        treeSceneCol0.pack_start(cellSceneCol0,True)
        treeSceneCol1.pack_start(cellSceneCol1,False)
        treeSceneCol2.pack_start(cellSceneCol2,False)
        treeSceneCol3.pack_start(cellSceneCol3,False)
        #treeSceneCol4.pack_start(cellSceneCol4,False)
        treeSceneCol0.add_attribute(cellSceneCol0,"text",0)
        treeSceneCol1.add_attribute(cellSceneCol1,"text",1)
        treeSceneCol2.add_attribute(cellSceneCol2,"text",2)
        treeSceneCol3.add_attribute(cellSceneCol3,"text",3)
        #treeSceneCol4.add_attribute(cellSceneCol4,"text",4)
        treeSceneCol0.set_attributes(cellSceneCol0,markup=0)
        cellSceneCol3.set_alignment(0.95,0.5)

        # Scenes Chapter Selector
        adjScene = Gtk.Adjustment(1,1,100,1,1,1)
        numSceneChapter = self.getObject("numSceneChapter")
        numSceneChapter.configure(adjScene,1,0)

        # Book Details Universe List
        cmbDetailsBookUniverse  = self.getObject("cmbBookUniverse")
        cmbDetailsBookUniverse.set_model(self.bookTree.listUnivs)

        # Load Project Data
        self.bookTree.loadContent()

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

    def loadScenes(self):

        if self.projData.bookHandle == "": return

        bookPath = self.bookTree.getPath(self.projData.bookHandle)

        self.allScenes.setDataPath(bookPath)
        self.allScenes.makeList()

        self.mapSceneStore = {}
        self.mapChapters   = {}
        self.chapterCount  = {}

        self.sceneStore.clear()
        tmpItem = DataWrapper("Scene")
        self.chapterCount["1.0.00.000"] = 0
        for itemHandle in self.allScenes.dataList.keys():
            tmpItem.setDataPath(self.allScenes.dataList[itemHandle])
            tmpItem.loadDetails()

            scnNum = makeSceneNumber(1,tmpItem.section,tmpItem.chapter,tmpItem.number)
            scnSec = scnNum[:7]+"000"

            if tmpItem.section == 0:
                parIter = None
                self.chapterCount[scnSec] += 1
            else:
                if scnSec in self.mapChapters:
                    parIter = self.mapChapters[scnSec]
                    self.chapterCount[scnSec] += 1
                else:
                    if tmpItem.section == 1: scnChapter = "<b>Prologue</b>"
                    if tmpItem.section == 2: scnChapter = "<b>Chapter %d</b>" % tmpItem.chapter
                    if tmpItem.section == 3: scnChapter = "<b>Epilogue</b>"
                    parIter = self.sceneStore.append(None,[scnChapter,None,None,None,scnSec,None])
                    self.mapChapters[scnSec]  = parIter
                    self.chapterCount[scnSec] = 1

            tmpIter = self.sceneStore.append(parIter,[tmpItem.title,str(tmpItem.number),tmpItem.pov,tmpItem.words,scnNum,itemHandle])
            self.mapSceneStore[itemHandle] = tmpIter

        self.getObject("treeScenes").expand_all()

        return

    def loadBookFiles(self):

        self.fileStore.clear()

        pltSort = makeSceneNumber(0,0,0,0)
        scnSort = makeSceneNumber(0,0,0,0)
        pltIter = self.fileStore.append(None,["<b>Plot</b>",0,pltSort,""])
        scnIter = self.fileStore.append(None,["<b>Scenes</b>",0,scnSort,""])

        if self.projData.bookHandle == "": return

        bookPath = self.bookTree.getPath(self.projData.bookHandle)

        self.allScenes.setDataPath(bookPath)
        self.allScenes.makeList()

        self.mapFilesStore = {}
        self.mapChapters   = {}

        tmpItem = DataWrapper("Scene")

        for itemHandle in self.allScenes.dataList.keys():
            tmpItem.setDataPath(self.allScenes.dataList[itemHandle])
            tmpItem.loadDetails()

            scnNum = makeSceneNumber(1,tmpItem.section,tmpItem.chapter,tmpItem.number)
            scnSec = makeSceneNumber(1,tmpItem.section,tmpItem.chapter,0)

            if tmpItem.section == 0:
                parIter = scnIter
            else:
                if scnSec in self.mapChapters:
                    parIter = self.mapChapters[scnSec]
                else:
                    if tmpItem.section == 1: scnChapter = "<b>Prologue</b>"
                    if tmpItem.section == 2: scnChapter = "<b>Chapter %d</b>" % tmpItem.chapter
                    if tmpItem.section == 3: scnChapter = "<b>Epilogue</b>"
                    parIter = self.fileStore.append(scnIter,[scnChapter,None,scnSec,None])
                    self.mapChapters[scnSec] = parIter

            tmpIter = self.fileStore.append(parIter,[tmpItem.title,tmpItem.words,scnNum,itemHandle])
            self.mapSceneStore[itemHandle] = tmpIter

        self.getObject("treeMain").expand_all()

        return

    def loadUnivFiles(self, universeHandle = ""):

        self.univStore.clear()
        self.univStore.append(None,["<b>History</b>",0,"",""])
        self.univStore.append(None,["<b>Characters</b>",0,"",""])

        if universeHandle == "": return

        return

    def displayBook(self):

        self.getObject("entryBookTitle").set_text(self.projData.bookTitle)
        self.getObject("cmbBookUniverse").set_active_iter(self.bookTree.univMap[self.projData.theBook.parent])

        return

    def updateSceneDetails(self):

        self.getObject("entrySceneTitle").set_text(self.projData.fileTitle)
        self.getObject("cmbSceneSection").set_active(self.projData.theFile.section)
        self.getObject("numSceneChapter").set_value(self.projData.theFile.chapter)

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
    #  Tree Selection Actions
    ##

    def onSelectBook(self, guiObject):

        logger.debug("Select Book")
        if not self.guiLoaded: return

        (listModel, pathList) = guiObject.get_selected_rows()
        for pathItem in pathList:
            listIter   = listModel.get_iter(pathItem)
            itemHandle = listModel.get_value(listIter,3)

        if len(pathItem) == 1:
            self.getObject("treeBooks").expand_row(pathItem,False)

        if len(pathItem) == 2:
            parIter   = listModel.get_iter(pathItem[0])
            parHandle = listModel.get_value(parIter,3)
            itemPath  = self.bookTree.getPath(itemHandle)
            parPath   = self.bookTree.getPath(parHandle)
            self.projData.loadProject(itemPath,itemHandle,parPath,parHandle)
            self.displayBook()
            self.loadScenes()

        return

    def onSelectFile(self, guiObject):

        logger.debug("Select File")
        if not self.guiLoaded: return

        (listModel, pathList) = guiObject.get_selected_rows()
        for pathItem in pathList:
            listIter   = listModel.get_iter(pathItem)
            itemHandle = listModel.get_value(listIter,3)

        if itemHandle == "" or itemHandle is None: return

        # If the file is a scene, load it
        scnPath = self.allScenes.getItem(itemHandle)
        if scnPath is not None:
            self.projData.newFile("Scene")
            self.projData.loadFile(scnPath,itemHandle)
            self.getObject("mainNoteBook").set_current_page(1)

        return

    def onSelectScene(self, guiObject):

        logger.debug("Select Scene")
        if not self.guiLoaded: return

        itemHandle = ""

        (listModel, pathList) = guiObject.get_selected_rows()
        for pathItem in pathList:
            listIter   = listModel.get_iter(pathItem)
            itemHandle = listModel.get_value(listIter,5)

        if itemHandle == "" or itemHandle is None: return

        itemPath = self.allScenes.getItem(itemHandle)
        self.projData.newFile("Scene")
        self.projData.loadFile(itemPath,itemHandle)
        self.updateSceneDetails()

        return

    ##
    #  Button Actions
    ##

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

    ##
    #  Scene Settings Action Buttons
    ##

    def onSceneAdd(self, guiObject):

        if self.projData.bookHandle == "": return

        scnSort  = makeSceneNumber(1,0,0,0)
        sceneNum = self.chapterCount[scnSort] + 1

        self.projData.newFile("Scene")
        self.projData.createFile("New Scene")
        self.projData.setFileParent("Book")
        self.projData.setFileNumber(sceneNum)
        self.projData.saveFile()

        self.loadScenes()
        if self.getObject("sideNoteBook").get_current_page() == 1:
            self.loadBookFiles()

        return

    def onSceneRemove(self, guiObject):
        return

    def onSceneUp(self, guiObject):
        return

    def onSceneDown(self, guiObject):
        return

    def onSceneSave(self, guiObject):

        logger.debug("Scene save clicked")

        prevSection = self.projData.theFile.section
        prevChapter = self.projData.theFile.chapter
        prevNumber  = self.projData.theFile.number

        scnTitle    = self.getObject("entrySceneTitle").get_text()
        scnSection  = self.getObject("cmbSceneSection").get_active()
        scnChapter  = self.getObject("numSceneChapter").get_value()
        scnPOV      = self.getObject("cmbSceneCharacter").get_active_text()

        if scnSection != 2: scnChapter = 1

        scnSort = makeSceneNumber(1,scnSection,scnChapter,0)
        if scnSort in self.chapterCount:
            if scnSection == prevSection and scnChapter == prevChapter:
                scnNumber = prevNumber
            else:
                scnNumber = self.chapterCount[scnSort] + 1
        else:
            scnNumber = 1

        self.projData.setSceneSettings(scnTitle,scnSection,scnChapter,scnNumber,scnPOV,"")
        self.projData.saveFile()

        self.loadScenes()
        if self.getObject("sideNoteBook").get_current_page() == 1:
            self.loadBookFiles()

        return

    ##
    #  Main Window Events
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
            self.loadBookFiles()
        if tabIdx == 2:
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
