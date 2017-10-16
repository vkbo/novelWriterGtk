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
        
        self.docMain    = {}
        self.docAside   = {}
        
        return
    
    def openFile(self):
        
        if not path.isfile(self.fullPath):
            logger.debug("File not found %s" % self.fullPath)
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
        
        for xChild in xRoot:
            if xChild.tag in ("document","note"):
                docVersion = xChild.attrib["version"]
                logger.debug("DocOpen: Found %s version %s" % (xChild.tag,docVersion))
                newDoc = {
                    "text"  : [],
                    "stats" : {
                        "paragraphs" : 0,
                        "words"      : 0,
                        "sentences"  : 0
                    },
                }
                for xItem in xChild:
                    if xItem.tag == "stats":
                        newDoc["stats"]["paragraphs"] = int(xItem.attrib["paragraphs"])
                        newDoc["stats"]["sentences"]  = int(xItem.attrib["sentences"])
                        newDoc["stats"]["words"]      = int(xItem.attrib["words"])
                    elif xItem.tag == "text":
                        for xPar in xItem:
                            newDoc["text"].append(xPar.text)
                if xChild.tag == "document":
                    self.docMain[docVersion] = newDoc
                else:
                    self.docAside[docVersion] = newDoc
        
        return
    
    def saveFile(self):
        
        nwXML = ET.Element("novelWriterXML",attrib={
            "fileVersion" : "1.0",
            "appVersion"  : str(nw.__version__),
        })
        
        for docVersion in self.docMain.keys():
            docMain = self.docMain[docVersion]
            xDoc = ET.SubElement(nwXML,"document",attrib={"version":docVersion})
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
        
        for docVersion in self.docAside.keys():
            docAside = self.docAside[docVersion]
            xNote = ET.SubElement(nwXML,"note",attrib={"version":docVersion})
            xStats = ET.SubElement(xNote,"stats",attrib={
                "paragraphs" : str(docAside["stats"]["paragraphs"]),
                "sentences"  : str(docAside["stats"]["sentences"]),
                "words"      : str(docAside["stats"]["words"]),
            })
            xText = ET.SubElement(xNote,"text")
            parIdx = 0
            for parItem in docAside["text"]:
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
        
        docText = {
            "text"  : newText,
            "stats" : {
                "paragraphs" : str(newCount[0]),
                "sentences"  : str(newCount[1]),
                "words"      : str(newCount[2]),
            }
        }
        
        if toTarget == self.DOC_MAIN:
            self.docMain["current"] = docText
        elif toTarget == self.DOC_ASIDE:
            self.docAside["current"] = docText
        else:
            logger.error("BUG: Unknown document target")
            
        return
    
    # def setCount(self, toTarget, parCount, sentCount, wordCount):
    #     statVals = {
    #         "paragraphs" : str(parCount),
    #         "sentences"  : str(sentCount),
    #         "words"      : str(wordCount),
    #     }
    #     if toTarget == self.DOC_MAIN:
    #         self.docMain["current"]["stats"] = statVals
    #     elif toTarget == self.DOC_ASIDE:
    #         self.docAside["current"]["stats"] = statVals
    #     else:
    #         logger.error("BUG: Unknown document target")
    #     return
    
# End Class DocFile
