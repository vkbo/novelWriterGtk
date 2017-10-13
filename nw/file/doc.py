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

from os           import path
from nw.content   import getLoremIpsum
from nw.file.item import BookItem

logger = logging.getLogger(__name__)

class DocFile():
    
    def __init__(self, docPath, itemHandle, itemClass):
        
        self.itemHandle = itemHandle
        self.itemClass  = itemClass
        
        self.docPath    = docPath
        self.docFile    = None
        
        self.docText    = None
        self.docNote    = None
        
        return
    
    def openFile(self):
        
        self.docText = "\n".join(getLoremIpsum(5))
        self.docNote = "\n".join(getLoremIpsum(2))
        
        return
    
    def saveFile(self):
        
        self.docFile  = "%s-%s.nwf" % (self.itemClass,self.itemHandle)
        self.fullPath = path.join(self.docPath,self.docFile)
        
        logger.vverbose("Document file path is %s" % self.fullPath)
    
    def setText(self, newText):
        
        print(newText)
        
        return

# End Class DocFile
