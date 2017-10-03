# -*- coding: utf-8 -*
"""novelWriter Main GUI Class

novelWriter – Main GUI Class
============================
Sets up the main GUI and holds action and event functions

File History:
Created: 2017-01-10 [0.1.0]

"""

import logging
import nw
import gi
gi.require_version("Gtk","3.0")

from gi.repository   import Gtk, GLib
from time            import sleep
from os              import path
# from nw.functions    import getIconWidget, formatDateTime, dateFromStamp, makeSortString
# from nw.editor       import Editor
# from nw.dialogs      import EditBookDialog
# from nw.scenetree    import SceneTree
# from nw.timer        import Timer
# from nw.book         import Book
# from nw.statusbar    import StatusBar
# from nw.bookoverview import BookOverview
# from nw.scenebuffer  import SceneBuffer

logger  = logging.getLogger(__name__)

class GUI():

    def __init__(self):

        self.guiLoaded    = False

        # Define Core Objects
        self.mainConf     = nw.CONFIG
        self.guiBuilder   = nw.BUILDER

        # Build the GUI
        logger.debug("Assembling the main GUI")
        self.getObject    = self.guiBuilder.get_object
        self.winMain      = self.getObject("winMain")
        
        # Prepare GUI Classes
        # self.theBook      = Book()
        # self.guiTimer     = Timer(self.theBook)
        # self.statusBar    = StatusBar()
        # self.webEditor    = Editor(self.guiTimer,self.statusBar)
        # self.sceneTree    = SceneTree()
        # self.sceneBuffer  = SceneBuffer(self.theBook)
        # self.bookOverview = BookOverview(self.theBook)

        # Runtime Properties
        self.currHandle   = ""

        # Set Up Event Handlers
        guiHandlers = {
            # Main GUI
            # "onClickNew"               :  self.onNewBook,
            # "onClickOpen"              :  self.onOpenBook,
            # "onClickSave"              :  self.onSaveBook,
            # "onClickEdit"              :  self.onEditBook,
            # "onClickPreferences"       :  self.mainConf.onLoad,
            # "onClickSceneAdd"          :  self.onSceneAdd,
            # "onClickSceneRemove"       :  self.onSceneRemove,
            # "onClickSceneMoveUp"       :  self.onSceneMoveUp,
            # "onClickSceneMoveDown"     :  self.onSceneMoveDown,
            # "onSelectTreeScene"        :  self.onSceneSelect,
            # "onMainTabChange"          :  self.onMainTabChange,
            "onMainWinDestroy"         :  self.onGuiDestroy,
            # "onMainWinChange"          :  self.onWinChange,
            # Main Menu
            # "onMenuFileNew"            :  self.onNewBook,
            # "onMenuFileOpen"           :  self.onOpenBook,
            # "onMenuFileSave"           :  self.onSaveBook,
            # "onMenuFileQuit"           :  self.onGuiDestroy,
            # "onMenuEditPastePlain"     : (self.webEditor.onEditPasteProcess,nw.PASTE_PLAIN),
            # "onMenuEditPasteClean"     : (self.webEditor.onEditPasteProcess,nw.PASTE_CLEAN),
            # "onMenuEditBook"           :  self.onEditBook,
            # "onMenuEditPreferences"    :  self.mainConf.onLoad,
            # "onMenuViewBookOverview"   :  self.onViewBookOverview,
            # "onMenuViewSceneBuffer"    :  self.onViewSceneBuffer,
            # "onMenuHelpAbout"          :  self.onShowAbout,
            # Main Menu Recent List
            # "onMenuRecent0"            : (self.onOpenRecent,0),
            # "onMenuRecent1"            : (self.onOpenRecent,1),
            # "onMenuRecent2"            : (self.onOpenRecent,2),
            # "onMenuRecent3"            : (self.onOpenRecent,3),
            # "onMenuRecent4"            : (self.onOpenRecent,4),
            # "onMenuRecent5"            : (self.onOpenRecent,5),
            # "onMenuRecent6"            : (self.onOpenRecent,6),
            # "onMenuRecent7"            : (self.onOpenRecent,7),
            # "onMenuRecent8"            : (self.onOpenRecent,8),
            # "onMenuRecent9"            : (self.onOpenRecent,9),
            # WebKit Editor Signals
            # "onToggleEditable"         :  self.webEditor.onToggleEditable,
            # "onClickEditRefresh"       :  self.webEditor.onEditRefresh,
            # "onClickEditUndo"          : (self.webEditor.onEditAction,"undo"),
            # "onClickEditRedo"          : (self.webEditor.onEditAction,"redo"),
            # "onClickEditCut"           :  self.webEditor.onEditCut,
            # "onClickEditCopy"          :  self.webEditor.onEditCopy,
            # "onClickEditPaste"         :  self.webEditor.onEditPaste,
            # "onClickEditInsertPara"    : (self.webEditor.onEditFormat,"p"),
            # "onClickEditBold"          : (self.webEditor.onEditAction,"bold"),
            # "onClickEditItalic"        : (self.webEditor.onEditAction,"italic"),
            # "onClickEditUnderline"     : (self.webEditor.onEditAction,"underline"),
            # "onClickEditStrikethrough" : (self.webEditor.onEditAction,"strikethrough"),
            # "onToggleShowPara"         :  self.webEditor.onShowParagraphs,
            # "onToggleSpellCheck"       :  self.webEditor.onToggleSpellCheck,
        }
        self.guiBuilder.connect_signals(guiHandlers)

        # Set Pane Positions
        # self.getObject("panedContent").set_position(self.mainConf.mainPane)
        # self.getObject("panedSide").set_position(self.mainConf.sidePane)

        # Prepare Editor
        # self.getObject("scrollEditor").add(self.webEditor)
        # self.getObject("textSource").set_editable(False)

        # Custom Icons
        # self.getObject("btnEditInsertPara").set_icon_widget(getIconWidget("icon-paragraph",24))
        # self.getObject("btnMainNew").set_icon_widget(getIconWidget("icon-book-new",28))

        # Set Up Timers
        # self.timerID    = GLib.timeout_add(200,self.onTick)
        # self.autoTaskID = GLib.timeout_add_seconds(self.mainConf.autoSave,self.doAutoTasks)

        ##
        #  Content
        ##

        # Scene Chapter Selector
        # adjScene = Gtk.Adjustment(1,1,100,1,1,1)
        # numSceneChapter = self.getObject("numSceneChapter")
        # numSceneChapter.configure(adjScene,1,0)

        ##
        #  Finalise GUI Setup
        ##

        # Remove Widgets Not In Use Yet
        # boxDetails = self.getObject("boxDetails")
        # boxDetails.remove(self.getObject("boxCharsNTime"))

        # Prepare Main Window
        self.winMain.set_title(self.mainConf.appName)
        self.winMain.resize(self.mainConf.winWidth,self.mainConf.winHeight)
        self.winMain.set_position(Gtk.WindowPosition.CENTER)
        self.winMain.show_all()

        # Load Last Book
        # self.loadBook()

        self.guiLoaded = True

        return

    def clearContent(self):

        self.webEditor.clearEditor()
        self.guiTimer.resetTimer()

        tmpBuffer = self.getObject("textSceneSummary").get_buffer()
        tmpBuffer.set_text("")

        self.getObject("lblSceneTitle").set_label("No file loaded")
        self.getObject("lblSceneCreated").set_label("Created")
        self.getObject("lblSceneUpdated").set_label("Updated")
        self.getObject("lblSceneVersion").set_label("")
        self.getObject("entrySceneTitle").set_text("")
        self.getObject("cmbSceneSection").set_active(0)
        self.getObject("numSceneChapter").set_value(1)

        return

    ##
    #  Book Functions
    ##

    def loadBook(self, bookFolder=None):

        if bookFolder is None:
            bookFolder = self.mainConf.getLastBook()

        if bookFolder == "":
            return

        logger.debug("GUI.loadBook: Loading book")

        self.clearContent()
        self.theBook.loadBook(bookFolder)
        self.sceneTree.loadContent(self.theBook)
        self.updateWindowTitle()

        recentHandle = self.theBook.getBookRecent()
        if not recentHandle == "":
            self.loadScene(recentHandle)

        self.statusBar.setActiveFile(self.theBook,"")

        return

    def saveBook(self):

        if self.theBook.bookLoaded:
            logger.debug("GUI.saveBook: Saving book")
            self.theBook.saveBook()

        return

    ##
    #  Scene Functions
    ##

    def loadScene(self, sceneHandle):

        logger.debug("GUI.loadScene: Loading scene")

        # Load Scene and Update Editor
        self.currHandle = sceneHandle
        self.theBook.setCurrHandle(self.currHandle)
        self.theBook.loadScene(self.currHandle)
        self.webEditor.loadText(self.theBook,self.currHandle)

        # Load Summary
        scnSummary = self.theBook.getSceneSummary(self.currHandle)
        tmpBuffer  = self.getObject("textSceneSummary").get_buffer()
        tmpBuffer.set_text(scnSummary)

        # Load Scene Data
        scnTitle   = self.theBook.getSceneTitle(self.currHandle)
        scnSection = self.theBook.getSceneSection(self.currHandle)
        scnChapter = self.theBook.getSceneChapter(self.currHandle)
        scnCreated = "Created "+formatDateTime(
            nw.DATE_DATE,dateFromStamp(self.theBook.getSceneCreated(self.currHandle)))
        scnUpdated = "Updated "+formatDateTime(
            nw.DATE_DATE,dateFromStamp(self.theBook.getSceneUpdated(self.currHandle)))
        scnVersion = "Draft %d, Version %d" % (
            self.theBook.getBookDraft(),self.theBook.getSceneVersion(self.currHandle))

        # Set GUI Elements
        self.getObject("lblSceneTitle").set_label(scnTitle)
        self.getObject("lblSceneCreated").set_label(scnCreated)
        self.getObject("lblSceneUpdated").set_label(scnUpdated)
        self.getObject("lblSceneVersion").set_label(scnVersion)
        self.getObject("entrySceneTitle").set_text(scnTitle)
        self.getObject("cmbSceneSection").set_active(scnSection)
        self.getObject("numSceneChapter").set_value(scnChapter)

        self.updateWordCount()
        self.statusBar.setActiveFile(self.theBook,self.currHandle)

        return

    def saveScene(self):

        logger.debug("GUI.saveScene: Saving scene")

        # Get Scene Values
        prevSection = self.theBook.getSceneSection(self.currHandle)
        prevChapter = self.theBook.getSceneChapter(self.currHandle)
        prevNumber  = self.theBook.getSceneNumber(self.currHandle)
        scnTitle    = self.getObject("entrySceneTitle").get_text()
        scnSection  = self.getObject("cmbSceneSection").get_active()
        scnChapter  = self.getObject("numSceneChapter").get_value()
        scnChapter  = int(scnChapter)

        if scnSection != 2: scnChapter = 0

        scnSort = makeSortString(scnSection,scnChapter,0)
        if scnSort in self.sceneTree.chapCount:
            if scnSection == prevSection and scnChapter == prevChapter:
                scnNumber = prevNumber
            else:
                scnNumber = self.sceneTree.chapCount[scnSort] + 1
        else:
            scnNumber = 1

        # Get Summary Text
        tmpBuffer  = self.getObject("textSceneSummary").get_buffer()
        tmpStart   = tmpBuffer.get_start_iter()
        tmpEnd     = tmpBuffer.get_end_iter()
        scnSummary = tmpBuffer.get_text(tmpStart,tmpEnd,True)

        # Set Scene Data
        self.theBook.setSceneTitle(self.currHandle,scnTitle)
        self.theBook.setSceneSection(self.currHandle,scnSection)
        self.theBook.setSceneChapter(self.currHandle,scnChapter)
        self.theBook.setSceneNumber(self.currHandle,scnNumber)
        self.theBook.setSceneSummary(self.currHandle,scnSummary)

        refreshTree = self.theBook.getSceneChanged(self.currHandle)

        self.webEditor.saveText()
        self.theBook.saveScene(self.currHandle)
        self.updateWordCount()

        if refreshTree:
            self.theBook.makeSceneIndex()
            self.sceneTree.loadContent(self.theBook)

        return

    ##
    #  Source View
    ##

    def loadSourceView(self):

        scnText   = self.webEditor.getText()
        tmpBuffer = self.getObject("textSource").get_buffer()
        tmpBuffer.set_text(scnText)

        return

    ##
    #  Update Functions
    ##

    def updateWordCount(self):

        wordCount    = self.theBook.getSceneWords(self.currHandle)
        sessionWords = str(wordCount[nw.COUNT_ADDED])
        totalWords   = str(wordCount[nw.COUNT_LATEST])

        self.getObject("lblWordsSessionValue").set_label(sessionWords)
        self.getObject("lblWordsTotalValue").set_label(totalWords)

        self.sceneTree.setValue(self.currHandle,self.sceneTree.COL_WORDS,totalWords)
        self.sceneTree.sumWords()

        return

    def updateWindowTitle(self):

        appName   = self.mainConf.appName
        bookTitle = self.theBook.getBookTitle()
        bookDraft = self.theBook.getBookDraft()

        if self.theBook.bookLoaded:
            winTitle = "%s - %s (Draft %d)" % (appName,bookTitle,bookDraft)
            self.getObject("winMain").set_title(winTitle)

        return

    ##
    #  Main ToolBar Button Events
    ##

    def onNewBook(self, guiObject):

        guiDialog = EditBookDialog(ACTION_NEW)

        dlgReturn = guiDialog.run()
        if dlgReturn == Gtk.ResponseType.ACCEPT:
            bookTitle  = guiDialog.entryBookTitle.get_text()
            bookAuthor = guiDialog.entryBookAuthor.get_text()
            rootFolder = guiDialog.fileBookPath.get_filename()

            self.theBook.setBookTitle(bookTitle)
            self.theBook.setBookAuthor(bookAuthor)
            self.theBook.createBook(rootFolder)
            self.loadBook(self.theBook.getBookFolder())

        guiDialog.destroy()

        return

    def onOpenBook(self, guiObject):

        guiDialog = Gtk.FileChooserDialog("Open Book Folder",self.winMain,
            Gtk.FileChooserAction.SELECT_FOLDER,(
                Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OPEN,   Gtk.ResponseType.OK
            )
        )
        guiDialog.set_default_response(Gtk.ResponseType.OK)

        dlgReturn = guiDialog.run()
        if dlgReturn == Gtk.ResponseType.OK:
            self.loadBook(guiDialog.get_filename())

        guiDialog.destroy()

        return

    def onOpenRecent(self, guiObject, recentIdx):
        logger.debug("GUI.onOpenRecent: Open recent book %d" % recentIdx)
        self.loadBook(self.mainConf.recentBook[recentIdx])
        return

    def onSaveBook(self, guiObject):
        self.saveBook()
        self.saveScene()
        return

    def onEditBook(self, guiObject):

        guiDialog = EditBookDialog(ACTION_EDIT)
        guiDialog.entryBookTitle.set_text(self.theBook.getBookTitle())
        guiDialog.entryBookAuthor.set_text(self.theBook.getBookAuthor())
        guiDialog.entryBookPath.set_text(self.theBook.getBookFolder())

        dlgReturn = guiDialog.run()
        if dlgReturn == Gtk.ResponseType.ACCEPT:
            bookTitle  = guiDialog.entryBookTitle.get_text()
            bookAuthor = guiDialog.entryBookAuthor.get_text()
            self.theBook.setBookTitle(bookTitle)
            self.theBook.setBookAuthor(bookAuthor)
            self.saveBook()
            self.updateWindowTitle()

        guiDialog.destroy()

        return

    ##
    #  Scene ToolBar Button Events
    ##

    def onSceneAdd(self, guiObject):

        scnSort  = makeSortString(0,0,0)
        sceneNum = self.sceneTree.chapCount[scnSort] + 1
        self.theBook.createScene("New Scene",sceneNum)
        self.sceneTree.loadContent(self.theBook)

        return

    def onSceneRemove(self, guiObject):

        scnSort = makeSortString(SCN_ARCH,0,0)
        if scnSort in self.sceneTree.chapCount:
            scnNumber = self.sceneTree.chapCount[scnSort] + 1
        else:
            scnNumber = 1

        self.theBook.setSceneSection(SCN_ARCH)
        self.theBook.setSceneNumber(scnNumber)
        self.webEditor.saveText()
        self.theBook.saveScene()
        self.theBook.makeSceneIndex()
        self.sceneTree.loadContent(self.theBook)

        return

    def onSceneMoveUp(self, guiObject):
        return

    def onSceneMoveDown(self, guiObject):
        return

    def onSceneSelect(self, guiObject):

        logger.debug("GUI.onSceneSelect: Select scene")

        itemHandle = ""

        listModel, pathList = guiObject.get_selected_rows()
        for pathItem in pathList:
            listIter   = listModel.get_iter(pathItem)
            itemHandle = listModel.get_value(listIter,self.sceneTree.COL_HANDLE)

        if itemHandle == "" or itemHandle is None: return

        self.loadScene(itemHandle)

        return

    ##
    #  Main Window Events
    ##

    def onViewBookOverview(self, guiObject):
        self.bookOverview.showGUI()
        return

    def onViewSceneBuffer(self, guiObject):
        self.sceneBuffer.showGUI()
        return

    def onShowAbout(self, guiObject):

        dlgAbout = Gtk.AboutDialog()

        dlgAbout.set_transient_for(self.winMain)
        dlgAbout.set_program_name(self.mainConf.appName)
        dlgAbout.set_version(nw.__version__)
        dlgAbout.set_logo(getIconWidget("novelWriter",64).get_pixbuf())
        dlgAbout.set_website(self.mainConf.appURL)
        dlgAbout.set_comments("A simple editor for writing novels.")
        dlgAbout.set_authors(nw.__credits__)

        dlgAbout.run()
        dlgAbout.destroy()

        return

    def onMainTabChange(self, guiObject, guiChild, tabIdx):
        logger.debug("GUI.onMainTabChange: Main tab change")
        if tabIdx == nw.MAIN_DETAILS:
            return
        if tabIdx == nw.MAIN_EDITOR:
            return
        if tabIdx == nw.MAIN_SOURCE:
            self.loadSourceView()
        return

    def onGuiDestroy(self, guiObject):

        logger.info("Beginning shutdown procedure")

        # self.sceneBuffer.destroyGUI()

        # mainPane = self.getObject("panedContent").get_position()
        # sidePane = self.getObject("panedSide").get_position()
        # self.mainConf.setMainPane(mainPane)
        # self.mainConf.setSidePane(sidePane)
        # self.mainConf.saveConfig()
        # 
        # self.theBook.closeBook()

        logger.info("Exiting")
        Gtk.main_quit()

        return

    def onWinChange(self, guiObject, guiEvent):
        self.mainConf.setWinSize(guiEvent.width,guiEvent.height)
        return

    def onTick(self):
        self.guiTimer.onTick()
        self.sceneBuffer.onUpdate()
        return True

    def doAutoTasks(self):
        self.mainConf.onAutoSave()
        self.saveScene()
        self.webEditor.saveText()
        self.theBook.onAutoSave()
        self.updateWordCount()
        return True

# End Class GUI
