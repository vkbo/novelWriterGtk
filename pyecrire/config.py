# -*- coding: utf-8 -*

import logging as logger
import configparser

from os      import path, mkdir
from appdirs import user_config_dir

class Config:

    def __init__(self):

        self.appName     = "pyÉcrire"
        self.appNameSafe = "pyEcrire"
        self.appHandle   = "pyecrire"
        self.appVersion  = "0.1"
        self.appURL      = "https://github.com/Jadzia626/pyEcrire"

        self.confPath    = user_config_dir(self.appHandle)
        self.confFile    = self.appHandle+".conf"
        self.homePath    = path.expanduser("~")

        # If config folder does not exist, make it.
        # This assumes that the os config folder itself exists.
        if not path.isdir(self.confPath):
            mkdir(self.confPath)

        # Set default values
        self.confChanged   = False

        ## General
        self.dataPath      = path.join(self.homePath, self.appNameSafe)
        self.winWidth      = 1000
        self.winHeight     = 700
        self.winPane       = 200

        ## Editor
        self.editAutoSave  = 10

        ## Timer
        self.timeAutoPause = 60

        # Check if config file exists
        if path.isfile(path.join(self.confPath,self.confFile)):
            self.loadConfig()

        # Validate config
        self.validateConfig()

        # Always save config after load in case of new values
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
            if confParser.has_option(cnfSec,"dataPath"):  self.dataPath      = confParser.get("Main","dataPath")
            if confParser.has_option(cnfSec,"winWidth"):  self.winWidth      = confParser.getint("Main","winWidth")
            if confParser.has_option(cnfSec,"winHeight"): self.winHeight     = confParser.getint("Main","winHeight")
            if confParser.has_option(cnfSec,"winPane"):   self.winPane       = confParser.getint("Main","winPane")

        ## Editor
        cnfSec = "Editor"
        if confParser.has_section(cnfSec):
            if confParser.has_option(cnfSec,"AutoSave"):  self.editAutoSave  = confParser.getint("Editor","AutoSave")

        ## Timer
        cnfSec = "Timer"
        if confParser.has_section(cnfSec):
            if confParser.has_option(cnfSec,"AutoPause"): self.timeAutoPause = confParser.getint("Timer","AutoPause")

        return


    def saveConfig(self):

        logger.debug("Saving config")
        confParser = configparser.ConfigParser()

        # Set options

        ## Main
        confParser.add_section("Main")
        confParser.set("Main","dataPath",  self.dataPath)
        confParser.set("Main","winWidth",  str(self.winWidth))
        confParser.set("Main","winHeight", str(self.winHeight))
        confParser.set("Main","winPane",   str(self.winPane))

        ## Editor
        confParser.add_section("Editor")
        confParser.set("Editor","AutoSave",str(self.editAutoSave))

        ## Timer
        confParser.add_section("Timer")
        confParser.set("Timer","AutoPause",str(self.timeAutoPause))

        # Write config file
        confParser.write(open(path.join(self.confPath,self.confFile),"w"))
        self.confChanged = False

        return


    def validateConfig(self):
        if not path.isdir(self.dataPath):
            logger.debug("Data path does not exist")
            self.dataPath = path.join(self.homePath, self.appNameSafe)
            mkdir(self.dataPath)
            logger.debug("Created folder %s" % self.dataPath)
        return


    def autoSaveConfig(self):
        if self.confChanged:
            logger.debug("Auto-saving config")
            self.saveConfig()
        return


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


    def setWinPane(self, width):
        if width != self.winPane:
            logger.debug("Pane size changed")
            self.winPane = width
            self.confChanged = True
        return

