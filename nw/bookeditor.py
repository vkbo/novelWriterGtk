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

    def __init__(self, theBook):

        self.mainConf   = CONFIG
        self.guiBuilder = BUILDER
        self.theBook    = theBook
        self.getObject  = self.guiBuilder.get_object

        self.dlgWin     = self.getObject("dlgEditBook")
        self.dlgWin.set_transient_for(self.getObject("winMain"))

        return

    def clearEditor(self):

        logger.debug("BookEditor.clearEditor: Clearing book data")

        self.getObject("entryWorkingTitle").set_text("")
        self.getObject("entryAuthor").set_text("")
        self.getObject("filechooserPath").set_visible(True)
        self.getObject("filechooserPath").set_filename(self.mainConf.homePath)
        self.getObject("entryPath").set_visible(False)
        self.getObject("entryPath").set_text("")

        return

    def loadEditor(self):

        if not self.theBook.bookLoaded:
            return

        logger.debug("BookEditor.loadEditor: Loading book data")

        self.getObject("entryWorkingTitle").set_text(self.theBook.getBookTitle())
        self.getObject("entryAuthor").set_text(self.theBook.getBookAuthor())
        self.getObject("filechooserPath").set_visible(False)
        self.getObject("filechooserPath").set_filename(self.theBook.getBookFolder())
        self.getObject("entryPath").set_visible(True)
        self.getObject("entryPath").set_text(self.theBook.getBookFolder())

        return

    def saveEditor(self):

        logger.debug("BookEditor: Saving book data")

        bookTitle  = self.getObject("entryWorkingTitle").get_text()
        bookAuthor = self.getObject("entryAuthor").get_text()
        bookFolder = self.getObject("filechooserPath").get_filename()

        self.theBook.setBookTitle(bookTitle)
        self.theBook.setBookAuthor(bookAuthor)
        self.theBook.setBookFolder(bookFolder)

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
        self.saveEditor()
        return

# End Class EditBookDialog
