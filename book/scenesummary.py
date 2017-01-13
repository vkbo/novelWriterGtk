# -*- coding: utf-8 -*

##
#  novelWriter – Scene Summary Class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Holds the summary of the loaded scene
##

import logging as logger

class SceneSummary():

    def __init__(self, theOpt):

        # Inherited Data
        self.theOpt      = theOpt
        self.mainConf    = theOpt.mainConf

        return

# End Class SceneSummary
