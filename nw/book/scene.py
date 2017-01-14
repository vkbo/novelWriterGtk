# -*- coding: utf-8 -*

##
#  novelWriter – Scene Class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Holds the scene of the loaded book
##

import logging as logger

from os                   import listdir
from hashlib              import sha256
from nw                   import *
from nw.book.scenemeta    import SceneMeta
from nw.book.scenetext    import SceneText
from nw.book.scenesummary import SceneSummary
from nw.book.scenetiming  import SceneTiming

class Scene():

    def __init__(self, theOpt):

        # Core Objects
        self.mainConf   = CONFIG
        self.theOpt     = theOpt
        self.theMeta    = SceneMeta(theOpt)
        self.theText    = SceneText(theOpt)
        self.theSummary = SceneSummary(theOpt)
        self.theTiming  = SceneTiming(theOpt)

        return

    def clearContent(self):

        # Clear Objects
        self.theMeta.clearContent()
        self.theText.clearContent()
        self.theSummary.clearContent()
        self.theTiming.clearContent()

        return

    ##
    #  Create, Load and Save
    ##

    def createScene(self, sceneTitle, sceneNumber):

        logger.debug("Scene.createScene: Creating new scene")

        sceneHandle = sha256(str(time()).encode()).hexdigest()[0:12]
        self.theOpt.setSceneHandle(sceneHandle)


        #self.theScene = SceneData()
        self.theMeta.setTitle(sceneTitle)
        self.theMeta.setNumber(sceneNumber)
        #self.theScene.setText("New Scene")
        #self.theScene.saveScene()

        return

    ##
    #  Methods
    ##

    def makeIndex(self):

        sceneIndex  = {}
        sceneFolder = self.theOpt.sceneFolder

        if sceneFolder is None:
            logger.debug("BookOpt.makeIndex: Path not found %s" % sceneFolder)
            return

        logger.debug("BookOpt.makeIndex: Scanning folder %s" % sceneFolder)
            
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
                if len(listItem) > 15 and listItem[-3:] == "txt":
                    itemHandle = listItem[:12]
                    sceneIndex[itemHandle][SCIDX_COUNT] += 1

        self.theOpt.setSceneIndex(sceneIndex)

        return

# End Class Scene
