# -*- coding: utf-8 -*
"""novelWriter Scene Options Class

novelWriter – Scene Options Class
====================================
Holds the data options of the loaded scene

File History:
Created: 2017-01-18 [0.3.0]

"""

import logging as logger
import nw

from os import path

class SceneOpt():

    def __init__(self):

        self.sceneHandle  = ""
        self.sceneFolder  = ""
        self.sceneVersion = 1

        return

    ##
    #  Setters
    ##

    def setSceneHandle(self, sceneHandle):
        if len(sceneHandle) == 20:
            self.sceneHandle = sceneHandle
        else:
            logger.debug("SceneOpt.setSceneHandle: Invalid handle %s" % sceneHandle)
        return

    def setSceneFolder(self, sceneFolder):
        if path.isdir(sceneFolder):
            self.sceneFolder = sceneFolder
        else:
            logger.debug("SceneOpt.setSceneFolder: Path not found %s" % sceneFolder)
        return

    def setSceneVersion(self, sceneVersion):
        if sceneVersion > 0:
            self.sceneVersion = sceneVersion
        else:
            logger.debug("SceneOpt.setSceneVersion: Invalid scene version %d" % sceneVersion)
        return

    ##
    #  Getters
    ##

    def getSceneHandle(self):
        return self.sceneHandle

    def getSceneFolder(self):
        return self.sceneFolder

    def getSceneVersion(self):
        return self.sceneVersion

# End Class SceneOpt
