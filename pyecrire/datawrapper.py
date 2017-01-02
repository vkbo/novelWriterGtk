# -*- coding: utf-8 -*

import logging as logger
import configparser

from os                 import path
from pyecrire.functions import makeTimeStamp

class DataWrapper():

    def __init__(self, dataType):

        if   dataType == "Book":
            self.dataGroup = "Container"
        elif dataType == "Universe":
            self.dataGroup = "Container"
        elif dataType == "Scene":
            self.dataGroup = "File"
        elif dataType == "Plot":
            self.dataGroup = "File"
        elif dataType == "Character":
            self.dataGroup = "File"
        elif dataType == "History":
            self.dataGroup = "File"
        else:
            self.dataGroup = ""

        # Default Values
        self.dataType = dataType
        self.dataPath = ""
        self.title    = ""
        self.created  = ""
        self.date     = ""
        self.parent   = ""

        # File Specific Values
        self.notes    = ""
        self.hasNotes = False
        self.text     = ""
        self.hasText  = False
        self.words    = 0
        self.number   = 0

        # Scene Specific Values
        self.section  = 0
        self.chapter  = 0
        self.pov      = ""

        # Book Specific Values
        self.category = ""
        self.status   = ""

        return

    def saveDetails(self):

        logger.debug("Saving data details")
        confParser = configparser.ConfigParser()

        # Set or Update TimeStamps
        if self.created == "":
            self.created = makeTimeStamp(3)
        self.date = makeTimeStamp(3)

        # Set Variables
        cnfSec = self.dataType
        confParser.add_section(cnfSec)
        confParser.set(cnfSec,"Title",   str(self.title))
        confParser.set(cnfSec,"Created", str(self.created))
        confParser.set(cnfSec,"Date",    str(self.date))
        if self.dataType != "Universe":
            confParser.set(cnfSec,"Parent",   str(self.parent))
        if self.dataGroup == "File":
            confParser.set(cnfSec,"Notes",    str(self.hasNotes))
            confParser.set(cnfSec,"Text",     str(self.hasText))
            confParser.set(cnfSec,"Words",    str(self.words))
            confParser.set(cnfSec,"Number",   str(self.number))
        if self.dataType == "Scene":
            confParser.set(cnfSec,"Section",  str(self.section))
            confParser.set(cnfSec,"Chapter",  str(self.chapter))
            confParser.set(cnfSec,"POV",      str(self.pov))
        if self.dataType == "Book":
            confParser.set(cnfSec,"Category", str(self.category))
            confParser.set(cnfSec,"Status",   str(self.status))

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
            if confParser.has_option(cnfSec,"Title"):    self.title    = confParser.get(cnfSec,"Title")
            if confParser.has_option(cnfSec,"Created"):  self.created  = confParser.get(cnfSec,"Created")
            if confParser.has_option(cnfSec,"Date"):     self.date     = confParser.get(cnfSec,"Date")
            if confParser.has_option(cnfSec,"Parent"):   self.parent   = confParser.get(cnfSec,"Parent")
            if confParser.has_option(cnfSec,"Notes"):    self.hasNotes = confParser.getboolean(cnfSec,"Notes")
            if confParser.has_option(cnfSec,"Text"):     self.hasText  = confParser.getboolean(cnfSec,"Text")
            if confParser.has_option(cnfSec,"Words"):    self.words    = confParser.getint(cnfSec,"Words")
            if confParser.has_option(cnfSec,"Number"):   self.number   = confParser.getint(cnfSec,"Number")
            if confParser.has_option(cnfSec,"Section"):  self.section  = confParser.getint(cnfSec,"Section")
            if confParser.has_option(cnfSec,"Chapter"):  self.chapter  = confParser.getint(cnfSec,"Chapter")
            if confParser.has_option(cnfSec,"POV"):      self.pov      = confParser.get(cnfSec,"POV")
            if confParser.has_option(cnfSec,"Category"): self.category = confParser.get(cnfSec,"Category")
            if confParser.has_option(cnfSec,"Status"):   self.status   = confParser.get(cnfSec,"Status")

        return

    ##
    #  Getters
    ##

    def getText(self):
        return "<p>Hello Kitty</p>"

    ##
    #  Setters
    ##

    def setDataType(self, dataType):
        self.dataType = dataType
        return

    def setDataPath(self, newPath):
        if path.isdir(newPath):
            self.dataPath = newPath
        else:
            logger.error("Path not found: %s" % newPath)
        return

    def setTitle(self, newTitle):
        if len(newTitle) > 0:
            self.title = newTitle
        else:
            logger.error("Setting %s title failed." % lower(self.dataType))
        return

    def setParent(self, newParent):
        self.parent = newParent
        return

    def setNumber(self, newNumber):
        if newNumber < 0:   newNumber = 0
        if newNumber > 999: newNumber = 999
        self.number = newNumber
        print(newNumber)
        return

    def setSection(self, newSection):
        if newSection < 0: newSection = 0
        if newSection > 3: newSection = 3
        self.section = newSection
        return

    def setChapter(self, newChapter):
        if newChapter < 0:  newChapter = 0
        if newChapter > 99: newChapter = 99
        self.chapter = newChapter
        return

    def setPOV(self, charHandle):
        self.pov = charHandle
        return

# End Class DataWrapper
