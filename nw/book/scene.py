# -*- coding: utf-8 -*

##
#  novelWriter – Scene Class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Holds the scene of the loaded book
##

import logging as logger

from os                   import listdir
from time                 import time
from hashlib              import sha256
from nw                   import *
from nw.book.scenemeta    import SceneMeta
from nw.book.scenetext    import SceneText
from nw.book.scenesummary import SceneSummary
from nw.book.scenetiming  import SceneTiming

class Scene():

    def __init__(self, theOpt, bookMeta):

        # Core Objects
        self.mainConf    = CONFIG
        self.bookMeta    = bookMeta
        self.theOpt      = theOpt
        self.theMeta     = SceneMeta(theOpt)
        self.theText     = SceneText(theOpt)
        self.theSummary  = SceneSummary(theOpt)
        self.theTiming   = SceneTiming(theOpt,self.theText)

        # Runtime Attributes
        self.sceneLoaded = False

        return

    def clearContent(self):

        logger.debug("Scene.clearContent: Clearing content")

        # Clear Objects
        self.theMeta.clearContent()
        self.theText.clearContent()
        self.theSummary.clearContent()
        self.theTiming.clearContent()

        # Clear Runtime Attributes
        self.sceneLoaded = False

        return

    ##
    #  Create, Load and Save
    ##

    def createScene(self, sceneTitle, sceneNumber):

        """
        Description:
            Sets title and number.
            Sets default text to "New Scene"
            Saves the scene
        """

        logger.debug("Scene.createScene: Creating new scene")

        self.clearContent()

        sceneHandle = sha256(str(time()).encode()).hexdigest()[0:12]
        self.theOpt.setSceneHandle(sceneHandle)

        self.theMeta.setTitle(sceneTitle)
        self.theMeta.setNumber(sceneNumber)
        self.theText.setText("New Scene")
        self.saveScene()
        self.makeIndex()
        self.sceneLoaded = True

        return

    def loadScene(self, sceneHandle):

        """
        Description:
            Verifies scene handle
            Checks if we're actually loading a new file
            If we are, save the current buffer including timing information
            Set new scene handle and clear all scene content
            Triggers load in all submodules
        """

        if not self.theOpt.isValidHandle(sceneHandle):
            logger.debug("Scene.loadScene: Invalid scene handle '%s'" % sceneHandle)
            return

        currHandle = self.theOpt.getSceneHandle()
        logger.debug("Scene.loadScene: Switching from handle '%s' to '%s'" % (currHandle,sceneHandle))

        if currHandle == sceneHandle:
            logger.debug("Scene.loadScene: Nothing to load")
            return

        # Close Old Scene
        self.closeScene()

        # Load New Scene
        self.theOpt.setSceneHandle(sceneHandle)
        self.clearContent()

        self.theMeta.loadData()
        self.theText.loadText()
        self.theSummary.loadSummary()
        self.theTiming.loadTiming()

        return

    def closeScene(self):

        """
        Description:
            If the scene handle is valid, save scene buffer and timing information
        """
        
        if self.theOpt.isValidHandle(self.theOpt.getSceneHandle()):
            self.saveScene()
            self.theTiming.saveTiming()
            self.clearContent()

        return

    def saveScene(self):

        """
        Description:
            Updates metadata.
            Triggers save in all submodules, except timing which is only saved on exit or close
        """

        self.theMeta.setUpdated(formatDateTime())
        self.theMeta.setWords(self.theText.wordsLatest)
        self.theMeta.setChars(self.theText.charsLatest)

        self.theMeta.saveData()
        self.theText.saveText()
        self.theSummary.saveSummary()

        return

    ##
    #  Methods
    ##

    def makeIndex(self):

        sceneIndex  = {}
        sceneFolder = self.theOpt.sceneFolder

        if sceneFolder is None:
            logger.debug("Scene.makeIndex: Path not found %s" % sceneFolder)
            return

        logger.debug("Scene.makeIndex: Scanning folder %s" % sceneFolder)
            
        dirContent = listdir(sceneFolder)

        # Scene Book Folder
        for listItem in dirContent:
            itemPath = path.join(sceneFolder,listItem)
            if path.isfile(itemPath):
                if len(listItem) == 25 and listItem[-12:] == "metadata.cnf":
                    itemHandle = listItem[:12]
                    tmpScene = SceneMeta(self.theOpt)
                    tmpScene.loadData(itemHandle)
                    sceneIndex[itemHandle] = [
                        tmpScene.sceneTitle,
                        tmpScene.sceneNumber,
                        tmpScene.sceneWords,
                        tmpScene.sceneSection,
                        tmpScene.sceneChapter,
                        0
                    ]

        # Count File Versions
        for listItem in dirContent:
            itemPath = path.join(sceneFolder,listItem)
            if path.isfile(itemPath):
                if len(listItem) > 18 and listItem[12:19] == "-scene-" and listItem[-3:] == "txt":
                    itemHandle = listItem[:12]
                    sceneIndex[itemHandle][SCIDX_COUNT] += 1

        self.theOpt.setSceneIndex(sceneIndex)

        return

# End Class Scene
