# -*- coding: utf-8 -*

##
#  novelWriter – Book Meta Class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Holds the metadata of the loaded book
##

import logging as logger
import configparser

from os import path

class BookMeta():

    def __init__(self, theOpt):

        # Inherited Data
        self.theOpt      = theOpt
        self.mainConf    = theOpt.mainConf

        # Saved Properties
        self.bookTitle   = ""
        self.bookAuthor  = ""
        self.bookDraft   = 1

        # Runtime Properties
        self.bookLoaded  = False
        self.bookChanged = False

        return

    ##
    #  Load and Save
    ##

    def loadData(self):

        bookFolder = self.theOpt.bookFolder
        if bookFolder is None:
            logger.debug("BookMeta.loadData: bookFolder = None")
            return

        bookPath = path.join(bookFolder,"bookData.nwf")
        if not path.isfile(bookPath):
            logger.debug("BookMeta.loadData: File not found %s" % bookPath)
            return

        confParser = configparser.ConfigParser()
        confParser.readfp(open(bookPath,"r"))

        # Get Variables
        cnfSec = "Book"
        if confParser.has_section(cnfSec):
            if confParser.has_option(cnfSec,"Title"):  self.bookTitle  = confParser.get(cnfSec,"Title")
            if confParser.has_option(cnfSec,"Author"): self.bookAuthor = confParser.get(cnfSec,"Author")
            if confParser.has_option(cnfSec,"Draft"):  self.bookDraft  = confParser.getint(cnfSec,"Draft")

        #self.makeIndex()

        self.mainConf.setLastBook(self.bookFolder)
        self.bookLoaded = True
        
        return

    def saveData(self):

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
        confParser.set(cnfSec,"Draft",  str(self.bookDraft))

        # Write File
        confParser.write(open(bookPath,"w"))
        self.mainConf.setLastBook(self.bookFolder)
        self.bookChanged = False

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

    ##
    #  Getters
    ##

    def getTitle(self):
        return self.bookTitle

    def getAuthor(self):
        return self.bookAuthor

# End Class BookMeta
