# -*- coding: utf-8 -*
#
#  pyÉcrire – Main GUI Class
#
##

import logging as logger

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit', '3.0')

from gi.repository      import Gtk, GLib, WebKit
from time               import sleep
from pyecrire.editor    import Editor
from pyecrire.timer     import Timer
from pyecrire.project   import *
from pyecrire.datastore import *
from pyecrire.datalist  import *

class GUI():

    def __init__(self, config):

        # Constants
        self.EDIT_FILE      = 0
        self.EDIT_BOOK      = 1
        self.EDIT_SCENE     = 2
        self.EDIT_UNIVERSE  = 3
        self.EDIT_CHARACTER = 4

        # Define Core Objects
        self.mainConf   = config
        self.projData   = Project(self.mainConf)

        # Initialise GUI
        self.guiBuilder = Gtk.Builder()
        self.guiBuilder.add_from_file("pyecrire/gui/winMain.glade")

        self.getObject  = self.guiBuilder.get_object
        self.winMain    = self.getObject("winMain")

        # Prepare GUI Classes
        self.webEditor  = Editor(self.winMain)
        self.guiTimer   = Timer(self.guiBuilder,self.mainConf)

        # Set Up Event Handlers
        guiHandlers = {
            "onDestroyWindow"          : self.guiDestroy,
            "onEventKeyPress"          : self.eventWinKeyPress,
            "onEventWinChange"         : self.eventWinChange,
            "onSwitchPageMainNoteBook" : self.eventTabChange,
            "onSwitchPageSideNoteBook" : self.eventTreeChange,
            "onClickNew"               : self.projData.newProject,
            "onClickSave"              : self.onFileSave,
            "onClickEditBold"          : self.webEditor.onEditAction,
            "onClickEditItalic"        : self.webEditor.onEditAction,
            "onClickEditUnderline"     : self.webEditor.onEditAction,
            "onClickEditStrikeThrough" : self.webEditor.onEditAction,
            "onClickEditColour"        : self.webEditor.onEditColour,
            "onClickTimerStart"        : self.guiTimer.onTimerStart,
            "onClickTimerPause"        : self.guiTimer.onTimerPause,
            "onClickTimerStop"         : self.guiTimer.onTimerStop,
            "onToggleNewUniverse"      : self.onToggleNewUniverse,
            "onMenuActionHelpAbout"    : self.onActionShowAbout,
            "onMenuActionFileSave"     : self.onFileSave,
            "onMenuActionFileQuit"     : self.guiDestroy,
        }
        self.guiBuilder.connect_signals(guiHandlers)

        # Prepare Panes
        self.guiPaned     = self.getObject("innerPaned")
        self.guiPaned.set_position(self.mainConf.winPane)

        # Prepare Details Pane and Default Document Type
        self.detailsPane  = self.getObject("detailsNoteBook")
        self.detailsPane.set_show_tabs(False)
        self.detailsPane.set_current_page(1)

        # Book Details
        self.allBooks        = DataList(self.mainConf.dataPath,"Book")
        self.allUniverses    = DataList(self.mainConf.dataPath,"Universe")
        self.bookUniverse    = self.getObject("cmbDetailsBookUniverse")
        self.bookUniverseNew = self.getObject("entryDetailsBookUniverse")
        self.listUniverse    = Gtk.ListStore(str)
        self.cellUniverse    = Gtk.CellRendererText()
        self.bookUniverse.set_model(self.listUniverse)
        self.bookUniverse.pack_start(self.cellUniverse, True)
        self.bookUniverse.add_attribute(self.cellUniverse, "text", 0)

        # Prepare Editor
        self.scrollEditor = self.getObject("scrollEditor")
        self.scrollEditor.add(self.webEditor)

        # Prepare Statusbar
        self.statusBar  = self.getObject("mainStatus")
        self.statusCID  = self.statusBar.get_context_id("Main")
        self.progStatus = self.getObject("progressStatus")

        # Set Up Timers
        self.timerID    = GLib.timeout_add(200, self.guiTimer.onTick)
        self.autoTaskID = GLib.timeout_add_seconds(30,self.autoTasks)

        # Prepare TreeView
        self.treeMain   = self.getObject("treeMain")
        self.treeData   = Gtk.TreeStore(str,int)
        self.treeData   = Gtk.TreeStore(str,int)
        self.treeMain.set_model(self.treeData)

        self.treeMainName  = self.treeMain.get_column(0)
        self.treeMainWords = self.treeMain.get_column(1)
        self.cellMainName  = Gtk.CellRendererText()
        self.cellMainWords = Gtk.CellRendererText()
        self.treeMainName.pack_start(self.cellMainName, True)
        self.treeMainWords.pack_start(self.cellMainWords, False)
        self.treeMainName.add_attribute(self.cellMainName, "text", 0)
        self.treeMainWords.add_attribute(self.cellMainWords, "text", 1)

        self.treeData.append(None,["New",0])

        # Default Values
        self.editType = self.EDIT_BOOK

        # Prepare Main Window
        self.winMain.set_title(self.mainConf.appName)
        self.winMain.resize(self.mainConf.winWidth,self.mainConf.winHeight)
        self.winMain.set_position(Gtk.WindowPosition.CENTER)
        self.winMain.show_all()

        return


    def loadProjects(self):


        return

    # Close Program
    def guiDestroy(self, guiObject):
        logger.debug("Exiting")
        self.mainConf.setWinPane(self.guiPaned.get_position())
        self.mainConf.autoSaveConfig()
        Gtk.main_quit()
        return


    # Automated Tasks
    def autoTasks(self):
        self.mainConf.autoSaveConfig()
        return True


    ##
    #  Actions
    ##

    def onFileSave(self, guiObject):
        logger.debug("Saving")
        if self.editType == self.EDIT_BOOK:
            self.projData.setBookTitle(self.getObject("entryDetailsBookTitle").get_text())
        self.projData.saveProject()
        return


    def onActionShowAbout(self, guiObject):

        dlgAbout = Gtk.AboutDialog()
        dlgAbout.set_transient_for(self.winMain)
        dlgAbout.set_program_name(self.mainConf.appName)
        dlgAbout.set_version(self.mainConf.appVersion)
        dlgAbout.set_website(self.mainConf.appURL)
        dlgAbout.run()
        dlgAbout.destroy()
        return


    ##
    #  Events
    ##

    def eventTabChange(self, guiObject, guiChild, tabIdx):
        logger.debug("Tab change")
        if tabIdx == 2:
            print("Source View")
            strSource = self.webEditor.getHtml()
            bufferSource = Gtk.TextBuffer()
            bufferSource.set_text(strSource)
            textSource = self.getObject("textSource")
            textSource.set_buffer(bufferSource)
            print(strSource)
        return

    def eventTreeChange(self, guiObject, guiChild, tabIdx):
        logger.debug("Tree tab change")
        if tabIdx == 0:
            self.editType = EDIT_BOOK
        if tabIdx == 1:
            self.editType = EDIT_FILE
        if tabIdx == 1:
            self.editType = EDIT_CHARACTER
        return

    def eventWinKeyPress(self, guiObject, guiEvent):
        self.guiTimer.resetAutoPause()
        return

    def eventWinChange(self, guiObject, guiEvent):
        self.mainConf.setWinSize(guiEvent.width,guiEvent.height)
        return

    def onToggleNewUniverse(self, guiObject):
        if guiObject.get_active():
            self.bookUniverseNew.set_can_focus(True)
        else:
            self.bookUniverseNew.set_can_focus(False)
        return


