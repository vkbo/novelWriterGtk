# -*- coding: utf-8 -*
"""novelWriter File Init

 novelWriter – File Init File
==============================
 initialisation of the file storage

 File History:
 Created: 2017-10-06 [0.4.0]

"""

import logging
import nw
import nw.const as NWC

from os             import path
from time           import time
from hashlib        import sha256
from nw.file.doc    import DocFile
from nw.file.bkmeta import BookMeta

logger = logging.getLogger(__name__)

class DataStore():
    
    def __init__(self):
        
        self.bookLoaded = False
        
        self.bookPath   = None
        self.theMeta    = BookMeta()
        self.theTree    = []
        
        
        return
    
    def openBook(self, bookPath):
        
        if path.isdir(bookPath):
            self.bookPath = bookPath
            self.theMeta.loadMeta(bookPath)
            self.bookLoaded = True
        else:
            logger.error("Path not found: %s" % bookPath)
            
        return
    
    def createBook(self):
        
        self.appendTree(0,0,NWC.TreeNodes.BOOK, "Book",      self.makeHandle())
        self.appendTree(0,0,NWC.TreeNodes.CHARS,"Characters",self.makeHandle())
        self.appendTree(0,0,NWC.TreeNodes.PLOTS,"Plots",     self.makeHandle())
        self.appendTree(0,0,NWC.TreeNodes.NOTES,"Notes",     self.makeHandle())
        
        
    
    def createDoc(self, docTitle, docType):
        
        nodeHandle = sha256(str(time()).encode()).hexdigest()[0:20]
        
        self.theTree[docHandle] = DocFile(self.nodeHandle)
        
        return True
    
    def appendTree(self,tClass,tLevel,tType,tName,tHandle):
        self.theTree.append({
            "Class"  : tClass,
            "Level"  : tLevel,
            "Type"   : tType,
            "Name"   : tName,
            "Handle" : tHandle
        })
        return True
    
    def makeHandle(self):
        return sha256(str(time()).encode()).hexdigest()[0:20]
    
# End Class DataStore
