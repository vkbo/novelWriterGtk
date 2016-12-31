# -*- coding: utf-8 -*

import logging as logger

from os import path, listdir

class DataList():

    def __init__(self, dataPath, listType):

        self.listType = listType
        self.listCode = listType[0:1].upper()
        self.dataPath = dataPath
        self.dataList = {}
        self.dataLen  = 0

        return


    def makeList(self):

        self.dataList = {}

        if path.isdir(self.dataPath):
            dirContent = listdir(self.dataPath)

            for listItem in dirContent:
                itemPath = path.join(self.dataPath,listItem)
                if path.isdir(itemPath):
                    itemType   = listItem[0:1]
                    itemHandle = listItem[2:12]

                    if itemType == self.listCode:
                        self.dataList[itemHandle] = itemPath

            self.dataLen = len(self.dataList)
        else:
            logger.error("Path not found: %s" % self.dataPath)

        return


    def getItem(self, itemHandle):
        return self.dataList[itemHandle]


    def setDataPath(self, newPath):
        if path.isdir(newPath):
            self.dataPath = newPath
        return


# End Class DataList
