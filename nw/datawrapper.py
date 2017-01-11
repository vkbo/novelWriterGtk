# -*- coding: utf-8 -*

##
#  novelWriter – Data Wrapper
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Wrapper classes for data files
##

import logging as logger
import configparser

from os      import path, mkdir
from hashlib import sha256
from time    import time
from re      import sub
from bleach  import clean
from nw      import *

# ==================================================================================================================== #
# Begin Class BookData
"""
  Main Data Wrapper Class for Book Data
 –––––––––––––––––––––––––––––––––––––––
"""

class BookData():

    def __init__(self):

        self.mainConf   = CONFIG

        self.bookTitle  = ""
        self.bookAuthor = ""
        self.bookFolder = ""
        self.bookDraft  = 1

        self.bookLoaded = False

        return

    def loadBook(self, loadPath):

        if loadPath == "": return

        self.bookFolder = loadPath

        confParser = configparser.ConfigParser()
        confParser.readfp(open(path.join(self.bookFolder,"metadata.cnf")))

        # Get Variables
        cnfSec = "Book"
        if confParser.has_section(cnfSec):
            if confParser.has_option(cnfSec,"Title"):  self.bookTitle  = confParser.get(cnfSec,"Title")
            if confParser.has_option(cnfSec,"Author"): self.bookAuthor = confParser.get(cnfSec,"Author")
            if confParser.has_option(cnfSec,"Draft"):  self.bookDraft  = confParser.get(cnfSec,"Draft")

        self.mainConf.setLastBook(self.bookFolder)

        self.bookLoaded = True

        return

    def saveBook(self):

        logger.debug("Saving Book Data")
        confParser = configparser.ConfigParser()

        # Set Variables
        cnfSec = "Book"
        confParser.add_section(cnfSec)
        confParser.set(cnfSec,"Title",  str(self.bookTitle))
        confParser.set(cnfSec,"Author", str(self.bookAuthor))
        confParser.set(cnfSec,"Draft",  str(self.bookDraft))

        # Write File
        confParser.write(open(path.join(self.bookFolder,"metadata.cnf"),"w"))
        self.mainConf.setLastBook(self.bookFolder)

        return

    ##
    #  Getters
    ##

    def getFilesPath(self):
        if self.bookFolder == "": return None
        return path.join(self.bookFolder,"Draft %d" % self.bookDraft)

    ##
    #  Setters
    ##

    def setTitle(self, title):
        self.bookTitle = title.strip()
        return

    def setAuthor(self, author):
        self.bookAuthor = author.strip()
        return

    def setBookFolder(self, folder):
        if path.isdir(folder) and self.bookTitle != "":
            self.bookFolder = path.join(folder,self.bookTitle)
            if not path.isdir(self.bookFolder):
                mkdir(self.bookFolder)
        return

# End Class BookData
# ==================================================================================================================== #
# Begin Class SceneData

