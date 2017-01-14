# -*- coding: utf-8 -*

##
#  novelWriter – Scene Meta Class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Holds the metadata of the loaded scene
##

import logging as logger
import configparser

from time import time
from os   import path
from nw   import *

class SceneMeta():

    def __init__(self, theOpt):

        # Core Objects
        self.mainConf     = CONFIG
        self.theOpt       = theOpt

        # Saved Attributes
        self.sceneTitle   = ""
        self.sceneCreated = formatDateTime()
        self.sceneUpdated = formatDateTime()
        self.sceneSection = 0
        self.sceneChapter = 1
        self.sceneNumber  = 1
        self.sceneWords   = 0
        self.sceneChars   = 0

        # Runtime Attributes
        self.sceneChanged = False

        return

    def clearContent(self):

        # Clear Saved Attributes
        self.sceneTitle   = ""
        self.sceneCreated = formatDateTime()
        self.sceneUpdated = formatDateTime()
        self.sceneSection = 0
        self.sceneChapter = 1
        self.sceneNumber  = 1
        self.sceneWords   = 0
        self.sceneChars   = 0

        # Runtime Attributes
        self.sceneChanged = False

        return

    ##
    #  Load and Save
    ##

    def loadData(self):

        sceneFolder = self.theOpt.sceneFolder
        sceneHandle = self.theOpt.sceneHandle

        if not path.isdir(sceneFolder):
            logger.debug("SceneMeta.loadData: Folder not found %s" % sceneFolder)
            return

        if sceneHandle == "" or sceneHandle is None:
            logger.error("SceneMeta.loadData: File handle missing")
            return

        fileName = "%s-metadata.cnf" % self.sceneHandle
        filePath = path.join(sceneFolder,fileName)

        if not path.isfile(filePath):
            logger.error("SceneMeta.loadData: File not found %s" % filePath)
            return

        logger.debug("SceneMeta.loadData: Loading scene metadata")

        confParser = configparser.ConfigParser()
        confParser.readfp(open(filePath,"r"))

        # Get Variables
        cnfSec = "Scene"
        if confParser.has_section(cnfSec):
            if confParser.has_option(cnfSec,"Title"):   self.sceneTitle   = confParser.get(cnfSec,"Title")
            if confParser.has_option(cnfSec,"Created"): self.sceneCreated = confParser.get(cnfSec,"Created")
            if confParser.has_option(cnfSec,"Updated"): self.sceneUpdated = confParser.get(cnfSec,"Updated")
            if confParser.has_option(cnfSec,"Section"): self.sceneSection = confParser.getint(cnfSec,"Section")
            if confParser.has_option(cnfSec,"Chapter"): self.sceneChapter = confParser.getint(cnfSec,"Chapter")
            if confParser.has_option(cnfSec,"Number"):  self.sceneNumber  = confParser.getint(cnfSec,"Number")
            if confParser.has_option(cnfSec,"Words"):   self.sceneWords   = confParser.getint(cnfSec,"Words")
            if confParser.has_option(cnfSec,"Chars"):   self.sceneChars   = confParser.getint(cnfSec,"Chars")

        self.sceneChanged = False

        return

    def saveData(self):

        sceneFolder = self.theOpt.sceneFolder
        sceneHandle = self.theOpt.sceneHandle

        if not path.isdir(sceneFolder):
            logger.debug("SceneMeta.saveScene: Folder not found %s" % sceneFolder)
            return

        if sceneHandle == "" or sceneHandle is None:
            logger.error("SceneMeta.saveScene: File handle missing")
            return

        logger.debug("SceneMeta.saveScene: Saving scene metadata")

        fileName   = "%s-metadata.cnf" % self.sceneHandle
        filePath   = path.join(sceneFolder,fileName)
        confParser = configparser.ConfigParser()

        # Set Variables
        cnfSec = "Scene"
        confParser.add_section(cnfSec)
        confParser.set(cnfSec,"Title",   str(self.sceneTitle))
        confParser.set(cnfSec,"Created", str(self.sceneCreated))
        confParser.set(cnfSec,"Updated", str(self.sceneUpdated))
        confParser.set(cnfSec,"Section", str(self.sceneSection))
        confParser.set(cnfSec,"Chapter", str(self.sceneChapter))
        confParser.set(cnfSec,"Number",  str(self.sceneNumber))
        confParser.set(cnfSec,"Words",   str(self.sceneWords))
        confParser.set(cnfSec,"Chars",   str(self.sceneChars))

        # Write File
        confParser.write(open(filePath,"w"))

        self.sceneChanged = False

        return

    ##
    #  Setters
    ##

    def setTitle(self, newTitle):
        newTitle = newTitle.strip()
        if len(newTitle) > 0:
            self.sceneTitle   = newTitle
            self.sceneChanged = True
        else:
            logger.error("SceneMeta.setTitle: Invalid scene title '%s'" % newTitle)
        return
        
    def setUpdated(self, newDate):
        if len(newTitle) > 0:
            self.sceneUpdated = newDate
            self.sceneChanged = True
        else:
            logger.error("SceneMeta.setUpdated: Invalid date")
        return
        
    def setSection(self, sceneSection):
        if sceneSection < 0: sceneSection = 0
        if sceneSection > 3: sceneSection = 3
        self.sceneSection = sceneSection
        if sceneSection != 2: self.sceneSection = 0
        self.sceneChanged = True
        return

    def setChapter(self, sceneChapter):
        if sceneChapter < 1:  sceneChapter = 1
        if sceneChapter > 99: sceneChapter = 99
        if self.sceneChapter != 2: sceneChapter = 0
        self.sceneChapter = sceneChapter
        self.sceneChanged = True
        return

    def setNumber(self, sceneNumber):
        if sceneNumber < 1:   sceneNumber = 1
        if sceneNumber > 999: sceneNumber = 999
        self.sceneNumber  = sceneNumber
        self.sceneChanged = True
        return

    def setWords(self, sceneWords):
        if sceneWords < 0: sceneWords = 0
        self.sceneWords   = sceneWords
        self.sceneChanged = True
        return

    def setChars(self, sceneChars):
        if sceneChars < 0: sceneChars = 0
        self.sceneChars   = sceneChars
        self.sceneChanged = True
        return

    ##
    #  Getters
    ##

    def getTitle(self):
        return self.sceneTitle

    def getCreated(self):
        return self.sceneCreated

    def getUpdated(self):
        return self.sceneUpdated

    def getSection(self):
        return self.sceneSection

    def getChapter(self):
        return self.sceneChapter

    def getNumber(self):
        return self.sceneNumber

    def getWords(self):
        return self.sceneWords

    def getChars(self):
        return self.sceneChars

# End Class SceneMeta
