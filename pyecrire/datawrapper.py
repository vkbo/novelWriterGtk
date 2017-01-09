# -*- coding: utf-8 -*

##
#  pyÉcrire – Data Wrapper Class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  This class wraps the actual data files related to the different data types.
#  All file reading and writing is done in this class.
##

import logging as logger
import configparser

from os                 import path, listdir
from hashlib            import sha256
from datetime           import datetime
from pyecrire           import *
from pyecrire.functions import makeTimeStamp, htmlCleanUp, wordCount, dateFromString

class DataWrapper():

    def __init__(self, dataType):

        # Connect to GUI
        self.mainConf = CONFIG

        # Default Values
        self.dataType   = ""
        self.dataPath   = ""
        self.parType    = ""
        self.fileList   = {}
        self.listLen    = 0
        self.fileToLoad   = ""
        self.currFile   = ""
        self.editFormat = ""
        self.fileHash   = ""
        self.timeList   = []
        self.timeTotal  = 0.0
        self.prevWords  = 0
        self.prevChars  = 0

        # General Values
        self.title      = ""
        self.created    = ""
        self.date       = ""
        self.parent     = ""

        # File Specific Values
        self.notes      = ""
        self.hasNotes   = False
        self.text       = ""
        self.hasText    = False
        self.words      = 0
        self.chars      = 0
        self.number     = 0

        # Scene Specific Values
        self.section    = 0
        self.chapter    = 0
        self.pov        = ""

        # Book Specific Values
        self.category   = ""
        self.status     = ""

        self.setDataType(dataType)

        return

    def makeList(self):

        fileList    = {}
        fileExclude = ["details.txt","timing.txt"]

        if path.isdir(self.dataPath):
            dirContent = listdir(self.dataPath)

            for listItem in dirContent:
                itemPath = path.join(self.dataPath,listItem)
                if path.isfile(itemPath):
                    itemExt = listItem[-3:]
                    if itemExt == "txt" and listItem not in fileExclude:
                        itemHandle = listItem[0:15]
                        fileList[itemHandle] = itemPath

            self.listLen = len(fileList)
        else:
            logger.error("Path not found: %s" % self.dataPath)

        fileKey = ""
        for fileKey in sorted(fileList):
            self.fileList[fileKey] = fileList[fileKey]

        if fileKey != "":
            self.fileToLoad = fileList[fileKey]
            fileDate        = dateFromString(fileKey,1)
            fileAge         = (datetime.now()-fileDate).total_seconds()/60.
            if fileAge < self.mainConf.versionAge:
                self.currFile = self.fileToLoad

        return

    ##
    #  Meta Data Functions (details.txt)
    ##

    def loadDetails(self):

        logger.debug("Loading data details")

        # General Values
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
        self.chars    = 0
        self.number   = 0

        # Scene Specific Values
        self.section  = 0
        self.chapter  = 0
        self.pov      = ""

        # Book Specific Values
        self.category = ""
        self.status   = ""

        confParser = configparser.ConfigParser()
        confParser.readfp(open(path.join(self.dataPath,"details.txt")))

        # Get Variables
        cnfSec = self.dataType
        if confParser.has_section(cnfSec):
            if confParser.has_option(cnfSec,"Title"):    self.title    = confParser.get(cnfSec,"Title")
            if confParser.has_option(cnfSec,"Created"):  self.created  = confParser.get(cnfSec,"Created")
            if confParser.has_option(cnfSec,"Date"):     self.date     = confParser.get(cnfSec,"Date")
            if confParser.has_option(cnfSec,"Number"):   self.number   = confParser.getint(cnfSec,"Number")
            if confParser.has_option(cnfSec,"Parent"):   self.parent   = confParser.get(cnfSec,"Parent")
            if confParser.has_option(cnfSec,"Notes"):    self.hasNotes = confParser.getboolean(cnfSec,"Notes")
            if confParser.has_option(cnfSec,"Text"):     self.hasText  = confParser.getboolean(cnfSec,"Text")
            if confParser.has_option(cnfSec,"Words"):    self.words    = confParser.getint(cnfSec,"Words")
            if confParser.has_option(cnfSec,"Chars"):    self.chars    = confParser.getint(cnfSec,"Chars")
            if confParser.has_option(cnfSec,"Section"):  self.section  = confParser.getint(cnfSec,"Section")
            if confParser.has_option(cnfSec,"Chapter"):  self.chapter  = confParser.getint(cnfSec,"Chapter")
            if confParser.has_option(cnfSec,"POV"):      self.pov      = confParser.get(cnfSec,"POV")
            if confParser.has_option(cnfSec,"Category"): self.category = confParser.get(cnfSec,"Category")
            if confParser.has_option(cnfSec,"Status"):   self.status   = confParser.get(cnfSec,"Status")

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
        confParser.set(cnfSec,"Number",  str(self.number))
        if self.dataType != NAME_UNIV:
            confParser.set(cnfSec,"Parent",   str(self.parent))
        if self.dataGroup == TYPE_FILE:
            confParser.set(cnfSec,"Notes",    str(self.hasNotes))
            confParser.set(cnfSec,"Text",     str(self.hasText))
            confParser.set(cnfSec,"Words",    str(self.words))
            confParser.set(cnfSec,"Chars",    str(self.chars))
        if self.dataType == NAME_SCNE:
            confParser.set(cnfSec,"Section",  str(self.section))
            confParser.set(cnfSec,"Chapter",  str(self.chapter))
            confParser.set(cnfSec,"POV",      str(self.pov))
        if self.dataType == NAME_BOOK:
            confParser.set(cnfSec,"Category", str(self.category))
            confParser.set(cnfSec,"Status",   str(self.status))

        # Write File
        confParser.write(open(path.join(self.dataPath,"details.txt"),"w"))

        return

    ##
    #  Timing Functions (timing.txt)
    ##

    def loadTiming(self):

        timeFile = path.join(self.dataPath,"timing.txt")
        if not path.isfile(timeFile): return
        logger.debug("Loading timing information")

        fileObj = open(timeFile,"r")
        tmpData = fileObj.read()
        fileObj.close()

        self.timeList  = []
        self.timeTotal = 0.0
        tmpLines = tmpData.split("\n")
        for tmpLine in tmpLines:
            tmpValues = tmpLine.split(",")
            if len(tmpValues) == 4:
                self.timeList.append(tmpValues)
                self.timeTotal += float(tmpValues[1])

        return

    def saveTiming(self, timeValue):

        if timeValue < self.mainConf.timeCutOff: return

        logger.debug("Saving timing information")

        self.timeTotal += timeValue

        timeStamp = makeTimeStamp(0)
        timeValue = str(timeValue)
        wordCount = str(self.words - self.prevWords)
        charCount = str(self.chars - self.prevChars)

        self.timeList.append([timeStamp,timeValue,wordCount,charCount])

        timeFile = path.join(self.dataPath,"timing.txt")
        timeSet  = timeStamp+","+timeValue+","+wordCount+","+charCount+"\n"
        fileObj  = open(timeFile,"a+")
        fileObj.write(timeSet)
        fileObj.close()

        return

    ##
    #  File Text Functions ([timestamp].txt)
    ##

    def loadText(self):

        logger.debug("Loading text file")

        if self.fileToLoad == "":
            self.text = "<p>New File</p>"
        else:
            fileObj   = open(path.join(self.dataPath,self.fileToLoad),encoding="utf-8",mode="r")
            self.text = fileObj.read()
            fileObj.close()

        self.fileHash = sha256(str(self.text).encode()).hexdigest()
        self.hasText  = True

        return

    def saveText(self):

        if not self.hasText: return
        if self.dataGroup is not TYPE_FILE: return

        logger.debug("Saving text file")

        if self.currFile == "": self.currFile = makeTimeStamp(1)+".txt"

        fileObj = open(path.join(self.dataPath,self.currFile),encoding="utf-8",mode="w")
        fileObj.write(self.text)
        fileObj.close()

        self.fileHash = sha256(str(self.text).encode()).hexdigest()
        self.makeList()
        self.saveDetails()

        return

    def doAutoSaveText(self):

        fileHash = sha256(str(self.text).encode()).hexdigest()

        if not self.hasText:                return False
        if self.dataGroup is not TYPE_FILE: return False
        if self.fileHash == fileHash:       return False

        logger.debug("Auto-saving text file")

        self.saveText()

        return True

    ##
    #  Getters
    ##

    def getFilePath(self, fileHandle):
        if fileHandle in self.fileList:
            return self.fileList[fileHandle]
        else:
            return None

    ##
    #  Setters
    ##

    def setDataType(self, dataType):

        self.dataType = dataType

        if   dataType == NAME_BOOK:
            self.dataGroup  = TYPE_CONT
            self.parType    = NAME_NONE
        elif dataType == NAME_UNIV:
            self.dataGroup  = TYPE_CONT
            self.parType    = NAME_NONE
        elif dataType == NAME_PLOT:
            self.dataGroup = TYPE_FILE
            self.parType   = NAME_BOOK
            self.editFormat = self.mainConf.plotFormat
        elif dataType == NAME_SCNE:
            self.dataGroup  = TYPE_FILE
            self.parType    = NAME_BOOK
            self.editFormat = self.mainConf.scneFormat
        elif dataType == NAME_HIST:
            self.dataGroup  = TYPE_FILE
            self.parType    = NAME_UNIV
            self.editFormat = self.mainConf.histFormat
        elif dataType == NAME_CHAR:
            self.dataGroup  = TYPE_FILE
            self.parType    = NAME_UNIV
            self.editFormat = self.mainConf.charFormat
        else:
            self.dataGroup = TYPE_NONE
            self.parType   = NAME_NONE

        return

    def setDataPath(self, newPath):
        if path.isdir(newPath):
            self.dataPath = newPath
            self.makeList()
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

    def setText(self, srcText):
        if len(srcText) > 0:
            words,chars  = wordCount(srcText)
            srcText      = htmlCleanUp(srcText)
            self.text    = srcText
            self.hasText = True
            self.words   = words
            self.chars   = chars
        return

    def setFileToLoad(self, filePath):
        self.fileToLoad = filePath
        return

# End Class DataWrapper
