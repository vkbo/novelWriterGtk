# -*- coding: utf-8 -*

##
#  novelWriter – Config Class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  This class reads and store the main preferences of the application.
##

import logging as logger
import configparser

from os      import path, mkdir, getcwd
from appdirs import user_config_dir
from nw      import *

class Config:

    def __init__(self):

        # Connect to GUI
        self.getObject  = None

        # Set Application Variables
        self.appName    = "novelWriter"
        self.appHandle  = "novelwriter"
        self.appVersion = "Dev0.3"
        self.appURL     = "https://github.com/Jadzia626/novelWriter"

        # Set Paths
        self.confPath   = user_config_dir(self.appHandle)
        self.confFile   = self.appHandle+".conf"
        self.homePath   = path.expanduser("~")
        self.appPath    = getcwd()
        self.guiPath    = path.join(self.appPath,"gui")

        # If config folder does not exist, make it.
        # This assumes that the os config folder itself exists.
        if not path.isdir(self.confPath):
            mkdir(self.confPath)

        # Set default values
        self.confChanged = False

        ## General
        self.winWidth    = 1000
        self.winHeight   = 700
        self.mainPane    = 200
        self.sidePane    = 200

        ## Editor
        self.autoSave    = 30   # Seconds
        self.fontSize    = 16   # Pixels
        self.lineHeight  = 150  # Percent
        self.lineIndent  = 400  # Percent
        self.parMargin   = 4    # Pixels
        self.pageMargin  = 40   # Pixels
        self.spellCheck  = "en_GB"

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

        logger.debug("Config: Loading")
        confParser = configparser.ConfigParser()
        confParser.readfp(open(path.join(self.confPath,self.confFile)))

        # Get options

        ## Main
        cnfSec = "Main"
        if confParser.has_section(cnfSec):
            if confParser.has_option(cnfSec,"winWidth"):   self.winWidth     = confParser.getint(cnfSec,"winWidth")
            if confParser.has_option(cnfSec,"winHeight"):  self.winHeight    = confParser.getint(cnfSec,"winHeight")
            if confParser.has_option(cnfSec,"mainPane"):   self.mainPane     = confParser.getint(cnfSec,"mainPane")
            if confParser.has_option(cnfSec,"sidePane"):   self.sidePane     = confParser.getint(cnfSec,"sidePane")

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
        confParser.set(cnfSec,"sidePane",   str(self.sidePane))

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

    def doAutoSave(self):
        if self.confChanged:
            logger.debug("Config: Autosaving")
            self.saveConfig()
        return True

    ##
    #  Setters
    ##

    def setBuilder(self, guiBuilder):
        self.getObject = guiBuilder.get_object
        return

    def setWinSize(self, width, height):
        if width != self.winWidth or height != self.winHeight:
            self.winWidth    = width
            self.winHeight   = height
            self.confChanged = True
        return

    def setMainPane(self, position):
        if position != self.mainPane:
            self.mainPane    = position
            self.confChanged = True
        return

    def setSidePane(self, position):
        if position != self.sidePane:
            self.sidePane    = position
            self.confChanged = True
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
        for n in range(10):
            self.getObject("menuFileRecent%d" % n).set_label("%d: %s" % (n,self.recentBook[n]))
        return

# End Class Config
