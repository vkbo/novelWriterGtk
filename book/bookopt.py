# -*- coding: utf-8 -*

##
#  novelWriter – Book Options Class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Holds the data options of the loaded book
##

import logging as logger

from os import path

class BookOpt():

    def __init__(self, parConfig):

        self.mainConf    = parConfig
        self.bookFolder  = None
        self.sceneFolder = None
        
        return

    ##
    #  Setters
    ##

    def setBookFolder(self, bookFolder):
        if path.isdir(bookFolder):
            self.bookFolder = bookFolder
        else:
            logger.debug("BookOpt.setBookFolder: Folder not found %s" % bookFolder)
        return

# End Class BookOpt
