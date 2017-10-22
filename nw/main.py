# -*- coding: utf-8 -*
"""novelWriter Main Class

 novelWriter – Main Class
==========================
 Sets up the main GUI and holds action and event functions

 File History:
 Created:   2017-01-10 [0.1.0]
 Rewritten: 2017-10-03 [0.4.0]

"""

import logging
import nw
import gi
gi.require_version("Gtk","3.0")

from gi.repository        import Gtk, Gdk
from time                 import sleep
from os                   import path
from nw.gui.winmain       import GuiWinMain
from nw.gui.tree_main     import GuiMainTree
from nw.gui.tree_chapters import GuiChaptersTree
from nw.gui.tree_chars    import GuiCharsTree
from nw.gui.tree_plots    import GuiPlotsTree
from nw.file.book         import Book, BookItem

logger = logging.getLogger(__name__)

class NovelWriter():
    
    def __init__(self):
        
        # Define Core Objects
        self.mainConf = nw.CONFIG
        self.theBook  = Book()
        
        # Build the GUI
        logger.debug("Assembling the main GUI")
        self.winMain   = GuiWinMain(self.theBook)
        self.bookPage  = self.winMain.bookPage
        self.charPage  = self.winMain.charPage
        self.plotPage  = self.winMain.plotPage
        # self.sceneEdit = self.winMain.sceneEdit
        
        # Set file filter for loading and saving
        self.fileFilter = Gtk.FileFilter()
        self.fileFilter.add_pattern("*")
        self.fileFilter.add_pattern("*.nwf")
        
        # Load StyleSheet
        cssPath = path.join(self.mainConf.themePath,self.mainConf.theTheme,"gtkstyles.css")
        logger.verbose("Loading stylesheet from %s" % cssPath)
        self.cssMain = Gtk.CssProvider()
        self.cssMain.load_from_path(cssPath)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),self.cssMain,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        
        #
        # Event Handlers
        #
        
        # Main Window
        self.winMain.connect("delete-event",self.onApplicationQuit)
        self.winMain.connect("configure-event",self.onMainWinChange)
        self.winMain.connect("key-press-event",self.onKeyPress)
        
        # Main ToolBar
        self.winMain.btnMainNew.connect("clicked",self.onBookNew)
        self.winMain.btnMainOpen.connect("clicked",self.onBookOpen)
        self.winMain.btnMainSave.connect("clicked",self.onBookSave)
        self.winMain.btnMainSaveAs.connect("clicked",self.onBookSave,True)
        
        # Main Tree
        self.winMain.treeLeft.treeSelect.connect("changed",self.onLeftTreeSelect)
        self.winMain.treeLeft.connect("row-activated",self.onLeftTreeActivate)
        self.winMain.btnLeftAdd.connect("clicked",self.onLeftAddFile)
        self.winMain.btnLeftMvU.connect("clicked",self.onLeftMoveFile,"UP")
        self.winMain.btnLeftMvD.connect("clicked",self.onLeftMoveFile,"DOWN")
        self.winMain.treeLeft.connect("button-release-event",self.onLeftTreeContextMenu)
        
        # Book Page
        self.bookPage.btnChaptersAdd.connect("clicked",self.onChapterAdd)
        self.bookPage.btnChaptersDel.connect("clicked",self.onChapterRemove)
        self.bookPage.btnChaptersMvU.connect("clicked",self.onChapterMove,"UP")
        self.bookPage.btnChaptersMvD.connect("clicked",self.onChapterMove,"DOWN")
        self.bookPage.treeChapters.rendType.connect("edited",self.onChapterEdit,"type")
        self.bookPage.treeChapters.rendNumber.connect("edited",self.onChapterEdit,"number")
        self.bookPage.treeChapters.rendTitle.connect("edited",self.onChapterEdit,"name")
        self.bookPage.treeChapters.rendCompile.connect("toggled",self.onChapterToggle,"compile")
        self.bookPage.treeChapters.rendComment.connect("edited",self.onChapterEdit,"comment")
        
        # Characters Page
        self.charPage.btnCharsAdd.connect("clicked",self.onCharAdd)
        self.charPage.btnCharsDel.connect("clicked",self.onCharRemove)
        self.charPage.btnCharsMvU.connect("clicked",self.onCharMove,"UP")
        self.charPage.btnCharsMvD.connect("clicked",self.onCharMove,"DOWN")
        self.charPage.treeChars.rendName.connect("edited",self.onCharEdit,"name")
        self.charPage.treeChars.rendImport.connect("edited",self.onCharEdit,"importance")
        self.charPage.treeChars.rendRole.connect("edited",self.onCharEdit,"role")
        self.charPage.treeChars.rendComment.connect("edited",self.onCharEdit,"comment")
        
        # Plots Page
        self.plotPage.btnPlotsAdd.connect("clicked",self.onPlotAdd)
        self.plotPage.btnPlotsDel.connect("clicked",self.onPlotRemove)
        self.plotPage.btnPlotsMvU.connect("clicked",self.onPlotMove,"UP")
        self.plotPage.btnPlotsMvD.connect("clicked",self.onPlotMove,"DOWN")
        self.plotPage.treePlots.rendName.connect("edited",self.onPlotEdit,"name")
        self.plotPage.treePlots.rendImport.connect("edited",self.onPlotEdit,"importance")
        self.plotPage.treePlots.rendComment.connect("edited",self.onPlotEdit,"comment")
        
        # Load Data from Last Project
        self.openBook(None,True)
        
        return
    
    #
    # Book Project Handling
    #
    
    def openBook(self, bookPath, openRecent=False):
        
        if openRecent:
            logger.info("BookOpen: Opening last book project from %s" % bookPath)
            bookPath = self.mainConf.getLastBook()
            if path.isfile(bookPath):
                self.theBook.openBook(bookPath)
            else:
                logger.info("BookOpen: Project file not found")
                self.theBook.createBook()
        else:
            if path.isfile(bookPath):
                logger.info("BookOpen: Opening book project from %s" % bookPath)
                self.theBook.openBook(bookPath)
            else:
                logger.info("BookOpen: Project file not found")
        
        self.winMain.treeLeft.loadContent()
        self.bookPage.treeChapters.loadContent()
        self.charPage.treeChars.loadContent()
        self.plotPage.treePlots.loadContent()
        
        bookTitle   = self.theBook.bookTitle
        bookAuthors = ", ".join(self.theBook.bookAuthors)
        winTitle    = "%s – novelWriter v%s" % (bookTitle,nw.__version__)
        
        self.winMain.set_title(winTitle)
        self.bookPage.entryBookTitle.set_text(bookTitle)
        self.bookPage.entryBookAuthor.set_text(bookAuthors)
        
        return
    
    def saveBook(self):
        
        self.theBook.setTitle(self.bookPage.entryBookTitle.get_text())
        self.theBook.setAuthors(self.bookPage.entryBookAuthor.get_text())
        
        for itemHandle in self.winMain.editPages.keys():
            self.winMain.editPages[itemHandle]["item"].saveContent()
        
        self.theBook.saveBook()
        self.mainConf.setLastBook(self.theBook.bookPath)
        
        self.winMain.treeLeft.loadContent()
        self.bookPage.treeChapters.loadContent()
        self.charPage.treeChars.loadContent()
        self.plotPage.treePlots.loadContent()
        
        return
    
    def closeBook(self):
        """Closes the currently open book project.
        ToDo: Make sure everything is saved
        ToDo: Close all open tabs
        """
        
        self.theBook.closeBook()
        
        return
    
    ##                  ##
    #   Event Handlers   #
    #  ================  #
    ##                  ##
    
    #
    # ToolBar Events
    #
    
    def onBookNew(self, guiObject):
        return
    
    def onBookOpen(self, guiObject):
        
        dlgOpen = Gtk.FileChooserNative()
        dlgOpen.set_title("Open book project ...")
        dlgOpen.set_transient_for(self.winMain)
        dlgOpen.set_modal(True)
        dlgOpen.set_action(Gtk.FileChooserAction.OPEN)
        dlgOpen.set_current_folder(self.mainConf.homePath)
        dlgReturn = dlgOpen.run()
        if dlgReturn == Gtk.ResponseType.ACCEPT:
            bookPath = dlgOpen.get_filename()
            logger.verbose("BookOpen: Reading %s" % bookPath)
            self.closeBook()
            self.openBook(bookPath)
        else:
            logger.verbose("BookOpen: Cancelled")
            return
        dlgOpen.destroy()
        
        return
    
    def onBookSave(self, guiObject, saveAs=False):
        
        if self.theBook.bookPath == None or saveAs:
            dlgSave = Gtk.FileChooserNative()
            dlgSave.set_title("Save book project as ...")
            dlgSave.set_transient_for(self.winMain)
            dlgSave.set_modal(True)
            dlgSave.set_action(Gtk.FileChooserAction.SAVE)
            dlgSave.set_current_folder(self.mainConf.homePath)
            dlgSave.set_current_name("NewBookProject.nwx")
            dlgReturn = dlgSave.run()
            if dlgReturn == Gtk.ResponseType.ACCEPT:
                savePath = dlgSave.get_filename()
                logger.verbose("BookSave: Saving to %s" % savePath)
                self.theBook.setBookPath(savePath)
            else:
                logger.verbose("BookSave: Cancelled")
                return
            dlgSave.destroy()
        
        self.saveBook()
        
        return
    
    #
    # Main Tree Events
    #
    
    def onLeftTreeSelect(self, guiObject):
        
        itemHandle = None
        
        listModel, pathList = guiObject.get_selected_rows()
        for pathItem in pathList:
            listIter   = listModel.get_iter(pathItem)
            itemHandle = listModel.get_value(listIter,GuiMainTree.COL_HANDLE)
            itemName   = listModel.get_value(listIter,GuiMainTree.COL_NAME)
            logger.vverbose("MainTree: Selected item %s named '%s'" % (itemHandle,itemName))
            
        if itemHandle == None: return
        
        itemEntry = self.theBook.getItem(itemHandle)
        
        itemClass = itemEntry["entry"].itemClass
        itemLevel = itemEntry["entry"].itemLevel
        itemType  = itemEntry["entry"].itemType
        
        logger.vverbose("MainTree: The item level is %s" % itemLevel)
        logger.vverbose("MainTree: The item type is %s" % itemType)
        
        if itemLevel == BookItem.LEV_ROOT:
            if itemType == BookItem.TYP_BOOK: self.winMain.showTab(self.winMain.TAB_BOOK)
            if itemType == BookItem.TYP_CHAR: self.winMain.showTab(self.winMain.TAB_CHAR)
            if itemType == BookItem.TYP_PLOT: self.winMain.showTab(self.winMain.TAB_PLOT)
            # if itemType == BookItem.TYP_NOTE: self.winMain.showTab(self.winMain.TAB_BOOK)
        # elif itemLevel == BookItem.LEV_FILE:
        #     docItem = itemEntry["doc"]
        #     if itemClass == BookItem.CLS_SCENE:
        #         self.winMain.showTab(self.winMain.TAB_EDIT)
        #         self.sceneEdit.loadContent(docItem)
        #     elif itemClass == BookItem.CLS_NOTE:
        #         self.winMain.showTab(self.winMain.TAB_EDIT)
        #         self.sceneEdit.loadContent(docItem)
        
        return
    
    def onLeftTreeActivate(self, guiObject, pathItem, itemColumn):
        
        listModel  = self.winMain.treeLeft.get_model()
        listIter   = listModel.get_iter(pathItem)
        itemHandle = listModel.get_value(listIter,GuiMainTree.COL_HANDLE)
        
        if itemHandle == None: return
        
        treeItem   = self.theBook.getItem(itemHandle)
        itemName   = treeItem["entry"].itemName
        itemLevel  = treeItem["entry"].itemLevel
        logger.vverbose("MainTree: Activated item %s named '%s'" % (itemHandle,itemName))
        
        if itemLevel == BookItem.LEV_FILE:
            self.winMain.editFile(itemHandle)
        
        return
    
    def onLeftMoveFile(self, guiObject, moveIt):
        
        itemHandle = None
        
        listModel, pathList = self.winMain.treeLeft.treeSelect.get_selected_rows()
        for pathItem in pathList:
            listIter   = listModel.get_iter(pathItem)
            itemHandle = listModel.get_value(listIter,GuiMainTree.COL_HANDLE)
        
        if itemHandle == None: return
        
        logger.debug("Moving file %s %s" % (itemHandle,moveIt))
        self.theBook.changeOrder(itemHandle,moveIt)
        
        self.winMain.treeLeft.loadContent()
        
        newIter = self.winMain.treeLeft.getIter(itemHandle)
        self.winMain.treeLeft.treeSelect.select_iter(newIter)
        
        return
    
    def onLeftAddFile(self, guiObject):
        
        itemHandle = None
        
        listModel, pathList = self.winMain.treeLeft.treeSelect.get_selected_rows()
        for pathItem in pathList:
            listIter   = listModel.get_iter(pathItem)
            itemHandle = listModel.get_value(listIter,GuiMainTree.COL_HANDLE)
            itemName   = listModel.get_value(listIter,GuiMainTree.COL_NAME)
            logger.vverbose("MainTree: Adding file to item %s named '%s'" % (itemHandle,itemName))
        
        if itemHandle == None: return
        
        self.theBook.addFile(itemHandle)
        self.winMain.treeLeft.loadContent()
        
        return
    
    def onLeftTreeContextMenu(self, guiObject, guiEvent):
        if guiEvent.button == 3:
            ctxMenu = self.winMain.treeLeft.menuContext
            ctxMenu.popup(None,None,None,None,guiEvent.button,guiEvent.time)
            ctxMenu.show_all()
        return
    
    #
    # Book Pane Events
    #
    
    def onChapterAdd(self, guiObject):
        
        logger.vverbose("User clicked add chapter")
        self.theBook.addChapter()
        self.winMain.treeLeft.loadContent()
        self.bookPage.treeChapters.loadContent()
        
        return
    
    def onChapterRemove(self, guiObject):
        
        logger.vverbose("User clicked remove chapter")
        
        return
    
    def onChapterMove(self, guiObject, moveIt):
        
        itemHandle = None
        
        listModel, pathList = self.winMain.bookPage.treeChapters.treeSelect.get_selected_rows()
        for pathItem in pathList:
            listIter   = listModel.get_iter(pathItem)
            itemHandle = listModel.get_value(listIter,GuiChaptersTree.COL_HANDLE)
        
        if itemHandle == None: return
        
        logger.debug("Moving chapter %s %s" % (itemHandle,moveIt))
        self.theBook.changeOrder(itemHandle,moveIt)
        
        self.winMain.treeLeft.loadContent()
        self.winMain.bookPage.treeChapters.loadContent()
        
        newIter = self.winMain.bookPage.treeChapters.getIter(itemHandle)
        self.winMain.bookPage.treeChapters.treeSelect.select_iter(newIter)
        
        return
    
    def onChapterEdit(self, guiObject, itemPath, editText, itemTag):
        
        srcTree   = self.bookPage.treeChapters
        handleCol = srcTree.COL_HANDLE
        
        if itemTag == "type":    srcColumn = srcTree.COL_TYPE
        if itemTag == "number":  srcColumn = srcTree.COL_NUMBER
        if itemTag == "name":    srcColumn = srcTree.COL_TITLE
        if itemTag == "comment": srcColumn = srcTree.COL_COMMENT
        
        itemHandle = srcTree.listStore[itemPath][handleCol]
        self.theBook.updateItem(itemHandle,itemTag,editText)
        parsedValue = self.theBook.getItem(itemHandle)["entry"].getFromTag(itemTag)
        srcTree.listStore[itemPath][srcColumn] = str(parsedValue)
        self.winMain.treeLeft.loadContent()
        
        return
    
    def onChapterToggle(self, guiObject, itemPath, itemTag):
        
        srcTree   = self.bookPage.treeChapters
        handleCol = srcTree.COL_HANDLE
        
        if itemTag == "compile": srcColumn = srcTree.COL_COMPILE
        
        itemHandle = srcTree.listStore[itemPath][handleCol]
        currState  = srcTree.listStore[itemPath][srcColumn]
        self.theBook.updateItem(itemHandle,itemTag,not currState)
        parsedValue = self.theBook.getItem(itemHandle)["entry"].getFromTag(itemTag)
        srcTree.listStore[itemPath][srcColumn] = parsedValue
        self.winMain.treeLeft.loadContent()
        
        return
    
    #
    # Characters Pane Events
    #
    
    def onCharAdd(self, guiObject):
        
        logger.vverbose("User clicked add character")
        self.theBook.addCharacter()
        self.winMain.treeLeft.loadContent()
        self.charPage.treeChars.loadContent()
        
        return
    
    def onCharRemove(self, guiObject):
        
        logger.vverbose("User clicked remove character")
        
        return
    
    def onCharMove(self, guiObject, moveIt):
        
        itemHandle = None
        
        listModel, pathList = self.winMain.charPage.treeChars.treeSelect.get_selected_rows()
        for pathItem in pathList:
            listIter   = listModel.get_iter(pathItem)
            itemHandle = listModel.get_value(listIter,GuiCharsTree.COL_HANDLE)
        
        if itemHandle == None: return
        
        logger.debug("Moving character %s %s" % (itemHandle,moveIt))
        self.theBook.changeOrder(itemHandle,moveIt)
        
        self.winMain.treeLeft.loadContent()
        self.winMain.charPage.treeChars.loadContent()
        
        newIter = self.winMain.charPage.treeChars.getIter(itemHandle)
        self.winMain.charPage.treeChars.treeSelect.select_iter(newIter)
        
        return
    
    def onCharEdit(self, guiObject, itemPath, editText, itemTag):
        
        srcTree   = self.charPage.treeChars
        handleCol = srcTree.COL_HANDLE
        
        if itemTag == "name":       srcColumn = srcTree.COL_TITLE
        if itemTag == "importance": srcColumn = srcTree.COL_IMPORTANCE
        if itemTag == "role":       srcColumn = srcTree.COL_ROLE
        if itemTag == "comment":    srcColumn = srcTree.COL_COMMENT
        
        itemHandle = srcTree.listStore[itemPath][handleCol]
        self.theBook.updateItem(itemHandle,itemTag,editText)
        parsedValue = self.theBook.getItem(itemHandle)["entry"].getFromTag(itemTag)
        srcTree.listStore[itemPath][srcColumn] = str(parsedValue)
        self.winMain.treeLeft.loadContent()
        
        return
    
    #
    # Plots Pane Events
    #
    
    def onPlotAdd(self, guiObject):
        
        logger.vverbose("User clicked add plot")
        self.theBook.addPlot()
        self.winMain.treeLeft.loadContent()
        self.plotPage.treePlots.loadContent()
        
        return
    
    def onPlotRemove(self, guiObject):
        
        logger.vverbose("User clicked remove plot")
        
        return
    
    def onPlotMove(self, guiObject, moveIt):
        
        itemHandle = None
        
        listModel, pathList = self.winMain.plotPage.treePlots.treeSelect.get_selected_rows()
        for pathItem in pathList:
            listIter   = listModel.get_iter(pathItem)
            itemHandle = listModel.get_value(listIter,GuiPlotsTree.COL_HANDLE)
        
        if itemHandle == None: return
        
        logger.debug("Moving plot %s %s" % (itemHandle,moveIt))
        self.theBook.changeOrder(itemHandle,moveIt)
        
        self.winMain.treeLeft.loadContent()
        self.winMain.plotPage.treePlots.loadContent()
        
        newIter = self.winMain.plotPage.treePlots.getIter(itemHandle)
        self.winMain.plotPage.treePlots.treeSelect.select_iter(newIter)
        
        return
    
    def onPlotEdit(self, guiObject, itemPath, editText, itemTag):
        
        srcTree   = self.plotPage.treePlots
        handleCol = srcTree.COL_HANDLE
        
        if itemTag == "name":       srcColumn = srcTree.COL_TITLE
        if itemTag == "importance": srcColumn = srcTree.COL_IMPORTANCE
        if itemTag == "comment":    srcColumn = srcTree.COL_COMMENT
        
        itemHandle = srcTree.listStore[itemPath][handleCol]
        self.theBook.updateItem(itemHandle,itemTag,editText)
        parsedValue = self.theBook.getItem(itemHandle)["entry"].getFromTag(itemTag)
        srcTree.listStore[itemPath][srcColumn] = str(parsedValue)
        self.winMain.treeLeft.loadContent()
        
        return
    
    #
    # Application Events
    #
    
    def onKeyPress(self, guiObject, guiKeyEvent):
        
        # print(guiKeyEvent.keyval)
        
        return
    
    def onMainWinChange(self, guiObject, guiEvent):
        self.mainConf.setWinSize(guiEvent.width,guiEvent.height)
        return

    def onApplicationQuit(self, guiObject, guiEvent):
        
        logger.info("Shutting down")
        
        # Get Pane Positions
        posOuter   = self.winMain.panedOuter.get_position()
        posContent = self.winMain.panedContent.get_position()
        # posEditor  = self.sceneEdit.get_position()
        # posMeta    = self.sceneEdit.panedMeta.get_position()
        # self.mainConf.setPanes([posOuter,posContent,posEditor,posMeta])
        self.mainConf.setPanes([posOuter,posContent])
        
        self.mainConf.saveConfig()
        logger.debug("Calling Gtk quit")
        Gtk.main_quit()
        
        return

# End Class NovelWriter
