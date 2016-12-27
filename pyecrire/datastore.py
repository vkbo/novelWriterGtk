# -*- coding: utf-8 -*

import logging as logger
import configparser

class DataWrapper():

    def __init__(self, dataType):

        self.dataType     = dataType
        self.dataPath     = ""
        self.fileTitle    = ""
        self.dateOriginal = 0
        self.dateFile     = 0
        self.fileNotes    = ""
        self.fileText     = ""

        return


class Universe(DataWrapper):

    def __init__(self):

        DataWrapper.__init__(self,"Universe")

        return


class Book(DataWrapper):

    def __init__(self):

        return


class Character(DataWrapper):

    def __init__(self):

        return

