# -*- coding: utf-8 -*
#
#  pyÉcrire – Project Class
#
##

import logging as logger

import gi
gi.require_version('Gtk', '3.0')

from gi.repository             import Gtk
from os                        import path, mkdir, rename
from pyecrire.functions        import *
from pyecrire.data.datawrapper import DataWrapper

class Project():

    def __init__(self, config):

        self.mainConf = config

        # The Book
        self.theBook        = DataWrapper("Book")
        self.bookTitle      = "New Book"
        self.bookName       = simplifyString(self.bookTitle)
        self.bookHandle     = ""
        self.bookFolder     = ""
        self.bookPath       = ""

        # The Universe
        self.theUniverse    = DataWrapper("Universe")
        self.universeTitle  = "New Universe"
        self.universeName   = simplifyString(self.universeTitle)
        self.universeHandle = ""
        self.universeFolder = ""
        self.universePath   = ""

        # Set Other Defaults
        self.theBook.setTitle("New Book")
        self.theUniverse.setTitle("New Universe")

        return

    ##
    #  Updaters
    ##

    def updateBookFolder(self):

        bookFolder = "B-"+self.bookHandle+"-"+self.bookName

        if bookFolder != self.bookFolder:
            oldPath = path.join(self.mainConf.dataPath,self.bookFolder)
            newPath = path.join(self.mainConf.dataPath,bookFolder)

            if self.bookFolder == "":
                mkdir(newPath)
            else:
                if path.isdir(oldPath):
                    rename(oldPath,newPath)
                else:
                    mkdir(newPath)

            self.bookFolder = bookFolder
            self.bookPath   = newPath
            self.theBook.setDataPath(newPath)

        return


    def updateUniverseFolder(self):

        universeFolder = "U-"+self.universeHandle+"-"+self.universeName

        if universeFolder != self.universeFolder:
            oldPath = path.join(self.mainConf.dataPath,self.universeFolder)
            newPath = path.join(self.mainConf.dataPath,universeFolder)

            if self.universeFolder == "":
                mkdir(newPath)
            else:
                if path.isdir(oldPath):
                    rename(oldPath,newPath)
                else:
                    mkdir(newPath)

            self.universeFolder = universeFolder
            self.universePath   = newPath
            self.theUniverse.setDataPath(newPath)

        return

    ##
    #  Creators
    ##

    def createBook(self, bookTitle):
        bookName = simplifyString(bookTitle)

        if len(bookTitle) > 0 and len(bookName) > 0:
            self.bookTitle  = bookTitle
            self.bookName   = bookName
            if self.bookHandle == "":
                self.bookHandle = makeHandle(bookTitle)
            self.theBook.setTitle(bookTitle)

        logger.debug("Book Title:  %s" % self.bookTitle)
        logger.debug("Book Name:   %s" % self.bookName)
        logger.debug("Book Handle: %s" % self.bookHandle)

        return


    def createUniverse(self, universeTitle):
        universeName = simplifyString(universeTitle)

        if len(universeTitle) > 0 and len(universeName) > 0:
            self.universeTitle  = universeTitle
            self.universeName   = universeName
            if self.universeHandle == "":
                self.universeHandle = makeHandle(universeTitle)
            self.theUniverse.setTitle(universeTitle)
            self.theBook.setParent(self.universeHandle)

        logger.debug("Universe Title:  %s" % self.universeTitle)
        logger.debug("Universe Name:   %s" % self.universeName)
        logger.debug("Universe Handle: %s" % self.universeHandle)

        return


    ##
    #  Setters
    ##

    def setUniverse(self, universeHandle, universePath):

        self.theUniverse.setDataPath(universePath)
        self.theUniverse.loadDetails()

        self.universeTitle  = self.theUniverse.title
        self.universeName   = simplifyString(self.universeTitle)
        self.universeHandle = universeHandle
        self.universeFolder = "U-"+self.universeHandle+"-"+self.universeName
        self.universePath   = universePath

        self.theBook.parent = universeHandle

        return


    ##
    #  Other Actions
    ##

    def newProject(self, guiObject=None):

        self.bookTitle      = "New Book"
        self.bookName       = simplifyString(self.bookTitle)
        self.bookHandle     = ""
        self.bookFolder     = ""
        self.bookPath       = ""

        self.universeTitle  = "New Universe"
        self.universeName   = simplifyString(self.universeTitle)
        self.universeHandle = ""
        self.universeFolder = ""
        self.universePath   = ""

        return


    def newScene(self):
        return


    def loadProject(self, bookPath, bookHandle, universePath, universeHandle):
        logger.debug("Loading project")

        self.theBook.setDataPath(bookPath)
        self.theBook.loadDetails()

        self.bookTitle  = self.theBook.title
        self.bookName   = simplifyString(self.bookTitle)
        self.bookHandle = bookHandle
        self.bookFolder = "B-"+self.bookHandle+"-"+self.bookName
        self.bookPath   = bookPath

        self.theUniverse.setDataPath(universePath)
        self.theUniverse.loadDetails()

        self.universeTitle  = self.theUniverse.title
        self.universeName   = simplifyString(self.universeTitle)
        self.universeHandle = universeHandle
        self.universeFolder = "U-"+self.universeHandle+"-"+self.universeName
        self.universePath   = universePath

        return


    def saveProject(self):

        # Book
        self.updateBookFolder()
        self.theBook.saveDetails()

        # Universe
        self.updateUniverseFolder()
        self.theUniverse.saveDetails()

        return


# End Class Project
