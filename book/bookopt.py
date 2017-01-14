# -*- coding: utf-8 -*

##
#  novelWriter – Book Options Class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Holds the data options of the loaded book
##

import logging as logger

from os import path

class BookOpt():

    def __init__(self, parConfig):

        # Core Objects
        self.mainConf    = parConfig

        # Attributes
        self.bookFolder  = None
        self.sceneFolder = None
        self.sceneIndex  = {}
        
        return

    def clearContent(self):

        # Clear Attributes
        self.bookFolder  = None
        self.sceneFolder = None
        self.sceneIndex  = {}

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

# End Class BookOpt
