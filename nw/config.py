# -*- coding: utf-8 -*
"""novelWriter Config Class

 novelWriter – Config Class
============================
 This class reads and store the main preferences of the application

 File History:
 Created: 2017-01-10 [0.1.0]

"""

import logging
import configparser
import nw
import gi
gi.require_version("Gtk","3.0")

from gi.repository import Gtk
from os            import path, mkdir, getcwd
from appdirs       import user_config_dir

logger = logging.getLogger(__name__)

class Config:

    def __init__(self):

        # Set Application Variables
        self.appName    = "novelWriter"
        self.appHandle  = "novelwriter"
        self.appURL     = "https://github.com/vkbo/novelWriter"

        # Set Paths
        self.confPath   = user_config_dir(self.appHandle)
        self.confFile   = self.appHandle+".conf"
        self.homePath   = path.expanduser("~")
        self.appPath    = path.dirname(__file__)
        self.guiPath    = path.join(self.appPath,"gui")
        self.themePath  = path.join(self.appPath,"themes")

        # If config folder does not exist, make it.
        # This assumes that the os config folder itself exists.
        if not path.isdir(self.confPath):
            mkdir(self.confPath)

        # Set default values
        self.confChanged = False

        ## General
        self.winWidth    = 1600
        self.winHeight   = 980
        self.mainPane    = 280
        self.contPane    = 750
        self.editPane    = 900
        self.metaPane    = 240
        self.theTheme    = "default"

        ## Editor
        self.autoSave    = 30   # Seconds
        self.fontSize    = 16   # Pixels
        self.lineHeight  = 150  # Percent
        self.lineIndent  = 400  # Percent
        self.parMargin   = 4    # Pixels
        self.pageMargin  = 40   # Pixels
        self.spellCheck  = "en_GB"
        self.spellState  = False
        self.showPara    = False

        ## Timer
        self.autoPause   = 60   # Seconds
        self.minTime     = 10   # Seconds

        ## Paths
        self.recentBook  = ["","","","","","","","","",""]

        # Check if config file exists
        if path.isfile(path.join(self.confPath,self.confFile)):
            self.loadConfig()

        # Save a copy of the default config if no file exists
        if not path.isfile(path.join(self.confPath,self.confFile)):
            self.saveConfig()

        return

    ##
    #  Actions
    ##

    def loadConfig(self):

        logger.debug("Loading config file")
        confParser = configparser.ConfigParser()
        confParser.readfp(open(path.join(self.confPath,self.confFile)))

        # Get options

        ## Main
        cnfSec = "Main"
        if confParser.has_section(cnfSec):
            if confParser.has_option(cnfSec,"winWidth"):   self.winWidth     = confParser.getint(cnfSec,"winWidth")
            if confParser.has_option(cnfSec,"winHeight"):  self.winHeight    = confParser.getint(cnfSec,"winHeight")
            if confParser.has_option(cnfSec,"mainPane"):   self.mainPane     = confParser.getint(cnfSec,"mainPane")
            if confParser.has_option(cnfSec,"contPane"):   self.contPane     = confParser.getint(cnfSec,"contPane")
            if confParser.has_option(cnfSec,"editPane"):   self.editPane     = confParser.getint(cnfSec,"editPane")
            if confParser.has_option(cnfSec,"metaPane"):   self.metaPane     = confParser.getint(cnfSec,"metaPane")

        ## Editor
        cnfSec = "Editor"
        if confParser.has_section(cnfSec):
            if confParser.has_option(cnfSec,"autoSave"):   self.autoSave     = confParser.getint(cnfSec,"autoSave")
            if confParser.has_option(cnfSec,"fontSize"):   self.fontSize     = confParser.getint(cnfSec,"fontSize")
            if confParser.has_option(cnfSec,"lineHeight"): self.lineHeight   = confParser.getint(cnfSec,"lineHeight")
            if confParser.has_option(cnfSec,"lineIndent"): self.lineIndent   = confParser.getint(cnfSec,"lineIndent")
            if confParser.has_option(cnfSec,"parMargin"):  self.parMargin    = confParser.getint(cnfSec,"parMargin")
            if confParser.has_option(cnfSec,"pageMargin"): self.pageMargin   = confParser.getint(cnfSec,"pageMargin")
            if confParser.has_option(cnfSec,"spellCheck"): self.spellCheck   = confParser.get(cnfSec,"spellCheck")
            if confParser.has_option(cnfSec,"spellState"): self.spellState   = confParser.getboolean(cnfSec,"spellState")
            if confParser.has_option(cnfSec,"showPara"):   self.showPara     = confParser.getboolean(cnfSec,"showPara")

        ## Timer
        cnfSec = "Timer"
        if confParser.has_section(cnfSec):
            if confParser.has_option(cnfSec,"autoPause"):  self.autoPause    = confParser.getint(cnfSec,"autoPause")
            if confParser.has_option(cnfSec,"minTime"):    self.minTime      = confParser.getint(cnfSec,"minTime")

        ## Path
        cnfSec = "Path"
        if confParser.has_section(cnfSec):
            if confParser.has_option(cnfSec,"Recent0"):   self.recentBook[0] = confParser.get(cnfSec,"Recent0")
            if confParser.has_option(cnfSec,"Recent1"):   self.recentBook[1] = confParser.get(cnfSec,"Recent1")
            if confParser.has_option(cnfSec,"Recent2"):   self.recentBook[2] = confParser.get(cnfSec,"Recent2")
            if confParser.has_option(cnfSec,"Recent3"):   self.recentBook[3] = confParser.get(cnfSec,"Recent3")
            if confParser.has_option(cnfSec,"Recent4"):   self.recentBook[4] = confParser.get(cnfSec,"Recent4")
            if confParser.has_option(cnfSec,"Recent5"):   self.recentBook[5] = confParser.get(cnfSec,"Recent5")
            if confParser.has_option(cnfSec,"Recent6"):   self.recentBook[6] = confParser.get(cnfSec,"Recent6")
            if confParser.has_option(cnfSec,"Recent7"):   self.recentBook[7] = confParser.get(cnfSec,"Recent7")
            if confParser.has_option(cnfSec,"Recent8"):   self.recentBook[8] = confParser.get(cnfSec,"Recent8")
            if confParser.has_option(cnfSec,"Recent9"):   self.recentBook[9] = confParser.get(cnfSec,"Recent9")

        return

    def saveConfig(self):

        logger.debug("Config: Saving")
        confParser = configparser.ConfigParser()

        # Set options

        ## Main
        cnfSec = "Main"
        confParser.add_section(cnfSec)
        confParser.set(cnfSec,"winWidth",   str(self.winWidth))
        confParser.set(cnfSec,"winHeight",  str(self.winHeight))
        confParser.set(cnfSec,"mainPane",   str(self.mainPane))
        confParser.set(cnfSec,"contPane",   str(self.contPane))
        confParser.set(cnfSec,"editPane",   str(self.editPane))
        confParser.set(cnfSec,"metaPane",   str(self.metaPane))

        ## Editor
        cnfSec = "Editor"
        confParser.add_section(cnfSec)
        confParser.set(cnfSec,"autoSave",   str(self.autoSave))
        confParser.set(cnfSec,"fontSize",   str(self.fontSize))
        confParser.set(cnfSec,"lineHeight", str(self.lineHeight))
        confParser.set(cnfSec,"lineIndent", str(self.lineIndent))
        confParser.set(cnfSec,"parMargin",  str(self.parMargin))
        confParser.set(cnfSec,"pageMargin", str(self.pageMargin))
        confParser.set(cnfSec,"spellCheck", str(self.spellCheck))
        confParser.set(cnfSec,"spellState", str(self.spellState))
        confParser.set(cnfSec,"showPara",   str(self.showPara))

        ## Timer
        cnfSec = "Timer"
        confParser.add_section(cnfSec)
        confParser.set(cnfSec,"autoPause",  str(self.autoPause))
        confParser.set(cnfSec,"minTime",    str(self.minTime))

        ## Path
        cnfSec = "Path"
        confParser.add_section(cnfSec)
        confParser.set(cnfSec,"Recent0",    str(self.recentBook[0]))
        confParser.set(cnfSec,"Recent1",    str(self.recentBook[1]))
        confParser.set(cnfSec,"Recent2",    str(self.recentBook[2]))
        confParser.set(cnfSec,"Recent3",    str(self.recentBook[3]))
        confParser.set(cnfSec,"Recent4",    str(self.recentBook[4]))
        confParser.set(cnfSec,"Recent5",    str(self.recentBook[5]))
        confParser.set(cnfSec,"Recent6",    str(self.recentBook[6]))
        confParser.set(cnfSec,"Recent7",    str(self.recentBook[7]))
        confParser.set(cnfSec,"Recent8",    str(self.recentBook[8]))
        confParser.set(cnfSec,"Recent9",    str(self.recentBook[9]))

        # Write config file
        confParser.write(open(path.join(self.confPath,self.confFile),"w"))
        self.confChanged = False

        return

    ##
    #  Events
    ##

    def onAutoSave(self):
        if self.confChanged:
            logger.debug("Config: Autosaving")
            self.saveConfig()
        return True

    ##
    #  Setters
    ##

    def setWinSize(self, width, height):
        if width != self.winWidth or height != self.winHeight:
            self.winWidth    = width
            self.winHeight   = height
            self.confChanged = True
        return
    
    def setPanes(self, panePos):
        if panePos[0] != self.mainPane:
            self.mainPane    = panePos[0]
            self.confChanged = True
        if panePos[1] != self.contPane:
            self.contPane    = panePos[1]
            self.confChanged = True
        if panePos[2] != self.editPane:
            self.editPane    = panePos[2]
            self.confChanged = True
        if panePos[3] != self.metaPane:
            self.metaPane    = panePos[3]
            self.confChanged = True
        return
    
    def setSpellState(self, state):
        self.spellState = state
        return

    def setLastBook(self, bookPath):
        if bookPath == "": return
        if bookPath in self.recentBook[0:10]:
            self.recentBook.remove(bookPath)
        self.recentBook.insert(0,bookPath)
        self.confChanged = True
        self.updateRecentList()
        return

    ##
    #  Getters
    ##

    def getLastBook(self, bookIdx=0):
        return self.recentBook[bookIdx]

    ##
    #  Methods
    ##

    def updateRecentList(self):
        # for n in range(10):
        #     if self.recentBook[n] == "":
        #         self.getObject("menuFileRecent%d" % n).set_visible(False)
        #     else:
        #         self.getObject("menuFileRecent%d" % n).set_visible(True)
        #         self.getObject("menuFileRecent%d" % n).set_label(self.recentBook[n])
        return

    ##
    #  GUI Actions
    ##

    def onLoad(self, guiObject=None):

        self.dlgBuilder.add_from_file(path.join(self.guiPath,"dlgPreferences.glade"))

        dlgPrefs = self.dlgObject("dlgPreferences")

        guiHandlers = {
            "onClickConfigSave"   : self.onSave,
            "onClickConfigCancel" : self.onClose,
            "onClickConfigClose"  : self.onClose,
        }
        self.dlgBuilder.connect_signals(guiHandlers)

        # Load Current Values
        self.dlgObject("spinFontSIze").set_value(self.fontSize)
        self.dlgObject("spinLineHeight").set_value(self.lineHeight/100.0)
        self.dlgObject("spinLineIndent").set_value(self.lineIndent/100.0)
        self.dlgObject("spinParSpacing").set_value(self.parMargin)
        self.dlgObject("spinPageMargin").set_value(self.pageMargin)
        self.dlgObject("entryLanguage").set_text(self.spellCheck)
        self.dlgObject("spinAutoSave").set_value(self.autoSave)
        self.dlgObject("spinAutoPause").set_value(self.autoPause)
        self.dlgObject("spinMinTime").set_value(self.minTime)

        dlgPrefs.set_transient_for(self.getObject("winMain"))
        dlgPrefs.show_all()

        return

    def onSave(self, guiObject=None):

        self.fontSize   = int(self.dlgObject("spinFontSIze").get_value())
        self.lineHeight = int(self.dlgObject("spinLineHeight").get_value()*100.0)
        self.lineIndent = int(self.dlgObject("spinLineIndent").get_value()*100.0)
        self.parMargin  = int(self.dlgObject("spinParSpacing").get_value())
        self.pageMargin = int(self.dlgObject("spinPageMargin").get_value())
        self.spellCheck = str(self.dlgObject("entryLanguage").get_text())
        self.autoSave   = int(self.dlgObject("spinAutoSave").get_value())
        self.autoPause  = int(self.dlgObject("spinAutoPause").get_value())
        self.minTime    = int(self.dlgObject("spinMinTime").get_value())

        self.saveConfig()
        dlgPrefs = self.dlgObject("dlgPreferences").destroy()

        return

    def onClose(self, guiObject=None):
        dlgPrefs = self.dlgObject("dlgPreferences").destroy()
        return

# End Class Config
