# -*- coding: utf-8 -*

import logging as logger
import configparser

from os      import path, mkdir
from appdirs import *

class Config:

    def __init__(self):

        self.appName     = "pyÉcrire"
        self.appNameSafe = "pyEcrire"
        self.appHandle   = "pyecrire"

        self.confPath    = user_config_dir(self.appHandle)
        self.confFile    = self.appHandle+".conf"
        self.homePath    = path.expanduser("~")

        # If config folder does not exist, make it.
        # This assumes that the os config folder itself exists.
        if not path.isdir(self.confPath):
            mkdir(self.confPath)

        # Set default values

        ## General
        self.dataPath      = path.join(self.homePath, self.appNameSafe)

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


    def loadConfig(self):

        logger.debug("Loading config")
        confParser = configparser.ConfigParser()
        confParser.readfp(open(path.join(self.confPath,self.confFile)))

        # Get options

        ## Main
        if confParser.has_section("Main"):
            self.dataPath = confParser.get("Main","dataPath")

        ## Editor
        if confParser.has_section("Editor"):
            self.editAutoSave = confParser.getint("Editor","AutoSave")

        ## Timer
        if confParser.has_section("Timer"):
            self.timeAutoPause = confParser.getint("Timer","AutoPause")


    def saveConfig(self):

        logger.debug("Saving config")
        confParser = configparser.ConfigParser()

        # Set options

        ## Main
        confParser.add_section("Main")
        confParser.set("Main","dataPath",self.dataPath)

        ## Editor
        confParser.add_section("Editor")
        confParser.set("Editor","AutoSave",str(self.editAutoSave))

        ## Timer
        confParser.add_section("Timer")
        confParser.set("Timer","AutoPause",str(self.timeAutoPause))

        # Write config file
        confParser.write(open(path.join(self.confPath,self.confFile),"w"))


    def validateConfig(self):

        if not path.isdir(self.dataPath):
            logger.debug("Data path does not exist")
            self.dataPath = path.join(self.homePath, self.appNameSafe)
            mkdir(self.dataPath)
            logger.debug("Created folder %s" % self.dataPath)

