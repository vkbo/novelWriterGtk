# -*- coding: utf-8 -*

##
#  novelWriter – Scene Timing Class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Holds the timing of the loaded scene
##

import logging as logger

from nw import *

class SceneTiming():

    def __init__(self, theOpt, theText):

        # Core Objects
        self.mainConf = CONFIG
        self.theOpt   = theOpt
        self.theText  = theText

        # Runtime Attributes
        self.timeTotal   = 0.0
        self.timeList    = []

        return

    def clearContent(self):

        # Clear Runtime Attributes
        self.timeTotal   = 0.0
        self.timeList    = []

        return

    ##
    #  Load and Save
    ##

    def loadTiming(self):

        sceneFolder  = self.theOpt.sceneFolder
        sceneHandle  = self.theOpt.sceneHandle

        if not path.isdir(sceneFolder):
            logger.debug("SceneTiming.loadTiming: Folder not found %s" % sceneFolder)
            return

        if not len(sceneHandle) == 12:
            logger.debug("SceneTiming.loadTiming: Invalid scene handle '%s'" % sceneHandle)
            return

        fileName = "%s-timing.csv" % sceneHandle
        filePath = path.join(sceneFolder,fileName)

        if not path.isfile(filePath): return

        logger.debug("SceneTiming.loadTiming: Loading timing information")

        fileObj = open(filePath,"r")
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

    def saveTiming(self, timeValue, theText):

        sceneFolder  = self.theOpt.sceneFolder
        sceneHandle  = self.theOpt.sceneHandle

        if not path.isdir(sceneFolder):
            logger.debug("SceneTiming.saveTiming: Folder not found %s" % sceneFolder)
            return

        if not len(sceneHandle) == 12:
            logger.debug("SceneTiming.saveTiming: Invalid scene handle '%s'" % sceneHandle)
            return

        fileName = "%s-timing.csv" % sceneHandle
        filePath = path.join(sceneFolder,fileName)

        logger.debug("SceneTiming.saveTiming: Saving timing information")

        self.timeTotal += timeValue

        timeStamp = formatDateTime()
        timeValue = str(timeValue)
        wordCount = str(self.theText.wordsLatest)
        charCount = str(self.theText.charsLatest)

        self.timeList.append([timeStamp,timeValue,wordCount,charCount])

        # Write File
        timeSet  = timeStamp+","+timeValue+","+wordCount+","+charCount+"\n"
        fileObj  = open(filePath,"a+")
        fileObj.write(timeSet)
        fileObj.close()

        return

    ##
    #  Getters
    ##

    def getTimeTotal(self):
        return self.timeTotal

    def getTimeList(self):
        return self.timeList

# End Class SceneTiming
