# -*- coding: utf-8 -*

##
#  novelWriter – Scene Timing Class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Holds the timing of the loaded scene
##

import logging as logger

from os import path, remove
from nw import *

class SceneTiming():

    def __init__(self, theOpt, theText):

        # Core Objects
        self.mainConf = CONFIG
        self.theOpt   = theOpt
        self.theText  = theText

        # Runtime Attributes
        self.timeCurrent = 0.0
        self.timeTotal   = 0.0
        self.timeList    = []

        return

    ##
    #  Load and Save
    ##

    def loadTiming(self):

        sceneFolder = self.theOpt.sceneFolder
        sceneHandle = self.theOpt.sceneHandle

        if not path.isdir(sceneFolder):
            logger.debug("SceneTiming.loadTiming: Folder not found %s" % sceneFolder)
            return

        if not len(sceneHandle) == 12:
            logger.debug("SceneTiming.loadTiming: Invalid scene handle '%s'" % sceneHandle)
            return

        tempName = "%s-timing.tmp" % sceneHandle
        tempPath = path.join(sceneFolder,tempName)

        fileName = "%s-timing.csv" % sceneHandle
        filePath = path.join(sceneFolder,fileName)

        if path.isfile(tempPath):
            logger.debug("SceneTiming.loadTiming: Appending autosaved timing")

            fileObj = open(tempPath,"r")
            tmpPrev = fileObj.read()
            fileObj.close()

            fileObj = open(filePath,"a+")
            fileObj.write(tmpPrev)
            fileObj.close()

            remove(tempPath)

        if not path.isfile(filePath): return

        logger.debug("SceneTiming.loadTiming: Loading timing information")

        fileObj = open(filePath,"r")
        tmpData = fileObj.read()
        fileObj.close()

        self.timeList    = []
        self.timeTotal   = 0.0
        self.timeCurrent = 0.0
        tmpLines = tmpData.split("\n")
        for tmpLine in tmpLines:
            tmpValues = tmpLine.split(",")
            if len(tmpValues) == 4:
                self.timeList.append(tmpValues)
                self.timeTotal += float(tmpValues[1])

        return

    def saveTiming(self, autoSave=False):

        if self.timeCurrent < self.mainConf.minTime: return

        sceneFolder = self.theOpt.sceneFolder
        sceneHandle = self.theOpt.sceneHandle

        if not path.isdir(sceneFolder):
            logger.debug("SceneTiming.saveTiming: Folder not found %s" % sceneFolder)
            return

        if not len(sceneHandle) == 12:
            logger.debug("SceneTiming.saveTiming: Invalid scene handle '%s'" % sceneHandle)
            return

        tempName = "%s-timing.tmp" % sceneHandle
        tempPath = path.join(sceneFolder,tempName)

        fileName = "%s-timing.csv" % sceneHandle
        filePath = path.join(sceneFolder,fileName)

        if autoSave:
            logger.debug("SceneTiming.saveTiming: Autosaving timing information")
            fileMode = "w+"
            savePath = tempPath
        else:
            logger.debug("SceneTiming.saveTiming: Saving timing information")
            self.timeTotal += self.timeCurrent
            fileMode = "a+"
            savePath = filePath

        timeStamp = formatDateTime()
        timeValue = str(self.timeCurrent)
        wordCount = str(self.theText.wordsLatest)
        charCount = str(self.theText.charsLatest)

        self.timeList.append([timeStamp,timeValue,wordCount,charCount])

        # Write File
        timeSet = timeStamp+","+timeValue+","+wordCount+","+charCount+"\n"
        fileObj = open(savePath,fileMode)
        fileObj.write(timeSet)
        fileObj.close()

        if path.isfile(tempPath) and not autoSave:
            logger.debug("SceneTiming.saveTiming: Deleting temp timing")
            remove(tempPath)

        return

    ##
    #  Setters
    ##

    def setTime(self, timeValue):
        self.timeCurrent = timeValue
        return

    ##
    #  Getters
    ##

    def getTimeTotal(self):
        return self.timeTotal

    def getTimeList(self):
        return self.timeList

# End Class SceneTiming
