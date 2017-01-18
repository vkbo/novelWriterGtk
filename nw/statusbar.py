# -*- coding: utf-8 -*

##
#  novelWriter – StatusBar Class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Main wrapper class for the GUI status bar
##

import logging as logger

import gi
gi.require_version("Gtk","3.0")

from gi.repository import Gtk
from nw            import *

class StatusBar():

    def __init__(self):

        # Connect to Global Objects
        self.mainConf     = CONFIG
        self.getObject    = BUILDER.get_object

        # Connect to GUI Elements
        self.statusImage  = self.getObject("imgStatusFile")
        self.statusText   = self.getObject("lblStatusFile")
        self.statusHandle = self.getObject("lblStatusHandle")
        self.statusLang   = self.getObject("lblStatusLang")
        self.statusProg   = self.getObject("progressStatus")

        return

    def setLED(self, ledColour):
        self.statusImage.set_from_pixbuf(getIconWidget(ledColour,16).get_pixbuf())
        return

    def setActiveFile(self, theBook):

        sepText   = " ► "

        bookTitle = theBook.getBookTitle()
        fileLabel = "Editing: "+bookTitle

        bookDraft = theBook.getBookDraft()
        if bookDraft > 0:
            fileLabel += sepText+("Draft %d" % bookDraft)

        # sceneHandle = theBook.getSceneHandle()
        # sceneTitle  = theBook.getSceneTitle()
        # if len(sceneHandle) == 12:
        #     fileLabel += sepText+(sceneTitle)
        #
        # sceneVersion = theBook.getSceneVersion()
        # if sceneVersion > 0:
        #     fileLabel += sepText+("Version %d" % sceneVersion)

        self.statusText.set_label(fileLabel)
        # self.statusHandle.set_label("[%s]" % sceneHandle)

        return

    def setLanguage(self, langText):
        self.statusLang.set_label("[%s]" % langText)
        return

# End Class StatusBar
