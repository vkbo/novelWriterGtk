# -*- coding: utf-8 -*

##
#  novelWriter – Scene Timing Class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Holds the timing of the loaded scene
##

import logging as logger

class SceneTiming():

    def __init__(self, theOpt):

        # Inherited Data
        self.theOpt      = theOpt
        self.mainConf    = theOpt.mainConf

        return

# End Class SceneTiming
