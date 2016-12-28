# -*- coding: utf-8 -*

import logging as logger

from os import path, listdir

class DataList():

    def __init__(self, dataPath, listType):

        self.dataPath = dataPath
        self.dataList = {}

        return


    def makeList(self):

        if path.isdir(self.dataPath):
            dirContent = listdir(self.dataPath)

            for listItem in dirContent:
                itemPath = path.join(self.dataPath,listItem)
                if path.isdir(itemPath):
                    itemType   = listItem[0:1]
                    itemHandle = listItem[2:12]
                    print(itemType+" "+itemHandle)
        else:
            logger.error("Path not found: %s" % self.dataPath)

        return


# End Class DataList