class SceneData():

    def __init__(self):

        self.fileTitle   = ""
        self.fileFolder  = ""
        self.fileHandle  = sha256(str(time()).encode()).hexdigest()[0:12]
        self.fileCreated = formatDateTime()
        self.fileUpdated = formatDateTime()
        self.fileVersion = 1
        self.fileSection = 0
        self.fileChapter = 0
        self.fileNumber  = 0

        self.theText     = TextFile()
        
        self.fileLoaded  = False

        return

    ##
    #  Load Functions
    ##

    def loadScene(self, fileHandle):

        if self.fileFolder == "":
            logger.error("SceneData: No folder specified")
            return False

        if fileHandle == "" or fileHandle is None:
            logger.error("SceneData: File handle missing")
            return False

        self.fileHandle = fileHandle

        fileName = "%s-metadata.cnf" % self.fileHandle
        filePath = path.join(self.fileFolder,fileName)

        if not path.isfile(filePath):
            logger.error("SceneData: File not found %s" % filePath)
            return False

        logger.debug("SceneData: Loading Scene MetaData")

        confParser = configparser.ConfigParser()
        confParser.readfp(open(filePath))

        self.fileUpdated = formatDateTime()

        # Get Variables
        cnfSec = "Scene"
        if confParser.has_section(cnfSec):
            if confParser.has_option(cnfSec,"Title"):   self.fileTitle   = confParser.get(cnfSec,"Title")
            if confParser.has_option(cnfSec,"Created"): self.fileCreated = confParser.get(cnfSec,"Created")
            if confParser.has_option(cnfSec,"Updated"): self.fileUpdated = confParser.get(cnfSec,"Updated")

        self.theText.loadText(self.fileFolder,self.fileHandle,self.fileVersion)
        self.theText.loadSummary(self.fileFolder,self.fileHandle,self.fileVersion)
        self.mainConf.setLastFile(self.fileHandle)

        self.fileLoaded = True
        
        return True

    ##
    #  Save Functions
    ##

    def saveScene(self):

        if self.fileFolder == "":
            logger.error("SceneData: No folder specified")
            return False

        logger.debug("SceneData: Loading Scene MetaData")
        confParser = configparser.ConfigParser()

        # Set Variables
        cnfSec = "Scene"
        confParser.add_section(cnfSec)
        confParser.set(cnfSec,"Title",   str(self.fileTitle))
        confParser.set(cnfSec,"Created", str(self.fileCreated))
        confParser.set(cnfSec,"Updated", str(self.fileUpdated))

        # Write File
        fileName = "%s-metadata.cnf" % self.fileHandle
        filePath = path.join(self.fileFolder,fileName)

        confParser.write(open(filePath,"w"))

        self.theText.saveText(self.fileFolder,self.fileHandle,self.fileVersion)
        self.theText.saveSummary(self.fileFolder,self.fileHandle,self.fileVersion)
        self.mainConf.setLastFile(self.fileHandle)

        return True

    def doAutoSaveText(self):
        self.theText.doAutoSaveText(self.fileFolder,self.fileHandle,self.fileVersion)
        return

    ##
    #  Getters
    ##

    def getText(self):
        return self.theText.getText()

    def getSummary(self):
        return self.theText.getSummary()

    def getSortString(self):
        return "%01d.%02d.%03d" % (self.fileSection,self.fileChapter,self.fileNumber)
    
    ##
    #  Setters
    ##

    def setTitle(self, newTitle):
        newTitle = newTitle.strip()
        if len(newTitle) > 0:
            self.fileTitel = newTitle
        else:
            logger.error("SceneData: Invalid scene title")
        return
        
    def setFolderPath(self, folderPath):
        if not path.isdir(folderPath):
            mkdir(folderPath)
            logger.debug("SceneData: Folder created %s" % folderPath)
        self.fileFolder = folderPath
        return

    def setSection(self, fileSection):
        if fileSection < 0: fileSection = 0
        if fileSection > 3: fileSection = 3
        self.fileSection = fileSection
        if fileSection != 2: self.fileChapter = 0
        return

    def setChapter(self, fileChapter):
        if fileChapter < 1:  fileChapter = 1
        if fileChapter > 99: fileChapter = 99
        if self.fileSection != 2: fileChapter = 0
        self.fileChapter = fileChapter
        return

    def setChapter(self, fileNumber):
        if fileNumber < 1:   fileNumber = 1
        if fileNumber > 999: fileNumber = 999
        self.fileNumber = fileNumber
        return

    def setText(self, srcText):
        self.theText.setText(srcText)
        return

    def setSummary(self, newSummary):
        self.theText.setSummary(newSummary)
        return

    ##
    #  Modifiers
    ##

    def incrementSceneVersion(self):
        self.fileVersion += 1
        self.saveScene()
        return

# End Class SceneData
# ==================================================================================================================== #
# Begin Class TextFile

