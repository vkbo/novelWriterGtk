# -*- coding: utf-8 -*

##
#  novelWriter – Data Wrapper
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Wrapper classes for data files
##

import logging as logger
import configparser

import gi
gi.require_version("Gtk","3.0")

from gi.repository import Gtk
from os            import path, mkdir
from nw            import *

class BookData():

    def __init__(self):

        self.mainConf   = CONFIG

        self.bookTitle  = ""
        self.bookAuthor = ""
        self.bookFolder = ""
        self.bookDraft  = 1

        self.bookLoaded = False

        return

    def loadBook(self, loadPath):

        if loadPath == "": return

        self.bookFolder = loadPath

        confParser = configparser.ConfigParser()
        confParser.readfp(open(path.join(self.bookFolder,"metadata.cnf")))

        # Get Variables
        cnfSec = "Book"
        if confParser.has_section(cnfSec):
            if confParser.has_option(cnfSec,"Title"):  self.bookTitle  = confParser.get(cnfSec,"Title")
            if confParser.has_option(cnfSec,"Author"): self.bookAuthor = confParser.get(cnfSec,"Author")
            if confParser.has_option(cnfSec,"Draft"):  self.bookDraft  = confParser.get(cnfSec,"Draft")

        self.mainConf.setLastBook(self.bookFolder)

        self.bookLoaded = True

        return

    def saveBook(self):

        logger.debug("Saving Book Data")
        confParser = configparser.ConfigParser()

        # Set Variables
        cnfSec = "Book"
        confParser.add_section(cnfSec)
        confParser.set(cnfSec,"Title",  str(self.bookTitle))
        confParser.set(cnfSec,"Author", str(self.bookAuthor))
        confParser.set(cnfSec,"Draft",  str(self.bookDraft))

        # Write File
        confParser.write(open(path.join(self.bookFolder,"metadata.cnf"),"w"))
        self.mainConf.setLastBook(self.bookFolder)

        return

    ##
    #  Setters
    ##

    def setTitle(self, title):
        self.bookTitle = title.strip()
        return

    def setAuthor(self, author):
        self.bookAuthor = author.strip()
        return

    def setBookFolder(self, folder):
        if path.isdir(folder) and self.bookTitle != "":
            self.bookFolder = path.join(folder,self.bookTitle)
            if not path.isdir(self.bookFolder):
                mkdir(self.bookFolder)
        return

# End Class BookData

class SceneData():

    def __init__(self):
        return

# End Class SceneData
