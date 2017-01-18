# -*- coding: utf-8 -*

##
#  novelWriter – Data Wrapper Init File
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Data Wrapper initialisation
##

import logging as logger

from os                   import path, mkdir, listdir
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

        """
        Description:
            Creates meta object and scene object.
            Links sub class functions.
        """
        
        # Core Objects
        self.mainConf = CONFIG
        self.theOpt   = BookOpt()
        self.theMeta  = BookMeta(self.theOpt)
        self.theScene = Scene(self.theOpt,self.theMeta)

        # Runtime Attributes
        self.bookLoaded = False

        # Connect to Scene Functions
        self.createScene     = self.theScene.createScene
        self.loadScene       = self.theScene.loadScene
        self.closeScene      = self.theScene.closeScene
        self.saveScene       = self.theScene.saveScene
        self.saveTiming      = self.theScene.theTiming.saveTiming

        # Connect to Setters
        self.setBookTitle    = self.theMeta.setTitle
        self.setBookAuthor   = self.theMeta.setAuthor
        self.setBookRecent   = self.theMeta.setRecent
        self.setBookFolder   = self.theOpt.setBookFolder
        self.setBookDraft    = self.theOpt.setBookDraft
        self.setSceneTitle   = self.theScene.theMeta.setTitle
        self.setSceneSection = self.theScene.theMeta.setSection
        self.setSceneChapter = self.theScene.theMeta.setChapter
        self.setSceneNumber  = self.theScene.theMeta.setNumber
        self.setSceneText    = self.theScene.theText.setText
        self.setSceneSummary = self.theScene.theSummary.setSummary
        self.setSceneTime    = self.theScene.theTiming.setTime

        # Connect to Getters
        self.getBookTitle    = self.theMeta.getTitle
        self.getBookAuthor   = self.theMeta.getAuthor
        self.getBookRecent   = self.theMeta.getRecent
        self.getBookFolder   = self.theOpt.getBookFolder
        self.getBookDraft    = self.theOpt.getBookDraft
        self.getSceneIndex   = self.theOpt.getSceneIndex
        self.getSceneHandle  = self.theOpt.getSceneHandle
        self.getSceneVersion = self.theOpt.getSceneVersion
        self.getSceneTitle   = self.theScene.theMeta.getTitle
        self.getSceneSection = self.theScene.theMeta.getSection
        self.getSceneCreated = self.theScene.theMeta.getCreated
        self.getSceneUpdated = self.theScene.theMeta.getUpdated
        self.getSceneChapter = self.theScene.theMeta.getChapter
        self.getSceneNumber  = self.theScene.theMeta.getNumber
        self.getSceneWords   = self.theScene.theMeta.getWords
        self.getSceneChars   = self.theScene.theMeta.getChars
        self.getSceneChanged = self.theScene.theMeta.getSceneChanged
        self.getSceneText    = self.theScene.theText.getText
        self.getSceneWords   = self.theScene.theText.getWordCount
        self.getSceneChars   = self.theScene.theText.getCharCount
        self.getSceneSummary = self.theScene.theSummary.getSummary
        self.getSceneTime    = self.theScene.theTiming.getTimeTotal

        # Connect to Methods
        self.makeSceneIndex  = self.theScene.makeIndex
        self.countWords      = self.theScene.theText.countWords
        self.htmlCleanUp     = self.theScene.theText.htmlCleanUp
        
        return

    ##
    #  Create, Load and Save
    ##

    def clearContent(self):

        """
        Description:
            Clears book options
            Clears book metadata
            Clears scene content
        """
        
        logger.debug("Book.clearContent: Clearing content")

        # Clear Objects
        self.theOpt.clearContent()
        self.theMeta.clearContent()
        self.theScene.clearContent()

        self.bookLoaded = False

        return

    def createBook(self, rootFolder):

        """
        Description:
            Requires book title to be set.
            Close current book, if any
            Creates a folder based on the book title.
            Sets the draft number to 1, which will ensure the folder is created when metadata is reloaded.
            Saves the book, and reloads it causing the metadata file to be written and indices to be updated.
        """
        
        bookTitle = self.getBookTitle()
        if bookTitle == "":
            logger.debug("Book.createBook: Set title before creating new book")
            return

        self.closeBook()

        bookFolder = path.join(rootFolder,bookTitle)
        if not path.isdir(bookFolder):
            mkdir(bookFolder)
            logger.debug("Book.createBook: Created folder %s" % bookFolder)

        self.theOpt.setBookFolder(bookFolder)
        self.theOpt.setBookDraft(1)
        self.saveBook()

        return

    def loadBook(self, bookFolder):

        """
        Description:
            Closes the current book
            Sets the current book folder and checks that it's valid.
            Generates book index which looks for draft folders and sets the draft to load to the latest.
            Generates scene index from the latest draft folder.
            If a recent scene is listed, load it
            Sets last loaded book in config
        """

        logger.debug("Book.loadBook: Loading book from %s" % bookFolder)

        # Close Current Book
        self.closeBook()

        # Load Book
        self.theOpt.setBookFolder(bookFolder)
        if self.theOpt.bookFolder is None: return

        # Load Book Data
        self.makeIndex()
        self.theMeta.loadData()
        self.theScene.makeIndex()

        self.mainConf.setLastBook(bookFolder)
        self.bookLoaded = self.theMeta.bookLoaded
        
        return

    def closeBook(self):

        """
        Description:
            Check if a book is loaded
            Save current book and scene (close scene)
            Clear content
        """

        if not self.bookLoaded:
            logger.debug("Book.closeBook: No book loaded")
            return
            
        logger.debug("Book.closeBook: Closing book")

        self.saveBook()
        self.theScene.closeScene()
        self.clearContent()
        
        return

    def saveBook(self):

        """
        Description:
            Saves meta data. Scene data must be saved separately.
        """

        logger.debug("Book.saveBook: Saving book")
        self.theMeta.saveData()

        return

    ##
    #  Methods
    ##

    def makeIndex(self):

        bookIndex  = {}
        bookFolder = self.theOpt.bookFolder

        if bookFolder is None:
            logger.debug("Book.makeIndex: Path not found %s" % bookFolder)
            return

        logger.debug("Book.makeIndex: Scanning folder %s" % bookFolder)
            
        dirContent = listdir(bookFolder)
        for listItem in dirContent:
            itemPath = path.join(bookFolder,listItem)
            if path.isdir(itemPath):
                if listItem[:5] == "Draft":
                    bookDraft = int(listItem[6:])
                    bookIndex[bookDraft] = [listItem,0]

        self.theOpt.setBookIndex(bookIndex)
        self.theOpt.setBookDraft(len(bookIndex))

        return

# End Class Book
