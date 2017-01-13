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

        self.appName    = "novelWriter"
        self.appHandle  = "novelwriter"
        self.appVersion = "0.1"
        self.appURL     = "https://github.com/Jadzia626/novelWriter"

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

        ## Timer
        self.autoPause   = 60   # Seconds
        self.minTime     = 10   # Seconds

        ## Paths
        self.lastBook    = ""
        self.lastFile    = ""

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
            if confParser.has_option(cnfSec,"winWidth"):   self.winWidth   = confParser.getint(cnfSec,"winWidth")
            if confParser.has_option(cnfSec,"winHeight"):  self.winHeight  = confParser.getint(cnfSec,"winHeight")
            if confParser.has_option(cnfSec,"mainPane"):   self.mainPane   = confParser.getint(cnfSec,"mainPane")
            if confParser.has_option(cnfSec,"sidePane"):   self.sidePane   = confParser.getint(cnfSec,"sidePane")

        ## Editor
        cnfSec = "Editor"
        if confParser.has_section(cnfSec):
            if confParser.has_option(cnfSec,"autoSave"):   self.autoSave   = confParser.getint(cnfSec,"autoSave")
            if confParser.has_option(cnfSec,"fontSize"):   self.fontSize   = confParser.getint(cnfSec,"fontSize")
            if confParser.has_option(cnfSec,"lineHeight"): self.lineHeight = confParser.getint(cnfSec,"lineHeight")
            if confParser.has_option(cnfSec,"lineIndent"): self.lineIndent = confParser.getint(cnfSec,"lineIndent")
            if confParser.has_option(cnfSec,"parMargin"):  self.parMargin  = confParser.getint(cnfSec,"parMargin")
            if confParser.has_option(cnfSec,"pageMargin"): self.pageMargin = confParser.getint(cnfSec,"pageMargin")

        ## Timer
        cnfSec = "Timer"
        if confParser.has_section(cnfSec):
            if confParser.has_option(cnfSec,"autoPause"):  self.autoPause  = confParser.getint(cnfSec,"autoPause")
            if confParser.has_option(cnfSec,"minTime"):    self.minTime    = confParser.getint(cnfSec,"minTime")
 
        ## Path
        cnfSec = "Path"
        if confParser.has_section(cnfSec):
            if confParser.has_option(cnfSec,"lastBook"):   self.lastBook   = confParser.get(cnfSec,"lastBook")
            if confParser.has_option(cnfSec,"lastFile"):   self.lastFile   = confParser.get(cnfSec,"lastFile")

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

        ## Timer
        cnfSec = "Timer"
        confParser.add_section(cnfSec)
        confParser.set(cnfSec,"autoPause",  str(self.autoPause))
        confParser.set(cnfSec,"minTime",    str(self.minTime))

        ## Path
        cnfSec = "Path"
        confParser.add_section(cnfSec)
        confParser.set(cnfSec,"lastBook",   str(self.lastBook))
        confParser.set(cnfSec,"lastFile",   str(self.lastFile))

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
        self.lastBook    = bookPath
        self.confChanged = True
        return

    def setLastFile(self, fileHandle):
        self.lastFile    = fileHandle
        self.confChanged = True
        return

# End Class Config
