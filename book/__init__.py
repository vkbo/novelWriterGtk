# -*- coding: utf-8 -*

##
#  novelWriter – Data Wrapper Init File
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Data Wrapper initialisation
##

import logging as logger

from book.bookopt      import BookOpt
from book.bookmeta     import BookMeta
from book.scenemeta    import SceneMeta
from book.scenetext    import SceneText
from book.scenesummary import SceneSummary
from book.scenetiming  import SceneTiming

# Constants
IDX_TITLE   = 0
IDX_NUMBER  = 1
IDX_WORDS   = 2
IDX_SECTION = 3
IDX_CHAPTER = 4
IDX_NUMBER  = 5
IDX_COUNT   = 6

# ==================================================================================================================== #
# Begin Class Book

class Book():

    def __init__(self, parConfig):

        # Core Objects
        self.mainConf = parConfig
        self.theOpt   = BookOpt(self.mainConf)
        self.theMeta  = BookMeta(self.theOpt)
        self.theScene = Scene(self.theOpt)

        # Attributes
        self.bookLoaded = False

        # Connect to Setters
        self.setBookTitle  = self.theMeta.setTitle
        self.setBookAuthor = self.theMeta.setAuthor

        # Connect to Getters
        self.getBookTitle  = self.theMeta.getTitle
        self.getBookAuthor = self.theMeta.getAuthor
        
        return

    def loadBook(self, bookFolder):

        # Reset Core Objects
        self.theOpt   = BookOpt(self.mainConf)
        self.theMeta  = BookMeta(self.theOpt)
        self.theScene = Scene(self.theOpt)

        # Load Book
        self.theOpt.setBookFolder(bookFolder)
        if self.theOpt.bookFolder is None: return

        self.theMeta.loadData()
        self.bookLoaded = self.theMeta.bookLoaded
        
        return

# End Class Book
# ==================================================================================================================== #
# Begin Class Scene

class Scene():

    def __init__(self, theOpt):

        self.theOpt     = theOpt
        self.theMeta    = SceneMeta(theOpt)
        self.theText    = SceneText(theOpt)
        self.theSummary = SceneSummary(theOpt)
        self.theTiming  = SceneTiming(theOpt)

        return

# End Class Scene
# ==================================================================================================================== #
