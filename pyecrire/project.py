# -*- coding: utf-8 -*
#
#  pyÉcrire – Project Class
#
##

import logging as logger

import gi
gi.require_version('Gtk', '3.0')

from gi.repository      import Gtk
from os                 import path, mkdir, rename
from pyecrire.functions import *


class Project():

    def __init__(self, config):

        self.mainConf = config

        self.bookTitle      = "New Book"
        self.bookName       = simplifyString(self.bookTitle)
        self.bookHandle     = makeHandle(self.bookTitle)
        self.bookFolder     = ""
        self.bookPath       = ""
        self.universeTitle  = "New Universe"
        self.universeName   = simplifyString(self.universeTitle)
        self.universeHandle = makeHandle(self.universeTitle)
        self.universeFolder = ""
        self.universePath   = ""

        return


    def updateBookFolder(self):

        bookFolder = "B-"+self.bookHandle+"-"+self.bookName

        if bookFolder != self.bookFolder:
            pathOld = path.join(self.mainConf.dataPath,self.bookFolder)
            pathNew = path.join(self.mainConf.dataPath,bookFolder)

            if self.bookFolder == "":
                mkdir(pathNew)
            else:
                if path.isdir(pathOld):
                    rename(pathOld,pathNew)
                else:
                    mkdir(pathNew)

            self.bookFolder = bookFolder
            self.bookPath   = pathNew

        return


    def updateUniverseFolder(self):

        universeFolder = "U-"+self.universeHandle+"-"+self.universeName

        if universeFolder != self.universeFolder:
            pathOld = path.join(self.mainConf.dataPath,self.universeFolder)
            pathNew = path.join(self.mainConf.dataPath,universeFolder)

            if self.universeFolder == "":
                mkdir(pathNew)
            else:
                if path.isdir(pathOld):
                    rename(pathOld,pathNew)
                else:
                    mkdir(pathNew)

            self.universeFolder = universeFolder
            self.universePath   = pathNew

        return


    ##
    #  Setters
    ##

    def setBookTitle(self, bookTitle):
        bookName = simplifyString(bookTitle)

        if len(bookTitle) > 0 and len(bookName) > 0:
            self.bookTitle  = bookTitle
            self.bookName   = bookName
            self.bookHandle = makeHandle(bookTitle)

        logger.debug("Book Title:  %s" % self.bookTitle)
        logger.debug("Book Name:   %s" % self.bookName)
        logger.debug("Book Handle: %s" % self.bookHandle)

        return


    def setUniverseTitle(self, universeTitle):
        universeName = simplifyString(universeTitle)

        if len(universeTitle) > 0 and len(universeName) > 0:
            self.universeTitle  = universeTitle
            self.universeName   = universeName
            self.universeHandle = makeHandle(universeTitle)

        logger.debug("Universe Title:  %s" % self.universeTitle)
        logger.debug("Universe Name:   %s" % self.universeName)
        logger.debug("Universe Handle: %s" % self.universeHandle)

        return


    ##
    #  Actions
    ##

    def newProject(self, guiObject):

        self.bookTitle      = "New Book"
        self.bookName       = simplifyString(self.bookTitle)
        self.bookHandle     = makeHandle(self.bookTitle)
        self.bookFolder     = ""
        self.bookPath       = ""

        self.universeTitle  = "New Universe"
        self.universeName   = simplifyString(self.universeTitle)
        self.universeHandle = makeHandle(self.universeTitle)
        self.universeFolder = ""
        self.universePath   = ""

        return


    def saveProject(self):

        self.updateBookFolder()
        self.updateUniverseFolder()

        return

