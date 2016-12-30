# -*- coding: utf-8 -*

import logging as logger
import configparser

from os import path

class DataWrapper():

    def __init__(self, dataType):

        # Default Values
        self.dataType = dataType
        self.dataPath = ""
        self.title    = ""
        self.parent   = ""
        self.created  = 0
        self.date     = 0
        self.notes    = ""
        self.hasNotes = False
        self.text     = ""
        self.hasText  = False
        self.words    = 0

        return


    def saveDetails(self):

        logger.debug("Saving data details")
        confParser = configparser.ConfigParser()

        # Set Variables
        cnfSec = self.dataType
        confParser.add_section(cnfSec)
        confParser.set(cnfSec,"Title",  str(self.title))
        confParser.set(cnfSec,"Parent", str(self.parent))
        confParser.set(cnfSec,"Created",str(self.created))
        confParser.set(cnfSec,"Date",   str(self.date))
        confParser.set(cnfSec,"Notes",  str(self.hasNotes))
        confParser.set(cnfSec,"Text",   str(self.hasText))
        confParser.set(cnfSec,"Words",  str(self.words))

        # Write File
        confParser.write(open(path.join(self.dataPath,"details.txt"),"w"))

        return


    def loadDetails(self):

        logger.debug("Loading data details")
        confParser = configparser.ConfigParser()
        confParser.readfp(open(path.join(self.dataPath,"details.txt")))

        # Get Variables
        cnfSec = self.dataType
        if confParser.has_section(cnfSec):
            if confParser.has_option(cnfSec,"Title"):   self.title    = confParser.get(cnfSec,"Title")
            if confParser.has_option(cnfSec,"Parent"):  self.parent   = confParser.get(cnfSec,"Parent")
            if confParser.has_option(cnfSec,"Created"): self.created  = confParser.getint(cnfSec,"Created")
            if confParser.has_option(cnfSec,"Date"):    self.date     = confParser.getint(cnfSec,"Date")
            if confParser.has_option(cnfSec,"Notes"):   self.hasNotes = confParser.getboolean(cnfSec,"Notes")
            if confParser.has_option(cnfSec,"Text"):    self.hasText  = confParser.getboolean(cnfSec,"Text")
            if confParser.has_option(cnfSec,"Words"):   self.words    = confParser.getint(cnfSec,"Words")

        return


    ##
    #  Setters
    ##

    def setTitle(self, newTitle):
        if len(newTitle) > 0:
            self.title = newTitle
        else:
            logger.error("Setting %s title failed." % lower(self.dataType))
        return


    def setDataPath(self, newPath):
        if path.isdir(newPath):
            self.dataPath = newPath
        else:
            logger.error("Path not found: %s" % newPath)
        return


    def setParent(self, newParent):
        self.parent = newParent
        return

# End Class DataWrapper

