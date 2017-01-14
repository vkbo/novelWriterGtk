# -*- coding: utf-8 -*

##
#  novelWriter – Scene Meta Class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Holds the metadata of the loaded scene
##

import logging as logger

class SceneMeta():

    def __init__(self, theOpt):

        # Inherited Data
        self.theOpt      = theOpt
        self.mainConf    = theOpt.mainConf

        return

# End Class SceneMeta
