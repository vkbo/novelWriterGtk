# -*- coding: utf-8 -*

##
#  novelWriter – Data Wrapper Init File
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Data Wrapper initialisation
##

import logging as logger

from os                   import path, mkdir
from nw                   import *
from nw.book.scene        import Scene
from nw.book.bookopt      import BookOpt
from nw.book.bookmeta     import BookMeta
from nw.book.scenemeta    import SceneMeta
from nw.book.scenetext    import SceneText
from nw.book.scenesummary import SceneSummary
from nw.book.scenetiming  import SceneTiming

class Book():

    def __init__(self):

        # Core Objects
        self.mainConf = CONFIG
        self.theOpt   = BookOpt()
        self.theMeta  = BookMeta(self.theOpt)
        self.theScene = Scene(self.theOpt)

        # Attributes
        self.bookLoaded = False

        # Connect to Setters
        self.setBookTitle    = self.theMeta.setTitle
        self.setBookAuthor   = self.theMeta.setAuthor
        self.setBookDraft    = self.theMeta.setDraft
        self.setSceneText    = self.theScene.theText.setText
        self.setSceneSummary = self.theScene.theSummary.setSummary

        # Connect to Getters
        self.getBookTitle    = self.theMeta.getTitle
        self.getBookAuthor   = self.theMeta.getAuthor
        self.getBookDraft    = self.theMeta.getDraft
        self.getSceneIndex   = self.theOpt.getSceneIndex
        self.getSceneHandle  = self.theOpt.getSceneHandle
        self.getSceneText    = self.theScene.theText.getText
        self.getSceneSummary = self.theScene.theSummary.getSummary

        # Connect to Methods
        self.makeSceneIndex = self.theScene.makeIndex
        self.countWords     = self.theScene.theText.countWords
        self.htmlCleanUp    = self.theScene.theText.htmlCleanUp
        
        return

    ##
    #  Create, Load and Save
    ##

    def createBook(self, rootFolder):

        bookTitle = self.getBookTitle()
        if bookTitle == "":
            logger.debug("Book.createBook: Set title before creating new book")
            return

        bookFolder = path.join(rootFolder,bookTitle)
        if not path.isdir(bookFolder):
            mkdir(bookFolder)
            logger.debug("Book.createBook: Created folder %s" % bookFolder)

        return

    def loadBook(self, bookFolder):

        # Clear Attributes
        self.bookLoaded = False

        # Clear Objects
        self.theOpt.clearContent()
        self.theMeta.clearContent()
        self.theScene.clearContent()

        # Load Book
        self.theOpt.setBookFolder(bookFolder)
        if self.theOpt.bookFolder is None: return

        self.theMeta.loadData()
        self.bookLoaded = self.theMeta.bookLoaded
        
        return

    def saveBook(self):
        return

# End Class Book
