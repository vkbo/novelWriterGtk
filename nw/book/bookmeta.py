# -*- coding: utf-8 -*

##
#  novelWriter – Book Meta Class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Holds the metadata of the loaded book
##

import logging as logger
import configparser

from os import path, mkdir
from nw import *

class BookMeta():

    def __init__(self, theOpt):

        # Core Objects
        self.mainConf    = CONFIG
        self.theOpt      = theOpt

        # Saved Attributes
        self.bookTitle   = ""
        self.bookAuthor  = ""
        self.recentScene = ""

        # Runtime Attributes
        self.bookLoaded  = False
        self.bookChanged = False

        return

    def clearContent(self):

        # Clear Saved Attributes
        self.bookTitle   = ""
        self.bookAuthor  = ""
        self.recentScene = ""

        # Clear Runtime Attributes
        self.bookLoaded  = False
        self.bookChanged = False

        return

    ##
    #  Load and Save
    ##

    def loadData(self):

        """
        Description:
            Loads the config variables for the currently loaded book speciefied in tyhe BookOpt object.
            Verifies that the draft folder for the scenes exists.
            Sets scene folder to the latest draft.
        """

        bookFolder = self.theOpt.bookFolder
        if bookFolder is None:
            logger.debug("BookMeta.loadData: bookFolder = None")
            return

        bookPath = path.join(bookFolder,"bookData.nwf")
        if not path.isfile(bookPath):
            logger.debug("BookMeta.loadData: File not found %s" % bookPath)
            return

        logger.debug("BookMeta.loadData: Loading book %s" % bookPath)
        confParser = configparser.ConfigParser()
        confParser.readfp(open(bookPath,"r"))

        # Get Variables
        cnfSec = "Book"
        if confParser.has_section(cnfSec):
            if confParser.has_option(cnfSec,"Title"):  self.bookTitle   = confParser.get(cnfSec,"Title")
            if confParser.has_option(cnfSec,"Author"): self.bookAuthor  = confParser.get(cnfSec,"Author")

        cnfSec = "Scene"
        if confParser.has_section(cnfSec):
            if confParser.has_option(cnfSec,"Recent"): self.recentScene = confParser.get(cnfSec,"Recent")

        self.bookLoaded = True
        
        self.verifyDraftFolder()
        sceneFolder = self.getDraftFolder()
        self.theOpt.setSceneFolder(sceneFolder)

        return

    def saveData(self):

        """
        Description:
            Simply saves the config data to the core book metadata file.
        """

        bookFolder = self.theOpt.bookFolder
        if bookFolder is None:
            logger.debug("BookMeta.saveData: bookFolder = None")
            return

        bookPath   = path.join(bookFolder,"bookData.nwf")
        confParser = configparser.ConfigParser()

        # Set Variables
        cnfSec = "Book"
        confParser.add_section(cnfSec)
        confParser.set(cnfSec,"Title",  str(self.bookTitle))
        confParser.set(cnfSec,"Author", str(self.bookAuthor))

        cnfSec = "Scene"
        confParser.add_section(cnfSec)
        confParser.set(cnfSec,"Recent", str(self.recentScene))

        # Write File
        confParser.write(open(bookPath,"w"))
        self.bookChanged = False

        self.verifyDraftFolder()

        return

    ##
    #  Setters
    ##

    def setTitle(self, newTitle):
        newTitle = newTitle.strip()
        if len(newTitle) > 0:
            self.bookTitle   = newTitle
            self.bookChanged = True
        else:
            logger.debug("BookMeta.setTitle: Invalid title '%s'" % newTitle)
        return

    def setAuthor(self, newAuthor):
        newAuthor = newAuthor.strip()
        self.bookAuthor  = newAuthor
        self.bookChanged = True
        return

    def setRecent(self, sceneHandle):
        self.recentScene = sceneHandle
        self.bookChanged = True
        return

    ##
    #  Getters
    ##

    def getTitle(self):
        return self.bookTitle

    def getAuthor(self):
        return self.bookAuthor

    def getRecent(self):
        return self.recentScene

    def getDraftFolder(self):
        return path.join(self.theOpt.bookFolder,"Draft %d" % self.theOpt.bookDraft)

    ##
    #  Methods
    ##

    def verifyDraftFolder(self):
        sceneFolder = self.getDraftFolder()
        if not path.isdir(sceneFolder):
            mkdir(sceneFolder)
            logger.debug("BookMeta.verifyDraftFolder: Created folder %s" % sceneFolder)
        return

# End Class BookMeta
