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

    def __init__(self, theOpt):

        # Core Objects
        self.mainConf    = CONFIG
        self.theOpt      = theOpt
        self.theMeta     = SceneMeta(theOpt)
        self.theText     = SceneText(theOpt)
        self.theSummary  = SceneSummary(theOpt)
        self.theTiming   = SceneTiming(theOpt)

        # Runtime Attributes
        self.sceneLoaded = False

        return

    def clearContent(self):

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
            Verifies scene handle.
            Triggers load in all submodules.
        """

        self.theOpt.setSceneHandle(sceneHandle)
        if not len(self.theOpt.sceneHandle) == 12:
            logger.debug("Scene.loadScene: Invalid scene handle '%s'" % sceneHandle)
            return

        self.theMeta.loadData()
        self.theText.loadText()
        self.theSummary.loadSummary()

        return

    def saveScene(self):

        """
        Description:
            Updates metadata.
            Triggers save in all submodules.
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
                        tmpScene.sceneNumber,
                        0
                    ]

        # Count File Versions
        for listItem in dirContent:
            itemPath = path.join(sceneFolder,listItem)
            if path.isfile(itemPath):
                if len(listItem) > 18 and listItem[12:19] == "-scene-":
                    itemHandle = listItem[:12]
                    sceneIndex[itemHandle][SCIDX_COUNT] += 1

        print(sceneIndex)

        self.theOpt.setSceneIndex(sceneIndex)

        return

# End Class Scene
