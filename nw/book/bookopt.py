# -*- coding: utf-8 -*

##
#  novelWriter – Book Options Class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Holds the data options of the loaded book
##

import logging as logger

from os import path, mkdir
from nw import *

class BookOpt():

    """
    Description:
        A container shared between all book methods.
        It holds the indices of drafts and scenes, as well as which one is currently loaded
    """

    def __init__(self):

        # Core Objects
        self.mainConf     = CONFIG

        # Attributes
        self.bookFolder   = None
        self.bookIndex    = {}
        self.bookDraft    = 0
        self.sceneFolder  = None
        self.sceneIndex   = {}

        return

    ##
    #  Setters
    ##

    def setBookFolder(self, bookFolder):
        if path.isdir(bookFolder):
            self.bookFolder = bookFolder
        else:
            logger.debug("BookOpt.setBookFolder: Folder not found %s" % bookFolder)
        return

    def setBookIndex(self, bookIndex):
        self.bookIndex = bookIndex
        return

    def setBookDraft(self, bookDraft):
        self.bookDraft = bookDraft
        return

    def setSceneFolder(self, sceneFolder):
        if path.isdir(sceneFolder):
            self.sceneFolder = sceneFolder
        else:
            logger.debug("BookOpt.setSceneFolder: Folder not found %s" % sceneFolder)
        return

    def setSceneIndex(self, sceneIndex):
        self.sceneIndex = sceneIndex
        return

    ##
    #  Getters
    ##

    def getLastDraft(self):
        return max(self.bookIndex.keys())

    def getBookFolder(self):
        return self.bookFolder

    def getBookDraft(self):
        return self.bookDraft

    def getSceneFolder(self):
        return self.sceneFolder

    def getSceneIndex(self):
        return self.sceneIndex

    def setSceneIndexEntry(self, sceneHandle, sceneValues):
        self.sceneIndex[sceneHandle] = sceneValues
        return

    ##
    #  Other Methods
    ##

    def isValidHandle(self, sceneHandle):
        if sceneHandle in self.sceneIndex.keys(): return True
        return False

    def removeSceneIndexEntry(self, sceneHandle):
        return self.sceneIndex.pop(sceneHandle,False)

# End Class BookOpt
