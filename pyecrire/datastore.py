# -*- coding: utf-8 -*

import logging as logger
import configparser

class Universe():

    def __init__(self, config):

        self.mainConf   = config
        self.univName   = ""
        self.univHandle = ""

    def setName(name):

        self.univName = name




class Project():

    def __init__(self, config, universe):

        self.mainConf   = config
        self.objUniv    = universe
        self.projName   = ""
        self.projHandle = ""




class Character():

    def __init__(self, config, universe):

        self.mainConf   = config
        self.objUniv    = universe
        self.charName   = ""
        self.charHandle = ""
