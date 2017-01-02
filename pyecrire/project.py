# -*- coding: utf-8 -*
#
#  pyÉcrire – Project Class
#
##

import logging as logger

from os                   import path, mkdir, rename
from pyecrire.functions   import simplifyString, makeHandle
from pyecrire.datawrapper import DataWrapper

class Project():

    def __init__(self, config):

        self.mainConf = config

        # The Book
        self.theBook     = DataWrapper("Book")
        self.bookTitle   = ""
        self.bookName    = ""
        self.bookHandle  = ""
        self.bookFolder  = ""
        self.bookPath    = ""

        # The Universe
        self.theUniverse = DataWrapper("Universe")
        self.univTitle   = ""
        self.univName    = ""
        self.univHandle  = ""
        self.univFolder  = ""
        self.univPath    = ""

        # The File
        self.theFile     = DataWrapper("File")
        self.fileType    = ""
        self.fileCode    = ""
        self.fileTitle   = ""
        self.fileName    = ""
        self.fileHandle  = ""
        self.fileFolder  = ""
        self.filePath    = ""
        self.fileParent  = ""

        # Set Other Defaults
        self.theBook.setTitle("New Book")
        self.theUniverse.setTitle("New Universe")
        self.theFile.setTitle("New File")

        return

    ##
    #  Creators
    ##

    def createBook(self, bookTitle):

        bookName = simplifyString(bookTitle)

        if len(bookTitle) > 0 and len(bookName) > 0:
            self.bookTitle = bookTitle
            self.bookName  = bookName
            if self.bookHandle == "":
                self.bookHandle = makeHandle(bookTitle)
            self.theBook.setTitle(bookTitle)

        logger.debug("Book Title:  %s" % self.bookTitle)
        logger.debug("Book Name:   %s" % self.bookName)
        logger.debug("Book Handle: %s" % self.bookHandle)

        return

    def createUniverse(self, univTitle):

        univName = simplifyString(univTitle)

        if len(univTitle) > 0 and len(univName) > 0:
            self.univTitle = univTitle
            self.univName  = univName
            if self.univHandle == "":
                self.univHandle = makeHandle(univTitle)
            self.theUniverse.setTitle(univTitle)
            self.theBook.setParent(self.univHandle)

        logger.debug("Universe Title:  %s" % self.univTitle)
        logger.debug("Universe Name:   %s" % self.univName)
        logger.debug("Universe Handle: %s" % self.univHandle)

        return

    def createFile(self, fileTitle):

        fileName = simplifyString(fileTitle)

        if len(fileTitle) > 0 and len(fileName) > 0:
            self.fileTitle = fileTitle
            self.fileName  = fileName
            if self.fileHandle == "":
                self.fileHandle = makeHandle(fileTitle)
            self.theFile.setTitle(fileTitle)
            self.theFile.setDataType(self.fileType)

        logger.debug("File Title:  %s" % self.fileTitle)
        logger.debug("File Name:   %s" % self.fileName)
        logger.debug("File Handle: %s" % self.fileHandle)

        return

    ##
    #  Updaters
    ##

    def updateBookFolder(self):

        bookFolder = "B-"+self.bookHandle+"-"+self.bookName

        if bookFolder != self.bookFolder:
            oldPath = path.join(self.mainConf.dataPath,self.bookFolder)
            newPath = path.join(self.mainConf.dataPath,bookFolder)

            if self.bookFolder == "":
                mkdir(newPath)
            else:
                if path.isdir(oldPath):
                    rename(oldPath,newPath)
                else:
                    mkdir(newPath)

            logger.debug("Book path changed from '%s' to '%s'" % (self.bookFolder, bookFolder))

            self.bookFolder = bookFolder
            self.bookPath   = newPath
            self.theBook.setDataPath(newPath)

        return

    def updateUniverseFolder(self):

        univFolder = "U-"+self.univHandle+"-"+self.univName

        if univFolder != self.univFolder:
            oldPath = path.join(self.mainConf.dataPath,self.univFolder)
            newPath = path.join(self.mainConf.dataPath,univFolder)

            if self.univFolder == "":
                mkdir(newPath)
            else:
                if path.isdir(oldPath):
                    rename(oldPath,newPath)
                else:
                    mkdir(newPath)

            logger.debug("Universe path changed from '%s' to '%s'" % (self.univFolder, univFolder))

            self.univFolder = univFolder
            self.univPath   = newPath
            self.theUniverse.setDataPath(newPath)

        return

    def updateFileFolder(self):

        if self.fileTitle == "":
            logger.error("Cannot create file folder before a title and type is set.")
            return

        fileFolder = self.fileCode+"-"+self.fileHandle+"-"+self.fileName
        if   self.fileParent == "Book":
            parentFolder = self.bookPath
        elif self.fileParent == "Universe":
            parentFolder = self.univPath
        else:
            logger.error("File parent type must be Book or Universe.")
            return

        if fileFolder != self.fileFolder:
            oldPath = path.join(parentFolder,self.fileFolder)
            newPath = path.join(parentFolder,fileFolder)

            if self.fileFolder == "":
                mkdir(newPath)
            else:
                if path.isdir(oldPath):
                    rename(oldPath,newPath)
                else:
                    mkdir(newPath)

            logger.debug("File path changed from '%s' to '%s'" % (self.fileFolder, fileFolder))

            self.fileFolder = fileFolder
            self.filePath   = newPath
            self.theFile.setDataPath(newPath)

        return

    ##
    #  Setters
    ##

    def setUniverse(self, univHandle, univPath):

        self.theUniverse.setDataPath(univPath)
        self.theUniverse.loadDetails()

        self.univTitle  = self.theUniverse.title
        self.univName   = simplifyString(self.univTitle)
        self.univHandle = univHandle
        self.univFolder = "U-"+self.univHandle+"-"+self.univName
        self.univPath   = univPath

        self.theBook.parent = univHandle

        return

    def setFileParent(self, parentType):

        if   parentType == "Book":
            self.fileParent     = parentType
            self.theFile.parent = self.bookHandle
        elif parentType == "Universe":
            self.fileParent     = parentType
            self.theFile.parent = self.univHandle
        else:
            logger.error("File parent type must be Book or Universe.")

        return

    def setFileNumber(self, newNumber):
        self.theFile.setNumber(newNumber)
        return

    def setSceneSettings(self, scnTitle, scnSection, scnChapter, scnNumber, scnPOV, scnTime):

        if self.theFile.dataType == "Scene":
            self.fileTitle = scnTitle
            self.fileName  = simplifyString(scnTitle)
            self.theFile.setTitle(scnTitle)
            self.theFile.setSection(scnSection)
            self.theFile.setChapter(int(scnChapter))
            self.theFile.setNumber(int(scnNumber))
            self.theFile.setPOV(scnPOV)

        return

    ##
    #  New, Load and Save
    ##

    def newProject(self, guiObject=None):

        # The Book
        self.theBook     = DataWrapper("Book")
        self.bookTitle   = ""
        self.bookName    = ""
        self.bookHandle  = ""
        self.bookFolder  = ""
        self.bookPath    = ""

        # The Universe
        self.theUniverse = DataWrapper("Universe")
        self.univTitle   = ""
        self.univName    = ""
        self.univHandle  = ""
        self.univFolder  = ""
        self.univPath    = ""

        # The File
        self.newFile("File")

        return

    def newFile(self, fileType):

        # The File
        self.theFile     = DataWrapper(fileType)
        self.fileType    = fileType
        self.fileCode    = fileType[0:1]
        self.fileTitle   = ""
        self.fileName    = ""
        self.fileHandle  = ""
        self.fileFolder  = ""
        self.filePath    = ""

        return

    def loadProject(self, bookPath, bookHandle, univPath, univHandle):

        logger.debug("Loading project")

        self.theBook.setDataPath(bookPath)
        self.theBook.loadDetails()

        self.bookTitle  = self.theBook.title
        self.bookName   = simplifyString(self.bookTitle)
        self.bookHandle = bookHandle
        self.bookFolder = "B-"+self.bookHandle+"-"+self.bookName
        self.bookPath   = bookPath

        self.theUniverse.setDataPath(univPath)
        self.theUniverse.loadDetails()

        self.univTitle  = self.theUniverse.title
        self.univName   = simplifyString(self.univTitle)
        self.univHandle = univHandle
        self.univFolder = "U-"+self.univHandle+"-"+self.univName
        self.univPath   = univPath

        return

    def loadFile(self, filePath, fileHandle):

        logger.debug("Loading file")

        self.theFile.setDataPath(filePath)
        self.theFile.loadDetails()

        self.fileTitle  = self.theFile.title
        self.fileName   = simplifyString(self.fileTitle)
        self.fileHandle = fileHandle
        self.fileFolder = self.fileCode+"-"+self.fileHandle+"-"+self.fileName
        self.filePath   = filePath

        if   self.theFile.dataType == "Scene":
            self.fileParent = "Book"
        elif self.theFile.dataType == "Plot":
            self.fileParent = "Book"
        elif self.theFile.dataType == "Character":
            self.fileParent = "Universe"
        elif self.theFile.dataType == "History":
            self.fileParent = "Universe"
        else:
            self.fileParent = ""

        return

    def saveProject(self):

        # Book
        self.updateBookFolder()
        self.theBook.saveDetails()

        # Universe
        self.updateUniverseFolder()
        self.theUniverse.saveDetails()

        return

    def saveFile(self):

        self.updateFileFolder()
        self.theFile.saveDetails()

        return

# End Class Project