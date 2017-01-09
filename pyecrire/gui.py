# -*- coding: utf-8 -*

##
#  pyÉcrire – Main GUI Class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Sets up the main GUI and holds action and event functions
##

import logging as logger
#import pyecrire

import gi
gi.require_version("Gtk","3.0")
gi.require_version("WebKit","3.0")

from gi.repository      import Gtk, GLib, WebKit
from time               import sleep
from pyecrire           import *
from pyecrire.project   import Project
from pyecrire.editor    import Editor
from pyecrire.timer     import Timer
from pyecrire.treeviews import ProjectTree, BookTree, UniverseTree, SceneTree, FileVersionTree, TimeTree
from pyecrire.functions import makeTimeStamp, makeSceneNumber
from pyecrire.dialogs   import SelectDialog

class GUI():

    def __init__(self):

        self.guiLoaded  = False

        # Define Core Objects
        self.mainConf   = CONFIG
        self.projData   = Project()

        # Initialise GUI
        self.guiBuilder = BUILDER
        self.guiBuilder.add_from_file("pyecrire/gui/winMain.glade")

        self.getObject  = self.guiBuilder.get_object
        self.winMain    = self.getObject("winMain")

        # Prepare GUI Classes
        self.guiTimer  = Timer()
        self.webEditor = Editor(self.guiTimer)
        self.projTree  = ProjectTree()
        self.bookTree  = BookTree()
        self.univTree  = UniverseTree()
        self.scneTree  = SceneTree()
        self.fileTree  = FileVersionTree()
        self.timeTree  = TimeTree()

        # Connect Editable Tree Cells
        self.bookTree.editCell.connect("edited",self.onEditBookFileTitle)

        # Set Up Event Handlers
        guiHandlers = {
            "onDestroyWindow"          : self.onGuiDestroy,
            "onEventKeyPress"          : self.onWinKeyPress,
            "onEventWinChange"         : self.onWinChange,
            "onSwitchPageMainNoteBook" : self.onMainTabChange,
            "onSwitchPageSideNoteBook" : self.onSideTabChange,
            "onClickNew"               : self.onNewProject,
            "onClickSave"              : self.onFileSave,
            "onChangeTreeProject"      : self.onSelectProjectTree,
            "onChangeTreeBook"         : self.onSelectBookTree,
            "onChangeTreeUniverse"     : self.onSelectUniverseTree,
            "onChangeTreeScenes"       : self.onSelectSceneTree,
            "onChangeTreeFileVersion"  : self.onSelectFileTree,
            "onToggleEditable"         : self.webEditor.onToggleEditable,
            "onClickEditReload"        : self.onFileReload,
            "onClickEditCopy"          : self.webEditor.onEditCopy,
            "onClickEditCut"           : self.webEditor.onEditCut,
            "onClickEditPaste"         : self.webEditor.onEditPaste,
            "onClickEditUndo"          : self.webEditor.onEditAction,
            "onClickEditRedo"          : self.webEditor.onEditAction,
            "onClickEditBold"          : self.webEditor.onEditAction,
            "onClickEditItalic"        : self.webEditor.onEditAction,
            "onClickEditUnderline"     : self.webEditor.onEditAction,
            "onClickEditStrikeThrough" : self.webEditor.onEditAction,
            "onClickEditLeft"          : self.webEditor.onEditAction,
            "onClickEditCentre"        : self.webEditor.onEditAction,
            "onClickEditRight"         : self.webEditor.onEditAction,
            "onClickEditJustify"       : self.webEditor.onEditAction,
            "onClickEditStrip"         : self.webEditor.onEditStripFormatting,
            "onClickTimerStart"        : self.webEditor.onTimerStart,
            "onClickTimerPause"        : self.webEditor.onTimerPause,
            "onClickTimerStop"         : self.webEditor.onTimerStop,
            "onClickBookAddFile"       : self.onBookAddFile,
            "onClickUniverseAddFile"   : self.onUniverseAddFile,
            "onClickSceneAdd"          : self.onSceneAdd,
            "onClickSceneRemove"       : self.onSceneRemove,
            "onClickSceneUp"           : self.onSceneUp,
            "onClickSceneDown"         : self.onSceneDown,
            "onClickSceneSave"         : self.onSceneSave,
            "onToggleNewUniverse"      : self.onToggleNewUniverse,
            "onMenuActionHelpAbout"    : self.onActionShowAbout,
            "onMenuActionFileSave"     : self.onFileSave,
            "onMenuActionFileQuit"     : self.onGuiDestroy,
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
        self.autoTaskID = GLib.timeout_add_seconds(self.mainConf.autoSave,self.doAutoTasks)

        ##
        #  Content
        ##

        # Gtk ListStore and TreeStore
        self.bookType   = Gtk.ListStore(str)

        # Scenes Chapter Selector
        adjScene = Gtk.Adjustment(1,1,100,1,1,1)
        numSceneChapter = self.getObject("numSceneChapter")
        numSceneChapter.configure(adjScene,1,0)

        # Book Details Universe List
        cmbDetailsBookUniverse  = self.getObject("cmbBookUniverse")
        cmbDetailsBookUniverse.set_model(self.projTree.listUnivs)

        ##
        #  Finalise GUI Setup
        ##

        # Load Project Data
        self.projTree.loadContent()
        self.bookTree.loadContent(None)
        self.univTree.loadContent(None)

        # Prepare Main Window
        self.winMain.set_title(self.mainConf.appName)
        self.winMain.resize(self.mainConf.winWidth,self.mainConf.winHeight)
        self.winMain.set_position(Gtk.WindowPosition.CENTER)
        self.winMain.show_all()

        self.guiLoaded = True

        return

    # Close Program
    def onGuiDestroy(self, guiObject):

        logger.debug("Exiting")

        self.mainConf.setWinPane(self.guiPaned.get_position())
        self.mainConf.saveConfig()
        self.webEditor.doAutoSave()
        self.webEditor.onTimerStop()

        Gtk.main_quit()

        return

    # Automated Tasks
    def doAutoTasks(self):

        statusBar = self.getObject("mainStatus")
        statusCID = self.statusBar.get_context_id("File")

        if self.mainConf.doAutoSaveConfig():
            statusBar.push(statusCID,makeTimeStamp(4)+"Config auto-saved")

        if self.webEditor.doAutoSave():
            self.updateWordCount()
            self.fileTree.loadContent(self.webEditor.theFile.fileList)
            statusBar.push(statusCID,makeTimeStamp(4)+"File auto-saved")

        return True

    ##
    #  Main NoteBook Content Functions
    ##

    def loadBook(self):

        self.webEditor.doAutoSave()
        self.webEditor.clearEditor()
        self.scneTree.loadContent(self.projData.bookPath)
        self.fileTree.clearTree()
        self.updateTitle()
        self.updateStatusFile()

        self.getObject("entryBookTitle").set_text(self.projData.bookTitle)
        self.getObject("cmbBookUniverse").set_active_iter(self.projTree.univMap[self.projData.theBook.parent])
        self.getObject("mainNoteBook").set_current_page(TABM_BOOK)

        return

    def saveBook(self):

        bookTitle      = self.getObject("entryBookTitle").get_text()
        chkNewUniverse = self.getObject("chkNewUniverse")

        self.projData.setupBook(bookTitle)

        if chkNewUniverse.get_active():
            univTitle = self.getObject("entryBookUniverse").get_text()
            self.projData.setupUniverse(univTitle)
        else:
            univIdx  = self.getObject("cmbBookUniverse").get_active()
            univItem = self.projTree.listUnivs[univIdx]
            self.projData.setUniverse(univItem[1],self.projTree.getPath(univItem[1]))

        self.projData.saveProject()

        if self.getObject("sideNoteBook").get_current_page() == TABS_PROJ:
            self.projTree.loadContent()

        return

    def loadUniverse(self):
        return

    def saveUniverse(self):
        return

    def loadEditor(self, fileGroup, fileHandle, doWordCount=True):

        if fileGroup == NAME_BOOK:
            filePath = self.bookTree.getPath(fileHandle)
            fileType = self.bookTree.getType(fileHandle)

        if fileGroup == NAME_UNIV:
            filePath = self.univTree.getPath(fileHandle)
            fileType = self.univTree.getType(fileHandle)

        if filePath is not None:
            self.webEditor.doAutoSave()
            self.webEditor.loadFile(fileType,filePath,fileHandle,doWordCount)
            self.fileTree.loadContent(self.webEditor.theFile.fileList)
            self.timeTree.loadContent(self.webEditor.theFile.timeList)
            self.getObject("mainNoteBook").set_current_page(TABM_EDIT)
            self.updateStatusFile()

        if doWordCount:
            self.updateWordCount()

        return

    def saveEditor(self):

        self.webEditor.saveFile()
        self.fileTree.loadContent(self.webEditor.theFile.fileList)
        self.updateWordCount()

        return

    def loadSource(self):
        return

    def saveSource(self):
        return

    ##
    #  Update GUI
    ##

    def updateTitle(self):
        self.getObject("lblBookTitle").set_label(self.projData.bookTitle)
        return

    def updateStatusFile(self):

        fileTitle = self.webEditor.theFile.title
        bookTitle = self.projData.bookTitle
        univTitle = self.projData.univTitle

        if fileTitle == "":
            currFile = bookTitle
        else:
            if self.projData.theFile.parType == NAME_BOOK:
                currFile = bookTitle+" > "+fileTitle
            else:
                currFile = univTitle+" > "+fileTitle

        self.getObject("lblCurrFile").set_label("File: "+currFile)

        return

    def updateWordCount(self):

        wordCount  = self.webEditor.theFile.words
        fileHandle = self.webEditor.fileHandle

        # Update Trees
        self.scneTree.setValue(fileHandle,self.scneTree.COL_WORDS,wordCount)
        self.scneTree.sumWords()

        if self.webEditor.theFile.parType == NAME_BOOK:
            self.bookTree.setValue(fileHandle,self.bookTree.COL_WORDS,wordCount)
            self.bookTree.sumWords()

        if self.webEditor.theFile.parType == NAME_UNIV:
            self.univTree.setValue(fileHandle,self.univTree.COL_WORDS,wordCount)
            self.univTree.sumWords()

        # Update Info Panel
        self.getObject("lblWCTotWords").set_label(str(self.webEditor.theFile.words))
        self.getObject("lblWCTotChars").set_label(str(self.webEditor.theFile.chars))
        self.getObject("lblWCSesWords").set_label(str(self.webEditor.theFile.words - self.webEditor.theFile.prevWords))
        self.getObject("lblWCSesChars").set_label(str(self.webEditor.theFile.chars - self.webEditor.theFile.prevChars))

        return

    ##
    #  Tree Selection Actions
    ##

    def onSelectProjectTree(self, guiObject):

        logger.debug("Select Project")
        if not self.guiLoaded: return

        pathItem = []

        (listModel, pathList) = guiObject.get_selected_rows()
        for pathItem in pathList:
            listIter   = listModel.get_iter(pathItem)
            itemHandle = listModel.get_value(listIter,3)

        if len(pathItem) == 1:
            self.getObject("treeProject").expand_row(pathItem,False)

        if len(pathItem) == 2:
            parIter   = listModel.get_iter(pathItem[0])
            parHandle = listModel.get_value(parIter,3)
            itemPath  = self.projTree.getPath(itemHandle)
            parPath   = self.projTree.getPath(parHandle)
            self.projData.loadProject(itemPath,itemHandle,parPath,parHandle)
            self.loadBook()

        return

    def onSelectBookTree(self, guiObject):

        logger.debug("Select Book File")
        if not self.guiLoaded: return

        itemHandle = ""

        (listModel, pathList) = guiObject.get_selected_rows()
        for pathItem in pathList:
            listIter   = listModel.get_iter(pathItem)
            itemHandle = listModel.get_value(listIter,3)

        if itemHandle == "" or itemHandle is None: return

        self.loadEditor(NAME_BOOK,itemHandle)

        return

    def onSelectUniverseTree(self, guiObject):

        logger.debug("Select Universe File")
        if not self.guiLoaded: return

        itemHandle = ""

        (listModel, pathList) = guiObject.get_selected_rows()
        for pathItem in pathList:
            listIter   = listModel.get_iter(pathItem)
            itemHandle = listModel.get_value(listIter,3)

        if itemHandle == "" or itemHandle is None: return

        self.loadEditor(NAME_UNIV,itemHandle)

        return

    def onSelectSceneTree(self, guiObject):

        logger.debug("Select Scene")
        if not self.guiLoaded: return

        itemHandle = ""

        (listModel, pathList) = guiObject.get_selected_rows()
        for pathItem in pathList:
            listIter   = listModel.get_iter(pathItem)
            itemHandle = listModel.get_value(listIter,5)

        if itemHandle == "" or itemHandle is None: return

        filePath = self.scneTree.getPath(itemHandle)
        self.projData.initFile(NAME_SCNE)
        self.projData.loadFile(filePath,itemHandle)

        # Load Form Details
        self.getObject("entrySceneTitle").set_text(self.projData.fileTitle)
        self.getObject("cmbSceneSection").set_active(self.projData.theFile.section)
        self.getObject("numSceneChapter").set_value(self.projData.theFile.chapter)

        return

    def onSelectFileTree(self, guiObject):

        logger.debug("Select File Version")
        if not self.guiLoaded: return

        itemHandle = ""

        (listModel, pathList) = guiObject.get_selected_rows()
        for pathItem in pathList:
            listIter   = listModel.get_iter(pathItem)
            itemHandle = listModel.get_value(listIter,1)

        if itemHandle == "" or itemHandle is None: return

        itemPath = self.webEditor.theFile.getFilePath(itemHandle)

        self.webEditor.doAutoSave()
        self.webEditor.loadFileVersion(itemPath)
        self.webEditor.setEditable(False)

        return

    ##
    #  Button Actions
    ##

    def onNewProject(self, guiObject=None):

        self.projData.newProject()
        self.scneTree.clearContent()

        self.getObject("entryBookTitle").set_text("")
        self.getObject("entryBookUniverse").set_text("")
        self.getObject("treeProjectSelect").unselect_all()
        self.getObject("entryBookUniverse").set_can_focus(False)
        self.getObject("mainNoteBook").set_current_page(TABM_BOOK)

        return

    def onFileSave(self, guiObject=None):

        logger.debug("Saving")

        mainIdx = self.getObject("mainNoteBook").get_current_page()

        if mainIdx == TABM_BOOK: self.saveBook()
        if mainIdx == TABM_UNIV: self.saveUniverse()
        if mainIdx == TABM_EDIT: self.saveEditor()

        return

    def onFileReload(self, guiObject=None):

        #self.saveEditor()
        self.loadEditor(self.webEditor.theFile.parType,self.webEditor.fileHandle,False)

        return

    def onToggleNewUniverse(self, guiObject):
        if guiObject.get_active():
            self.getObject("entryBookUniverse").set_can_focus(True)
        else:
            self.getObject("entryBookUniverse").set_can_focus(False)
        return

    ##
    #  Menu Action
    ##

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
    #  Book Files Action Buttons
    ##

    def onBookAddFile(self, guiObject):

        if self.projData.bookHandle == "": return

        logger.debug("Add book file")

        guiDialog = SelectDialog("Select file type",["Plot","Scene"],[NUM_PLOT,NUM_SCNE])
        dlgReturn = guiDialog.run()
        guiDialog.destroy()

        if dlgReturn == Gtk.ResponseType.CANCEL: return
        if dlgReturn == NUM_SCNE: self.onSceneAdd()

        if dlgReturn == NUM_PLOT:
            self.projData.initFile(NAME_PLOT)
            self.projData.setupFile("New Plot")
            self.projData.setFileNumber(self.bookTree.getCount(NAME_PLOT)+1)
            self.projData.setFileParent(NAME_BOOK)
            self.projData.saveFile()
            self.bookTree.loadContent(self.projData.bookPath)

        return

    def onUniverseAddFile(self, guiObject):

        if self.projData.univHandle == "": return

        logger.debug("Add universe file")

        guiDialog = SelectDialog("Select file type",["History","Character"],[NUM_HIST,NUM_CHAR])
        dlgReturn = guiDialog.run()
        guiDialog.destroy()

        if dlgReturn == Gtk.ResponseType.CANCEL: return

        if dlgReturn == NUM_HIST: fileType = NAME_HIST
        if dlgReturn == NUM_CHAR: fileType = NAME_CHAR

        self.projData.initFile(fileType)
        self.projData.setupFile("New "+fileType)
        self.projData.setFileNumber(self.univTree.getCount(fileType)+1)
        self.projData.setFileParent(NAME_UNIV)
        self.projData.saveFile()
        self.univTree.loadContent(self.projData.univPath)

        return

    def onEditBookFileTitle(self, guiObject, rowPath, editValue):

        logger.debug("Edit book file title")

        treeSelect = self.getObject("treeBookSelect")
        itemIter   = self.bookTree.treeSort.get_iter(rowPath)
        itemHandle = self.bookTree.treeSort.get_value(itemIter,self.bookTree.COL_HANDLE)
        itemPath   = self.bookTree.getPath(itemHandle)
        itemType   = self.bookTree.getType(itemHandle)

        self.bookTree.setValue(itemHandle,self.bookTree.COL_TITLE,editValue)
        self.projData.initFile(itemType)
        self.projData.loadFile(itemPath,itemHandle)
        self.projData.setFileTitle(editValue)
        if itemType == NAME_PLOT: self.bookTree.allPlots.makeList()
        if itemType == NAME_SCNE: self.bookTree.allScenes.makeList()

        if itemType == NAME_SCNE:
            self.scneTree.loadContent(self.projData.bookPath)

        return

    ##
    #  Scene Settings Action Buttons
    ##

    def onSceneAdd(self, guiObject=None):

        if self.projData.bookHandle == "": return

        scnSort  = makeSceneNumber(1,0,0,0)
        sceneNum = self.scneTree.chapCount[scnSort] + 1

        self.projData.initFile(NAME_SCNE)
        self.projData.setupFile("New Scene")
        self.projData.setFileParent(NAME_BOOK)
        self.projData.setFileNumber(sceneNum)
        self.projData.saveFile()

        self.scneTree.loadContent(self.projData.bookPath)
        if self.getObject("sideNoteBook").get_current_page() == TABS_BOOK:
            self.bookTree.loadContent(self.projData.bookPath)

        return

    def onSceneRemove(self, guiObject=None):
        return

    def onSceneUp(self, guiObject=None):
        return

    def onSceneDown(self, guiObject=None):
        return

    def onSceneSave(self, guiObject=None):

        logger.debug("Scene save clicked")

        prevSection = self.projData.theFile.section
        prevChapter = self.projData.theFile.chapter
        prevNumber  = self.projData.theFile.number

        scnTitle    = self.getObject("entrySceneTitle").get_text()
        scnSection  = self.getObject("cmbSceneSection").get_active()
        scnChapter  = self.getObject("numSceneChapter").get_value()
        scnPOV      = self.getObject("cmbSceneCharacter").get_active_text()

        if scnSection != 2: scnChapter = 0

        scnSort = makeSceneNumber(GRP_SCNE,scnSection,scnChapter,0)
        if scnSort in self.scneTree.chapCount:
            if scnSection == prevSection and scnChapter == prevChapter:
                scnNumber = prevNumber
            else:
                scnNumber = self.scneTree.chapCount[scnSort] + 1
        else:
            scnNumber = 1

        self.projData.setSceneSettings(scnTitle,scnSection,scnChapter,scnNumber,scnPOV,"")
        self.projData.saveFile()

        self.scneTree.loadContent(self.projData.bookPath)
        if self.getObject("sideNoteBook").get_current_page() == TABS_BOOK:
            self.bookTree.loadContent(self.projData.bookPath)

        return

    ##
    #  Tab Changes
    ##

    def onMainTabChange(self, guiObject, guiChild, tabIdx):

        logger.debug("Main tab change")

        if tabIdx != TABM_EDIT:
            self.webEditor.setEditable(False)

        if tabIdx == TABM_SRCE:
            logger.debug("Source View")
            textSource = self.getObject("textSource")
            textBuffer = textSource.get_buffer()
            srcText    = self.webEditor.getText()
            textBuffer.set_text(srcText)

        return

    def onSideTabChange(self, guiObject, guiChild, tabIdx):

        logger.debug("Side tab change")

        if tabIdx == TABS_PROJ:
            self.getObject("mainNoteBook").set_current_page(TABM_BOOK)
        if tabIdx == TABS_BOOK:
            self.bookTree.loadContent(self.projData.bookPath)
        if tabIdx == TABS_UNIV:
            self.univTree.loadContent(self.projData.univPath)

        return

    ##
    #  Main Window Events
    ##

    def onWinKeyPress(self, guiObject, guiEvent):
        #self.guiTimer.resetAutoPause()
        return

    def onWinChange(self, guiObject, guiEvent):
        self.mainConf.setWinSize(guiEvent.width,guiEvent.height)
        return

# End Class GUI
