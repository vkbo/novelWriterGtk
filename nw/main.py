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

from gi.repository    import Gtk, Gdk
from time             import sleep
from os               import path
from nw.gui.winmain   import GuiWinMain
from nw.gui.tree_main import GuiMainTree
from nw.file          import Book, BookItem

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
        
        # Set Up Event Handlers
        self.winMain.connect("delete-event",self.onApplicationQuit)
        self.winMain.connect("configure-event",self.onMainWinChange)
        self.winMain.btnMainNew.connect("clicked",self.onBookNew)
        self.winMain.btnMainOpen.connect("clicked",self.onBookOpen)
        self.winMain.btnMainSave.connect("clicked",self.onBookSave)
        
        # Main Tree
        self.winMain.treeLeft.treeSelect.connect("changed",self.onLeftTreeSelect)
        self.winMain.treeLeft.connect("row-activated",self.onLeftTreeActivate)
        self.winMain.btnLeftAdd.connect("clicked",self.onLeftAddFile)
        
        # Book Page
        self.bookPage.btnChaptersAdd.connect("clicked",self.onChapterAdd)
        self.bookPage.btnChaptersDel.connect("clicked",self.onChapterRemove)
        self.bookPage.treeChapters.rendType.connect("edited",self.onChapterEdit,"type")
        self.bookPage.treeChapters.rendNumber.connect("edited",self.onChapterEdit,"number")
        self.bookPage.treeChapters.rendTitle.connect("edited",self.onChapterEdit,"name")
        self.bookPage.treeChapters.rendCompile.connect("edited",self.onChapterEdit,"compile")
        self.bookPage.treeChapters.rendComment.connect("edited",self.onChapterEdit,"comment")
        
        # Characters Page
        self.charPage.btnCharsAdd.connect("clicked",self.onCharAdd)
        self.charPage.btnCharsDel.connect("clicked",self.onCharRemove)
        self.charPage.treeChars.rendName.connect("edited",self.onCharEdit,"name")
        self.charPage.treeChars.rendImport.connect("edited",self.onCharEdit,"importance")
        self.charPage.treeChars.rendRole.connect("edited",self.onCharEdit,"role")
        self.charPage.treeChars.rendComment.connect("edited",self.onCharEdit,"comment")
        
        # Plots Page
        self.plotPage.btnPlotsAdd.connect("clicked",self.onPlotAdd)
        self.plotPage.btnPlotsDel.connect("clicked",self.onPlotRemove)
        self.plotPage.treePlots.rendName.connect("edited",self.onPlotEdit,"name")
        self.plotPage.treePlots.rendImport.connect("edited",self.onPlotEdit,"importance")
        self.plotPage.treePlots.rendComment.connect("edited",self.onPlotEdit,"comment")
        
        # Load Data
        lastBook = self.mainConf.getLastBook()
        if lastBook == "":
            logger.debug("No recent files set, creating empty book project")
            self.theBook.createBook()
        else:
            if path.isfile(lastBook):
                logger.info("Opening last book project from %s" % lastBook)
                self.openBook(lastBook)
            else:
                logger.debug("Last book project not found, creating empty book project")
                self.theBook.createBook()
        
        self.winMain.treeLeft.loadContent()
        self.bookPage.treeChapters.loadContent()
        self.charPage.treeChars.loadContent()
        self.plotPage.treePlots.loadContent()
        
        return
    
    def openBook(self, bookPath):
        
        self.theBook.openBook(bookPath)
        
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
        
        self.theBook.saveBook()
        self.mainConf.setLastBook(self.theBook.bookPath)
        
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
        return
    
    def onBookSave(self, guiObject):
        
        if self.theBook.bookPath == None:
            dlgSave = Gtk.FileChooserNative()
            dlgSave.set_title("Save book as ...")
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
            
        for itemHandle in self.winMain.editPages.keys():
            self.winMain.editPages[itemHandle]["item"].saveContent()
        
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
        
        itemEntry = self.theBook.getTreeEntry(itemHandle)
        
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
        itemName   = listModel.get_value(listIter,GuiMainTree.COL_NAME)
        logger.vverbose("MainTree: Activated item %s named '%s'" % (itemHandle,itemName))
            
        if itemHandle == None: return
        
        self.winMain.editFile(itemHandle)
        
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
    
    def onChapterEdit(self, guiObject, itemPath, editText, itemTag):
        
        srcTree   = self.bookPage.treeChapters
        handleCol = srcTree.COL_HANDLE
        
        if itemTag == "type":    srcColumn = srcTree.COL_TYPE
        if itemTag == "number":  srcColumn = srcTree.COL_NUMBER
        if itemTag == "name":    srcColumn = srcTree.COL_TITLE
        if itemTag == "compile": srcColumn = srcTree.COL_COMPILE
        if itemTag == "comment": srcColumn = srcTree.COL_COMMENT
        
        itemHandle = srcTree.listStore[itemPath][handleCol]
        self.theBook.updateTreeEntry(itemHandle,itemTag,editText)
        parsedValue = self.theBook.getTreeEntry(itemHandle)["entry"].getFromTag(itemTag)
        srcTree.listStore[itemPath][srcColumn] = str(parsedValue)
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
    
    def onCharEdit(self, guiObject, itemPath, editText, itemTag):
        
        srcTree   = self.charPage.treeChars
        handleCol = srcTree.COL_HANDLE
        
        if itemTag == "name":       srcColumn = srcTree.COL_TITLE
        if itemTag == "importance": srcColumn = srcTree.COL_IMPORTANCE
        if itemTag == "role":       srcColumn = srcTree.COL_ROLE
        if itemTag == "comment":    srcColumn = srcTree.COL_COMMENT
        
        itemHandle = srcTree.listStore[itemPath][handleCol]
        self.theBook.updateTreeEntry(itemHandle,itemTag,editText)
        parsedValue = self.theBook.getTreeEntry(itemHandle)["entry"].getFromTag(itemTag)
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
    
    def onPlotEdit(self, guiObject, itemPath, editText, itemTag):
        
        srcTree   = self.plotPage.treePlots
        handleCol = srcTree.COL_HANDLE
        
        if itemTag == "name":       srcColumn = srcTree.COL_TITLE
        if itemTag == "importance": srcColumn = srcTree.COL_IMPORTANCE
        if itemTag == "comment":    srcColumn = srcTree.COL_COMMENT
        
        itemHandle = srcTree.listStore[itemPath][handleCol]
        self.theBook.updateTreeEntry(itemHandle,itemTag,editText)
        parsedValue = self.theBook.getTreeEntry(itemHandle)["entry"].getFromTag(itemTag)
        srcTree.listStore[itemPath][srcColumn] = str(parsedValue)
        self.winMain.treeLeft.loadContent()
        
        return
    
    #
    # Application Events
    #
    
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