class TextFile():

    def __init__(self):

        self.text        = ""
        self.summary     = ""
        self.textHash    = ""
        self.hasText     = False
        self.wordsOnLoad = 0
        self.charsOnLoad = 0
        self.wordsAdded  = 0
        self.charsAdded  = 0
        
        return

    ##
    #  Load Functions
    ##

    def loadText(self, fileFolder, fileHandle, fileVersion):

        if not path.isdir(fileFolder): return False

        logger.debug("TextFile: Loading Scene Text")

        fileName = "%s-scene-v%d.txt" % (fileHandle,fileVersion)
        filePath = path.join(fileFolder,fileName)

        if not path.isfile(filePath):
            self.text = "<p>New scene</p>"
            self.saveText()
            self.wordsAdded = 2
            self.charsAdded = 9
        else:
            fileObj   = open(filePath,encoding="utf-8",mode="r")
            self.text = fileObj.read()
            fileObj.close()
            words, chars     = self.wordCount()
            self.wordsOnLoad = words
            self.charsOnLoad = chars

        self.textHash = sha256(str(self.text).encode()).hexdigest()
        self.hasText  = True

        return

    def loadSummary(self, fileFolder, fileHandle, fileVersion):

        if not path.isdir(fileFolder): return False

        logger.debug("TextFile: Loading Scene Summary")

        fileName = "%s-summary-v%d.txt" % (fileHandle,fileVersion)
        filePath = path.join(fileFolder,fileName)

        if path.isfile(filePath):
            fileObj      = open(filePath,encoding="utf-8",mode="r")
            self.summary = fileObj.read()
            fileObj.close()

        return

    ##
    #  Save Functions
    ##

    def saveText(self, fileFolder, fileHandle, fileVersion):

        if not self.hasText: return

        logger.debug("TextFile: Saving Scene Text")

        fileName = "%s-scene-v%d.txt" % (fileHandle,fileVersion)
        filePath = path.join(fileFolder,fileName)
        fileObj  = open(filePath,encoding="utf-8",mode="w")
        fileObj.write(self.text)
        fileObj.close()

        self.textHash = sha256(str(self.text).encode()).hexdigest()

        return

    def doAutoSaveText(self, fileFolder, fileHandle, fileVersion):

        if not self.hasText: return False
        if self.fileHash == sha256(str(self.text).encode()).hexdigest(): return False

        logger.debug("TextFile: AutoSaving")

        self.saveText(fileFolder,fileHandle,fileVersion)

        return True

    def saveSummary(self, fileFolder, fileHandle, fileVersion):

        if not self.hasSummary: return

        logger.debug("TextFile: Saving Scene Summary")

        fileName = "%s-summary-v%d.txt" % (fileHandle,fileVersion)
        filePath = path.join(fileFolder,fileName)
        fileObj  = open(filePath,encoding="utf-8",mode="w")
        fileObj.write(self.text)
        fileObj.close()

        return

    ##
    #  Getters
    ##

    def getText(self):
        return self.text

    def getSummary(self):
        return self.summary

    ##
    #  Setters
    ##

    def setText(self, srcText):
        if len(srcText) > 0:
            words,chars  = wordCount(srcText)
            srcText      = htmlCleanUp(srcText)
            self.text    = srcText
            self.hasText = True
            self.words   = words
            self.chars   = chars
        return

    def setSummary(self, newSummary):
        self.summary = newSummary
        return

    ##
    #  Internal Methods
    ##

    def countWords(self):

        cleanText = self.text
        cleanText = sub("<.*?>"," ",cleanText)
        cleanText = sub("&.*?;","?",cleanText)
        cleanText = cleanText.strip()
        splitText = cleanText.split()

        return len(splitText), len(cleanText)

    def htmlCleanUp(self, srcText):

        okTags   = ["p","b","i","u","strike","ul","ol","li","h2","h3","h4","pre"]
        okAttr   = {"*" : ["style"]}
        okStyles = ["text-align"]

        srcText  = clean(srcText,tags=okTags,attributes=okAttr,styles=okStyles,strip=True)

        if srcText[0:3] != "<p>": srcText = "<p>"+srcText+"</p>"

        srcText  = srcText.replace("<p></p>","")
        srcText  = srcText.replace("</p>","</p>\n")
        srcText  = srcText.replace('style=""',"")
        srcText  = srcText.replace("style=''","")
        srcText  = srcText.replace(" >",">")
        srcText  = srcText.replace("\n ","\n")

        return srcText
    
# End Class TextFile
# ==================================================================================================================== #
# Begin Class Chapters

class Chapters():

    def __init__(self):

        self.chapterList = []
        
        return

    ##
    #  Load Functions
    ##

    def loadChapters(self, fileFolder):
        return
        
# End Class Chapters
# ==================================================================================================================== #
