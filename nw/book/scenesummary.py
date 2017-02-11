# -*- coding: utf-8 -*

##
#  novelWriter – Scene Summary Class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Holds the summary of the loaded scene
##

import logging as logger

from os      import path, rename, remove
from hashlib import sha256
from nw      import *

class SceneSummary():

    def __init__(self, theOpt):

        # Core Objects
        self.mainConf    = CONFIG
        self.theOpt      = theOpt

        # Attributes
        self.summary     = ""
        self.summaryHash = ""
        self.hasSummary  = False

        return

    ##
    # Load and Save
    ##

    def loadSummary(self):

        sceneFolder  = self.theOpt.sceneFolder
        sceneHandle  = self.theOpt.sceneHandle
        sceneVersion = self.theOpt.sceneVersion

        if not path.isdir(sceneFolder):
            logger.debug("SceneSummary.loadSummary: Folder not found %s" % sceneFolder)
            return

        logger.debug("SceneSummary.loadSummary: Loading scene summary")

        fileName  = "%s-summary-%03d.txt" % (sceneHandle,sceneVersion)
        filePath  = path.join(sceneFolder,fileName)

        if not path.isfile(filePath):
            logger.debug("SceneSummary.loadSummary: File not found %s" % filePath)
            return

        fileObj      = open(filePath,encoding="utf-8",mode="r")
        self.summary = fileObj.read()
        fileObj.close()

        self.summaryHash = sha256(str(self.summary).encode()).hexdigest()
        self.hasSummary  = True

        return

    def saveSummary(self):

        if not self.hasSummary:
            logger.debug("SceneSummary.saveSummary: No text to save")
            return False

        if self.summaryHash == sha256(str(self.summary).encode()).hexdigest():
            logger.debug("SceneSummary.saveSummary: No changes to save")
            return False

        sceneFolder  = self.theOpt.sceneFolder
        sceneHandle  = self.theOpt.sceneHandle
        sceneVersion = self.theOpt.sceneVersion

        if not path.isdir(sceneFolder):
            logger.debug("SceneSummary.saveSummary: Folder not found %s" % sceneFolder)
            return False

        if not len(sceneHandle) == 12:
            logger.debug("SceneSummary.saveSummary: Invalid scene handle '%s'" % sceneHandle)
            return False

        if not sceneVersion > 0:
            logger.debug("SceneSummary.saveSummary: Invalid scene version %d" % sceneVersion)
            return False

        logger.debug("SceneSummary.saveSummary: Saving scene text")

        fileName = "%s-summary-%03d.txt" % (sceneHandle,sceneVersion)
        tempName = "%s-summary-%03d.bak" % (sceneHandle,sceneVersion)
        filePath = path.join(sceneFolder,fileName)
        tempPath = path.join(sceneFolder,tempName)

        # Back up old file
        if path.isfile(tempPath): remove(tempPath)
        if path.isfile(filePath): rename(filePath,tempPath)

        fileObj  = open(filePath,encoding="utf-8",mode="w")
        fileObj.write(self.summary)
        fileObj.close()

        self.summaryHash = sha256(str(self.summary).encode()).hexdigest()

        return True

    ##
    #  Setters
    ##

    def setSummary(self, newSummary):
        self.summary    = newSummary.strip()
        self.hasSummary = True
        return

    ##
    #  Getters
    ##

    def getSummary(self):
        return self.summary

# End Class SceneSummary
