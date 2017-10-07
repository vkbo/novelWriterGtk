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
import xml.etree.ElementTree as ET

from os          import path, mkdir
from xml.dom     import minidom
from time        import time
from hashlib     import sha256
# from datetime    import datetime
from nw.file.doc import DocFile

logger = logging.getLogger(__name__)

class Book():
    
    def __init__(self):
        
        self.bookLoaded = False
        
        self.bookPath   = None
        self.docPath    = None
        self.theTree    = []
        self.theIndex   = {}
        
        # Book Settings
        self.bookTitle   = ""
        self.bookAuthors = []
        
        return
    
    def openBook(self, bookPath):
        
        if not path.isfile(bookPath):
            logger.error("Path not found: %s" % bookPath)
            return
        
        self.bookPath = bookPath
        
        nwXML = ET.parse(bookPath)
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
            if xChild.tag == "book":
                logger.debug("BookOpen: Found book data")
                for xItem in xChild:
                    if xItem.tag == "title":
                        logger.verbose("BookOpen: Title is '%s'" % xItem.text)
                        self.bookTitle = xItem.text
                    elif xItem.tag == "author":
                        logger.verbose("BookOpen: Author: '%s'" % xItem.text)
                        self.bookAuthors.append(xItem.text)
            elif xChild.tag == "content":
                logger.debug("BookOpen: Found book content")
                for xItem in xChild:
                    itemName   = xItem.text
                    itemAttrib = xItem.attrib
                    itemClass  = self.getEnumFromString(NWC.ItemClass,itemAttrib["class"])
                    itemLevel  = self.getEnumFromString(NWC.ItemLevel,itemAttrib["level"])
                    itemType   = self.getEnumFromString(NWC.ItemType,itemAttrib["type"])
                    itemHandle = itemAttrib["handle"]
                    itemParent = itemAttrib["parent"]
                    logger.verbose("BookOpen: Loading item '%s'" % itemName)
                    logger.vverbose("BookOpen: Item class is %s" % itemClass)
                    logger.vverbose("BookOpen: Item level is %s" % itemLevel)
                    logger.vverbose("BookOpen: Item type is %s" % itemType)
                    logger.vverbose("BookOpen: Item handle is %s" % itemHandle)
                    logger.vverbose("BookOpen: Item parent is %s" % itemParent)
                    self.appendTree(itemClass,itemLevel,itemType,itemHandle,itemParent,itemName)
        
        self.bookLoaded = True
        
        return
    
    def saveBook(self):
        
        bookDir  = path.dirname(self.bookPath)
        bookFile = path.basename(self.bookPath)
        logger.vverbose("BookSave: Folder is %s" % bookDir)
        logger.vverbose("BookSave: File is %s" % bookFile)
        
        if bookFile[-4:] == ".nwx":
            self.docPath = path.join(bookDir,bookFile[:-4]+".nwd")
            if not path.isdir(self.docPath):
                logger.info("BookSave: Created folder %s" % self.docPath)
                mkdir(self.docPath)
        
        nwXML = ET.Element("novelWriterXML",attrib={
            "fileVersion" : "1.0",
            "appVersion"  : str(nw.__version__),
        })
        xBook = ET.SubElement(nwXML,"book")
        xBookTitle = ET.SubElement(xBook,"title")
        xBookTitle.text = self.bookTitle
        for bookAuthor in self.bookAuthors:
            xBookAuthor = ET.SubElement(xBook,"author")
            xBookAuthor.text = bookAuthor
        
        xContent = ET.SubElement(nwXML,"content",attrib={"count":str(len(self.theTree))})
        itemIdx  = 0
        for treeItem in self.theTree:
            tmpXML = ET.SubElement(xContent,"item",attrib={
                "idx"    : str(itemIdx),
                "class"  : str(treeItem[NWC.BookTree.CLASS].name),
                "level"  : str(treeItem[NWC.BookTree.LEVEL].name),
                "type"   : str(treeItem[NWC.BookTree.TYPE].name),
                "handle" : str(treeItem[NWC.BookTree.HANDLE]),
                "parent" : str(treeItem[NWC.BookTree.PARENT]),
            })
            tmpXML.text = str(treeItem[NWC.BookTree.NAME])
            itemIdx += 1
        
        roughXML  = ET.tostring(nwXML,"utf-8")
        prettyXML = minidom.parseString(roughXML)
        with open(self.bookPath,"wt") as outFile:
            prettyXML.writexml(outFile,indent="",addindent="  ",newl="\n")
        
        return True
    
    def createBook(self):
        
        logger.debug("Creating empty book project")
        
        itCls = NWC.ItemClass.CONTAINER
        itLvl = NWC.ItemLevel.ROOT
        
        self.appendTree(itCls,itLvl,NWC.ItemType.BOOK, None,None,"Book")
        self.appendTree(itCls,itLvl,NWC.ItemType.CHARS,None,None,"Characters")
        self.appendTree(itCls,itLvl,NWC.ItemType.PLOTS,None,None,"Plots")
        self.appendTree(itCls,itLvl,NWC.ItemType.NOTES,None,None,"Notes")
        
        return True
    
    def setBookPath(self, bookPath):
        self.bookPath = bookPath
        return
    
    def setTitle(self, bookTitle):
        logger.debug("Book title changed to '%s'" % bookTitle)
        self.bookTitle = bookTitle.strip()
        return
    
    def setAuthors(self, bookAuthors):
        self.bookAuthors = []
        authList = bookAuthors.split(",")
        for author in authList:
            logger.debug("Book author '%s' added" % author.strip())
            self.bookAuthors.append(author.strip())
        return
    
    def createDoc(self, docTitle, docType):
        
        
        return True
    
    def getTreeEntry(self,itemHandle):
        return self.theTree[self.theIndex[itemHandle]]
    
    def appendTree(self,tClass,tLevel,tType,tHandle,pHandle,tName):
        """
        Appends an entry to the main project tree.
        """

        if tHandle == None:
            tHandle = self.makeHandle()
        if pHandle == "None":
            pHandle = None

        self.theTree.append({
            NWC.BookTree.CLASS  : tClass,
            NWC.BookTree.LEVEL  : tLevel,
            NWC.BookTree.TYPE   : tType,
            NWC.BookTree.HANDLE : tHandle,
            NWC.BookTree.PARENT : pHandle,
            NWC.BookTree.NAME   : tName,
        })
        self.theIndex[tHandle] = len(self.theTree)-1
        
        logger.verbose("Added item %s named '%s' to the project tree" % (tHandle,tName))
        
        return True
    
    def makeHandle(self,seed=""):
        itemHandle = sha256((str(time())+seed).encode()).hexdigest()[0:13]
        if itemHandle in self.theIndex.keys():
            logger.warning("Duplicate handle encountered! Retrying ...")
            itemHandle = self.makeHandle(seed+"!")
        return itemHandle
    
    def getEnumFromString(self,enumItem,lookUp):
        for enumName in enumItem:
            if enumName.name == lookUp:
                return enumName
        return None
    
# End Class DataStore
