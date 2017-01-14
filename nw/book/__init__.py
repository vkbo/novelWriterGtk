# -*- coding: utf-8 -*

##
#  novelWriter – Data Wrapper Init File
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Data Wrapper initialisation
##

import logging as logger

from os                   import path, mkdir
from nw                   import *
from nw.book.bookopt      import BookOpt
from nw.book.bookmeta     import BookMeta
from nw.book.scenemeta    import SceneMeta
from nw.book.scenetext    import SceneText
from nw.book.scenesummary import SceneSummary
from nw.book.scenetiming  import SceneTiming

# Constants
IDX_TITLE   = 0
IDX_NUMBER  = 1
IDX_WORDS   = 2
IDX_SECTION = 3
IDX_CHAPTER = 4
IDX_NUMBER  = 5
IDX_COUNT   = 6

# ==================================================================================================================== #
# Begin Class Book

class Book():

    def __init__(self):

        # Core Objects
        self.mainConf = CONFIG
        self.theOpt   = BookOpt(self.mainConf)
        self.theMeta  = BookMeta(self.theOpt)
        self.theScene = Scene(self.theOpt)

        # Attributes
        self.bookLoaded = False

        # Connect to Setters
        self.setBookTitle  = self.theMeta.setTitle
        self.setBookAuthor = self.theMeta.setAuthor
        self.setBookDraft  = self.theMeta.setDraft

        # Connect to Getters
        self.getBookTitle  = self.theMeta.getTitle
        self.getBookAuthor = self.theMeta.getAuthor
        self.getBookDraft  = self.theMeta.getDraft
        
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
# ==================================================================================================================== #
# Begin Class Scene

class Scene():

    def __init__(self, theOpt):

        self.theOpt     = theOpt
        self.theMeta    = SceneMeta(theOpt)
        self.theText    = SceneText(theOpt)
        self.theSummary = SceneSummary(theOpt)
        self.theTiming  = SceneTiming(theOpt)

        return

    def clearContent(self):

        # Clear Objects

        return

    ##
    #  Methods
    ##

    def makeIndex(self):

        sceneIndex  = {}
        sceneFolder = self.theOpt.sceneFolder

        if sceneFolder is None:
            logger.debug("BookOpt.makeIndex: Path not found %s" % sceneFolder)
            return

        logger.debug("BookOpt.makeIndex: Scanning folder %s" % sceneFolder)
            
        dirContent = listdir(sceneFolder)

        # Scene Book Folder
        for listItem in dirContent:
            itemPath = path.join(sceneFolder,listItem)
            if path.isfile(itemPath):
                if len(listItem) == 25 and listItem[-12:] == "metadata.cnf":
                    itemHandle = listItem[:12]
                    tmpScene = SceneData()
                    tmpScene.setFolderPath(sceneFolder)
                    tmpScene.loadScene(itemHandle,True)
                    sceneIndex[itemHandle] = [
                        tmpScene.fileTitle,
                        tmpScene.fileNumber,
                        tmpScene.fileWords,
                        tmpScene.fileSection,
                        tmpScene.fileChapter,
                        tmpScene.fileNumber,
                        0
                    ]

        # Count File Versions
        for listItem in dirContent:
            itemPath = path.join(sceneFolder,listItem)
            if path.isfile(itemPath):
                if len(listItem) > 15 and listItem[-3:] == "txt":
                    itemHandle = listItem[:12]
                    sceneIndex[itemHandle][self.IDX_COUNT] += 1

        self.theOpt.setSceneIndex(sceneIndex)

        return

# End Class Scene
# ==================================================================================================================== #
