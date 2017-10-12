# -*- coding: utf-8 -*
"""novelWriter Document File

 novelWriter – Document File
=============================
 Manages a single document

 File History:
 Created: 2017-10-06 [0.4.0]

"""

import logging
import nw

from nw.content import getLoremIpsum

logger = logging.getLogger(__name__)

class DocFile():
    
    def __init__(self, docPath, docSlug):
        
        self.docPath = docPath
        self.docSlug = docSlug
        
        self.docText = None
        self.docNote = None
        
        return
    
    def openFile(self):
        
        self.docText = "\n".join(getLoremIpsum(5))
        self.docNote = "\n".join(getLoremIpsum(2))
        
        return

# End Class DocFile
