# -*- coding: utf-8 -*

##
#  novelWriter – Book Options Class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Holds the data options of the loaded book
##

import logging as logger

from os import path
from nw import *

class BookOpt():

    def __init__(self):

        # Core Objects
        self.mainConf     = CONFIG

        # Attributes
        self.bookFolder   = None
        self.sceneFolder  = None
        self.sceneIndex   = {}
        self.sceneHandle  = ""
        self.sceneVersion = 1
        
        return

    def clearContent(self):

        # Clear Attributes
        self.bookFolder   = None
        self.sceneFolder  = None
        self.sceneIndex   = {}
        self.sceneHandle  = ""
        self.sceneVersion = 1

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

    def setSceneFolder(self, sceneFolder):
        if path.isdir(sceneFolder):
            self.sceneFolder = sceneFolder
        else:
            logger.debug("BookOpt.setSceneFolder: Folder not found %s" % sceneFolder)
        return

    def setSceneIndex(self, sceneIndex):
        self.sceneIndex = sceneIndex
        return

    def setSceneHandle(self, sceneHandle):
        if len(sceneHandl) == 12:
            self.sceneHandle = sceneHandle
        else:
            logger.debug("BookOpt.setSceneHandle: Invalid scene handle '%s'" % sceneHandle)
        return

    def setSceneVersion(self, sceneVersion):
        if sceneVersion > 0:
            self.sceneVersion = sceneVersion
        else:
            logger.debug("BookOpt.setSceneVersion: Invalid scene version")
        return

    ##
    #  Getters
    ##

    def getBookFolder(self):
        return self.bookFolder

    def getSceneFolder(self):
        return self.sceneFolder

    def getSceneIndex(self):
        return self.sceneIndex

    def getSceneHandle(self):
        return self.sceneHandle

    def getSceneVersion(self):
        return self.sceneVersion

# End Class BookOpt
