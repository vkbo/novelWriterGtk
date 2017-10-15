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
    
    DOC_MAIN  = 0
    DOC_ASIDE = 1
    
    def __init__(self, docPath, itemHandle, itemClass):
        
        self.itemHandle = itemHandle
        self.itemClass  = itemClass
        
        self.docPath    = docPath
        self.docFile    = "%s-%s.nwf" % (self.itemClass,self.itemHandle)
        self.fullPath   = path.join(self.docPath,self.docFile)
        
        self.docTemplate = {
            "text"  : [],
            "stats" : {
                "paragraphs" : 0,
                "words"      : 0,
                "sentences"  : 0
            },
        }
        
        self.docMain  = []
        self.docAside = []
        
        return
    
    def openFile(self):
        
        if not path.isfile(self.fullPath):
            self.docMain.append(self.docTemplate)
            self.docMain[0]["text"] = getLoremIpsum(2)
            return
        
        nwXML = ET.parse(self.fullPath)
        xRoot = nwXML.getroot()
        
        nwxRoot     = xRoot.tag
        appVersion  = xRoot.attrib["appVersion"]
        fileVersion = xRoot.attrib["fileVersion"]

        logger.verbose("XML: Root is %s" % nwxRoot)
        logger.verbose("XML: Version is %s" % fileVersion)
        
        if not nwxRoot == "novelWriterXML" or not fileVersion == "1.0":
            logger.error("BookOpen: Project file does not appear to be a novelWriterXML file version 1.0")
            return
        
        # self.docMain = "\n".join(getLoremIpsum(2))
        # self.docNote = "\n".join(getLoremIpsum(1))
        
        return
    
    def saveFile(self):
        
        nwXML = ET.Element("novelWriterXML",attrib={
            "fileVersion" : "1.0",
            "appVersion"  : str(nw.__version__),
        })
        for docMain in self.docMain:
            xDoc = ET.SubElement(nwXML,"document",attrib={"version":"current"})
            xStats = ET.SubElement(xDoc,"stats",attrib={
                "paragraphs" : str(docMain["stats"]["paragraphs"]),
                "sentences"  : str(docMain["stats"]["sentences"]),
                "words"      : str(docMain["stats"]["words"]),
            })
            xText = ET.SubElement(xDoc,"text")
            parIdx = 0
            for parItem in docMain["text"]:
                xPar = ET.SubElement(xText,"paragraph",attrib={"idx":str(parIdx)})
                xPar.text = ET.CDATA(parItem)
                parIdx += 1
        
        logger.vverbose("Document file path is %s" % self.fullPath)
        
        with open(self.fullPath,"wb") as outFile:
            outFile.write(ET.tostring(
                nwXML,
                pretty_print    = True,
                encoding        = "utf-8",
                xml_declaration = True
            ))
        
        return
    
    def setText(self, toTarget, newText, newCount):
        
        docText = self.docTemplate
        docText["text"]  = newText
        docText["stats"] = {
            "paragraphs" : str(newCount[0]),
            "sentences"  : str(newCount[1]),
            "words"      : str(newCount[2]),
        }
        
        if toTarget == self.DOC_MAIN:
            self.docMain[0] = docText
        elif toTarget == self.DOC_ASIDE:
            self.docMain[0] = docText
        else:
            logger.error("BUG: Unknown document target")
            
        return
    
    def setCount(self, addTarget, parCount, sentCount, wordCount):
        statVals = {
            "paragraphs" : str(parCount),
            "sentences"  : str(sentCount),
            "words"      : str(wordCount),
        }
        if addTarget == self.DOC_MAIN:
            self.docMain[0]["stats"] = statVals
        elif addTarget == self.DOC_ASIDE:
            self.docAside[0]["stats"] = statVals
        else:
            logger.error("BUG: Unknown document target")
        return
    
# End Class DocFile
