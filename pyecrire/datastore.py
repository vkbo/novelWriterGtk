# -*- coding: utf-8 -*

import logging as logger
import configparser

class DataWrapper():

    def __init__(self,config,docType):

        self.mainConf  = config
        self.docType   = docType
        self.docTitle  = ""
        self.docName   = ""
        self.docHandle = ""

        return


class Universe(DataWrapper):

    def __init__(self,config):

        return


class Book(DataWrapper):

    def __init__(self,config):

        return


class Character(DataWrapper):

    def __init__(self,config):

        return

