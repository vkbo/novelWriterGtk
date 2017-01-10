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
        self.dataPath   = path.join(self.homePath, self.appName)
        self.winWidth   = 1000
        self.winHeight  = 700
        self.mainPane   = 200
        self.sidePane   = 200

        ## Editor
        self.autoSave   = 30   # Seconds
        self.versionAge = 60   # Minutes
        self.fontSize   = 16   # Pixels
        self.lineHeight = 150  # Percent
        self.lineIndent = 400  # Percent
        self.parMargin  = 4    # Pixels

        ## Timer
        self.autoPause  = 60   # Seconds

        # Check if config file exists
        if path.isfile(path.join(self.confPath,self.confFile)):
            self.loadConfig()

        # Validate config
        self.validateConfig()

        # Save a copy of the default config if no file exists
        if not path.isfile(path.join(self.confPath,self.confFile)):
            self.saveConfig()

        return

    ##
    #  Actions
    ##

    def loadConfig(self):

        logger.debug("Loading config")
        confParser = configparser.ConfigParser()
        confParser.readfp(open(path.join(self.confPath,self.confFile)))

        # Get options

        ## Main
        cnfSec = "Main"
        if confParser.has_section(cnfSec):
            if confParser.has_option(cnfSec,"dataPath"):   self.dataPath   = confParser.get("Main","dataPath")
            if confParser.has_option(cnfSec,"winWidth"):   self.winWidth   = confParser.getint("Main","winWidth")
            if confParser.has_option(cnfSec,"winHeight"):  self.winHeight  = confParser.getint("Main","winHeight")
            if confParser.has_option(cnfSec,"mainPane"):   self.mainPane   = confParser.getint("Main","mainPane")
            if confParser.has_option(cnfSec,"sidePane"):   self.sidePane   = confParser.getint("Main","sidePane")

        ## Editor
        cnfSec = "Editor"
        if confParser.has_section(cnfSec):
            if confParser.has_option(cnfSec,"autoSave"):   self.autoSave   = confParser.getint("Editor","autoSave")
            if confParser.has_option(cnfSec,"versionAge"): self.versionAge = confParser.getint("Editor","versionAge")
            if confParser.has_option(cnfSec,"fontSize"):   self.fontSize   = confParser.getint("Editor","fontSize")
            if confParser.has_option(cnfSec,"lineHeight"): self.lineHeight = confParser.getint("Editor","lineHeight")
            if confParser.has_option(cnfSec,"lineIndent"): self.lineIndent = confParser.getint("Editor","lineIndent")
            if confParser.has_option(cnfSec,"parMargin"):  self.parMargin  = confParser.getint("Editor","parMargin")

        ## Timer
        cnfSec = "Timer"
        if confParser.has_section(cnfSec):
            if confParser.has_option(cnfSec,"AutoPause"):  self.autoPause  = confParser.getint("Timer","AutoPause")

        return

    def saveConfig(self):

        logger.debug("Saving config")
        confParser = configparser.ConfigParser()

        # Set options

        ## Main
        confParser.add_section("Main")
        confParser.set("Main","dataPath",     str(self.dataPath))
        confParser.set("Main","winWidth",     str(self.winWidth))
        confParser.set("Main","winHeight",    str(self.winHeight))
        confParser.set("Main","mainPane",     str(self.mainPane))
        confParser.set("Main","sidePane",     str(self.sidePane))

        ## Editor
        confParser.add_section("Editor")
        confParser.set("Editor","autoSave",   str(self.autoSave))
        confParser.set("Editor","versionAge", str(self.versionAge))
        confParser.set("Editor","fontSize",   str(self.fontSize))
        confParser.set("Editor","lineHeight", str(self.lineHeight))
        confParser.set("Editor","lineIndent", str(self.lineIndent))
        confParser.set("Editor","parMargin",  str(self.parMargin))

        ## Timer
        confParser.add_section("Timer")
        confParser.set("Timer","autoPause",   str(self.autoPause))

        # Write config file
        confParser.write(open(path.join(self.confPath,self.confFile),"w"))
        self.confChanged = False

        return

    def validateConfig(self):
        if not path.isdir(self.dataPath):
            logger.debug("Data path does not exist")
            self.dataPath = path.join(self.homePath, self.appName)
            mkdir(self.dataPath)
            logger.debug("Created folder %s" % self.dataPath)
        return

    def doAutoSaveConfig(self):

        if not self.confChanged: return False

        logger.debug("Auto-saving config")
        self.saveConfig()

        return True

    ##
    #  Setters
    ##

    def setWinSize(self, width, height):
        if width != self.winWidth or height != self.winHeight:
            logger.debug("Window size changed")
            self.winWidth  = width
            self.winHeight = height
            self.confChanged = True
        return

    def setMainPane(self, position):
        if position != self.mainPane:
            logger.debug("Pane size changed")
            self.mainPane = position
            self.confChanged = True
        return

    def setSidePane(self, position):
        if position != self.sidePane:
            logger.debug("Pane size changed")
            self.sidePane = position
            self.confChanged = True
        return

# End Class Config
