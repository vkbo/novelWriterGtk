# -*- coding: utf-8 -*

import logging as logger

from os import path, listdir

class DataList():

    def __init__(self, dataPath, listType):

        self.dataPath = dataPath

        return


    def updateList(self):

        if path.isdir(self.dataPath):
            dirContent = listdir(self.dataPath)

            for listItem in dirContent:
                print(listItem)

        return


# End Class DataList
