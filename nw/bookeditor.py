# -*- coding: utf-8 -*

##
#  novelWriter – Book Editor
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Book Editor GUI
##

import logging as logger

import gi
gi.require_version("Gtk","3.0")

from os            import path
from gi.repository import Gtk
from nw            import *

class BookEditor():

    def __init__(self):

        self.mainConf   = CONFIG
        self.guiBuilder = BUILDER
        self.theBook    = None
        self.getObject  = self.guiBuilder.get_object

        self.dlgWin     = self.getObject("dlgEditBook")
        self.dlgWin.set_transient_for(self.getObject("winMain"))

        return

    def loadEditor(self, theBook):

        if not theBook.bookLoaded:
            return

        logger.debug("Book Editor: Load")

        self.theBook = theBook
        self.theBook.loadBook(self.theBook.bookFolder)

        self.getObject("entryWorkingTitle").set_text(self.theBook.bookTitle)
        self.getObject("entryAuthor").set_text(self.theBook.bookAuthor)
        self.getObject("filechooserPath").set_filename(self.theBook.bookFolder)

        self.mainConf.setLastBook(self.theBook.bookFolder)

        return

    def saveEditor(self):

        logger.debug("Book Editor: Save")

        bookTitle  = self.getObject("entryWorkingTitle").get_text()
        bookAuthor = self.getObject("entryAuthor").get_text()
        bookFolder = self.getObject("filechooserPath").get_filename()

        self.theBook.setTitle(bookTitle)
        self.theBook.setAuthor(bookAuthor)
        if self.theBook.bookFolder == "":
            self.theBook.setBookFolder(bookFolder)

        appName   = self.mainConf.appName
        bookTitle = self.theBook.bookTitle
        bookDraft = self.theBook.bookDraft

        winTitle = "%s: %s (Draft %d)" % (appName,bookTitle,bookDraft)
        self.getObject("winMain").set_title(winTitle)

        self.theBook.saveBook()
        self.dlgWin.hide()

        return

    def cancelEditor(self):
        self.dlgWin.hide()
        return

    ##
    #  Button Events
    ##

    def onBookCancel(self, guiObject):
        self.cancelEditor()
        return

    def onBookSave(self, guiObject):
        logger.debug("Book Save")
        self.saveEditor()
        return

# End Class EditBookDialog
