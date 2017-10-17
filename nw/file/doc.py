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
from nw.functions import getTimeStamp

logger = logging.getLogger(__name__)

class DocFile():
    
    VAL_TEXT   = "text"
    VAL_NOTE   = "note"
    VAL_TIME   = "timestamp"
    VAL_COUNT  = "counts"
    
    CNT_PAR    = "parcount"
    CNT_SENT   = "sencount"
    CNT_WORD   = "wordcount"
    CNT_CHAR   = "charcount"
    
    validEntry = [VAL_TEXT,VAL_NOTE,VAL_TIME,VAL_COUNT]
    validCount = [CNT_PAR,CNT_SENT,CNT_WORD,CNT_CHAR]
    
    def __init__(self, docPath, itemHandle, itemClass):
        
        self.itemHandle = itemHandle
        self.itemClass  = itemClass
        
        self.docPath    = docPath
        self.docFile    = "%s-%s.nwf" % (self.itemClass,self.itemHandle)
        self.fullPath   = path.join(self.docPath,self.docFile)
        
        self.docText = {
            self.VAL_TEXT  : [],
            self.VAL_NOTE  : [],
            self.VAL_TIME  : None,
            self.VAL_COUNT : {
                self.CNT_PAR  : None,
                self.CNT_SENT : None,
                self.CNT_WORD : None,
                self.CNT_CHAR : None,
            }
        }
        
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
            if xChild.tag == "document":
                if self.VAL_TIME in xChild.attrib.keys():
                    self.docText[self.VAL_TIME] = xChild.attrib[self.VAL_TIME]
                for xItem in xChild:
                    if xItem.tag == self.VAL_COUNT:
                        for attribKey in xItem.attrib.keys():
                            if not attribKey in self.validCount: continue
                            self.docText[self.VAL_COUNT][attribKey] = int(xItem.attrib[attribKey])
                    elif xItem.tag == self.VAL_TEXT:
                        for xPar in xItem:
                            self.docText[self.VAL_TEXT].append(xPar.text)
                    elif xItem.tag == self.VAL_NOTE:
                        for xPar in xItem:
                            self.docText[self.VAL_NOTE].append(xPar.text)
                    else:
                        logger.error("DocOpen: Unknown tag '%s' in XML" % xItem.tag)
                logger.debug("DocOpen: Opened document %s last saved on %s" %(
                    self.itemHandle, self.docText[self.VAL_TIME]
                ))
        
        return
    
    def saveFile(self):
        
        nwXML = ET.Element("novelWriterXML",attrib={
            "fileVersion" : "1.0",
            "appVersion"  : str(nw.__version__),
        })
        
        xDoc = ET.SubElement(nwXML,"document",attrib={self.VAL_TIME:getTimeStamp("-")})
        countVals = {}
        for countType in self.docText[self.VAL_COUNT].keys():
            countVal = self.docText[self.VAL_COUNT][countType]
            if not countVal is None:
                countVals[countType] = str(countVal)
        xCounts = ET.SubElement(xDoc,self.VAL_COUNT,attrib=countVals)
        
        parIdx = 0
        xText  = ET.SubElement(xDoc,self.VAL_TEXT)
        for parItem in self.docText[self.VAL_TEXT]:
            xPar = ET.SubElement(xText,"paragraph",attrib={"idx":str(parIdx)})
            xPar.text = ET.CDATA(parItem)
            parIdx += 1
        
        parIdx = 0
        if len(self.docText[self.VAL_NOTE]) > 0:
            xNote = ET.SubElement(xDoc,self.VAL_NOTE)
            for parItem in self.docText[self.VAL_NOTE]:
                xPar = ET.SubElement(xNote,"paragraph",attrib={"idx":str(parIdx)})
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
    
    def setText(self, newText, newCount, newNote=[]):
        
        for n in range(4):
            if len(newCount) > n:
                self.docText[self.validCount[n]] = newCount[n]
        
        self.docText[self.VAL_TEXT] = newText
        self.docText[self.VAL_NOTE] = newNote
        
        return
    
    # def setCount(self, toTarget, parCount, sentCount, wordCount):
    #     statVals = {
    #         "paragraphs" : str(parCount),
    #         "sentences"  : str(sentCount),
    #         "words"      : str(wordCount),
    #     }
    #     if toTarget == self.DOC_MAIN:
    #         self.docText["current"]["stats"] = statVals
    #     elif toTarget == self.DOC_ASIDE:
    #         self.docAside["current"]["stats"] = statVals
    #     else:
    #         logger.error("BUG: Unknown document target")
    #     return
    
# End Class DocFile
