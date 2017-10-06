# -*- coding: utf-8 -*
"""novelWriter Book Meta Data

 novelWriter – Book Meta Data
==============================
 Loads the book meta data

 File History:
 Created: 2017-10-06 [0.4.0]

"""

import logging

from os import path

logger = logging.getLogger(__name__)

class BookMeta():
    
    def __init__(self):
        
        self.bookPath = None
        
        return
    
    def loadMeta(self, bookPath):
        
        return True

# End Class BookMeta
