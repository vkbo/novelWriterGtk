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
import lxml.etree as ET

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
        
        self.docText = "\n".join(getLoremIpsum(2))
        self.docNote = "\n".join(getLoremIpsum(1))
        
        return
    
    def saveFile(self):
        
        self.docFile  = "%s-%s.nwf" % (self.itemClass,self.itemHandle)
        self.fullPath = path.join(self.docPath,self.docFile)
        
        nwXML = ET.Element("novelWriterXML",attrib={
            "fileVersion" : "1.0",
            "appVersion"  : str(nw.__version__),
        })
        xDoc = ET.SubElement(nwXML,"document")
        xDoc.text = self.docText[31:]
        
        # nwDoc = ET.fromstring(self.docText[31:])
        print(ET.tostring(nwXML,pretty_print=True))
        
        logger.vverbose("Document file path is %s" % self.fullPath)
    
    def setText(self, newText):
        
        self.docText = newText
        print(newText[31:])
        self.saveFile()
        
        return

# End Class DocFile
