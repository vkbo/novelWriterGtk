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

from os           import path, mkdir
from xml.dom      import minidom
from time         import time
from hashlib      import sha256
from nw.file.item import BookItem

logger = logging.getLogger(__name__)

class Book():
    
    def __init__(self):
        
        self.bookLoaded  = False
        
        self.bookPath    = None
        self.docPath     = None
        self.theTree     = []
        self.theIndex    = {}
        
        self.bookHandle  = None
        self.charHandle  = None
        self.plotHandle  = None
        self.noteHandle  = None
        
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
                    itemAttrib = xItem.attrib
                    itemHandle = itemAttrib["handle"]
                    itemParent = itemAttrib["parent"]
                    bookItem   = BookItem()
                    for xValue in xItem:
                        bookItem.setFromTag(xValue.tag,xValue.text)
                        # try:
                        #     bookKey = NWC.BookTree[xValue.tag.upper()]
                        #     itemValues[bookKey] = xValue.text
                        # except:
                        #     logger.warning("BookOpen: Unknown XML tag '%s' in item "
                        #                    "with handle %s" % (xValue.tag,itemHandle))
                    self.appendTree(itemHandle,itemParent,bookItem)
        
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
            
            itemHandle = str(treeItem[NWC.BookTree.HANDLE])
            parHandle  = str(treeItem[NWC.BookTree.PARENT])
            
            xItem = ET.SubElement(xContent,"item",attrib={
                "idx"    : str(itemIdx),
                "handle" : str(itemHandle),
                "parent" : str(parHandle),
            })
            
            xValue = ET.SubElement(xItem,"class")
            xValue.text = str(treeItem[NWC.BookTree.CLASS].name)
            xValue = ET.SubElement(xItem,"level")
            xValue.text = str(treeItem[NWC.BookTree.LEVEL].name)
            xValue = ET.SubElement(xItem,"type")
            xValue.text = str(treeItem[NWC.BookTree.TYPE].name)
            xValue = ET.SubElement(xItem,"name")
            xValue.text = str(treeItem[NWC.BookTree.NAME])
            
            if treeItem[NWC.BookTree.LEVEL] == NWC.ItemLevel.ITEM:
                if treeItem[NWC.BookTree.TYPE] == NWC.ItemType.BOOK:
                    xValue = ET.SubElement(xItem,"subtype")
                    xValue.text = str(treeItem[NWC.BookTree.SUBTYPE].name)
                    xValue = ET.SubElement(xItem,"number")
                    xValue.text = str(treeItem[NWC.BookTree.NUMBER])
                    xValue = ET.SubElement(xItem,"compile")
                    xValue.text = str(treeItem[NWC.BookTree.COMPILE])
                    xValue = ET.SubElement(xItem,"comment")
                    xValue.text = str(treeItem[NWC.BookTree.COMMENT])
                if treeItem[NWC.BookTree.TYPE] == NWC.ItemType.CHARS:
                    xValue = ET.SubElement(xItem,"importance")
                    xValue.text = str(treeItem[NWC.BookTree.IMPORTANCE])
                    xValue = ET.SubElement(xItem,"role")
                    xValue.text = str(treeItem[NWC.BookTree.ROLE])
                    xValue = ET.SubElement(xItem,"comment")
                    xValue.text = str(treeItem[NWC.BookTree.COMMENT])
                if treeItem[NWC.BookTree.TYPE] == NWC.ItemType.PLOTS:
                    xValue = ET.SubElement(xItem,"importance")
                    xValue.text = str(treeItem[NWC.BookTree.IMPORTANCE])
                    xValue = ET.SubElement(xItem,"comment")
                    xValue.text = str(treeItem[NWC.BookTree.COMMENT])
                        
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
        
        self.bookHandle = self.makeHandle()
        self.charHandle = self.makeHandle()
        self.plotHandle = self.makeHandle()
        self.noteHandle = self.makeHandle()
        
        self.appendTree(itCls,itLvl,NWC.ItemType.BOOK, self.bookHandle,None,"Book")
        self.appendTree(itCls,itLvl,NWC.ItemType.CHARS,self.charHandle,None,"Characters")
        self.appendTree(itCls,itLvl,NWC.ItemType.PLOTS,self.plotHandle,None,"Plots")
        self.appendTree(itCls,itLvl,NWC.ItemType.NOTES,self.noteHandle,None,"Notes")
        
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
        return
    
    def addChapter(self):
        
        parHandle = self.appendTree(
            None,
            self.bookHandle,
            {
                NWC.BookTree.CLASS   : NWC.ItemClass.CONTAINER.name,
                NWC.BookTree.LEVEL   : NWC.ItemLevel.ITEM.name,
                NWC.BookTree.TYPE    : NWC.ItemType.BOOK.name,
                NWC.BookTree.NAME    : "New Chapter",
                NWC.BookTree.SUBTYPE : NWC.BookType.CHAPTER.name,
                NWC.BookTree.NUMBER  : None,
                NWC.BookTree.COMPILE : True,
                NWC.BookTree.COMMENT : None,
            }
        )
        
        return
    
    def addCharacter(self):
        
        parHandle = self.appendTree(
            None,
            self.charHandle,
            {
                NWC.BookTree.CLASS      : NWC.ItemClass.CONTAINER.name,
                NWC.BookTree.LEVEL      : NWC.ItemLevel.ITEM.name,
                NWC.BookTree.TYPE       : NWC.ItemType.CHARS.name,
                NWC.BookTree.NAME       : "New Character",
                NWC.BookTree.IMPORTANCE : None,
                NWC.BookTree.ROLE       : None,
                NWC.BookTree.COMMENT    : None,
            }
        )
        
        return
    
    def addPlot(self):
        
        parHandle = self.appendTree(
            None,
            self.plotHandle,
            {
                NWC.BookTree.CLASS      : NWC.ItemClass.CONTAINER.name,
                NWC.BookTree.LEVEL      : NWC.ItemLevel.ITEM.name,
                NWC.BookTree.TYPE       : NWC.ItemType.PLOTS.name,
                NWC.BookTree.NAME       : "New Plot",
                NWC.BookTree.IMPORTANCE : None,
                NWC.BookTree.COMMENT    : None,
            }
        )
        
        return
    
    def updateTreeEntry(self,tHandle,tTarget,tValue):
        self.theTree[self.theIndex[tHandle]][tTarget] = tValue.strip()
        return
    
    def getTreeEntry(self,itemHandle):
        return self.theTree[self.theIndex[itemHandle]]
    
    def appendTree(self,tHandle,pHandle,bookItem):
        """
        Appends an entry to the main project tree.
        """
        
        tHandle = self.checkString(tHandle,self.makeHandle(),False)
        pHandle = self.checkString(pHandle,None,True)
        
        logger.verbose("BookOpen: Adding item %s with parent %s" % (str(tHandle),str(pHandle)))
        
        self.theTree.append({
            "handle" : tHandle,
            "parent" : pHandle,
            "item"   : bookItem,
        })
        lastIdx = len(self.theTree)-1
        self.theIndex[tHandle] = lastIdx
        
        return
        
        # # Fields set for all items
        # try:
        #     tClass = NWC.ItemClass[iValues[NWC.BookTree.CLASS].upper()]
        # except:
        #     logger.error("BookOpen: - class tag missing")
        #     return None
        # 
        # try:
        #     tLevel = NWC.ItemLevel[iValues[NWC.BookTree.LEVEL].upper()]
        # except:
        #     logger.error("BookOpen: - level tag missing")
        #     return None
        # 
        # try:
        #     tType = NWC.ItemType[iValues[NWC.BookTree.TYPE].upper()]
        # except:
        #     logger.error("BookOpen: - type tag missing")
        #     return None
        # 
        # try:
        #     tName = self.checkString(iValues[NWC.BookTree.NAME],None,True)
        # except:
        #     logger.warning("BookOpen: - name tag missing")
        #     tName = None
        # 
        # logger.vverbose("BookOpen: - class: %s"   % tClass)
        # logger.vverbose("BookOpen: - level: %s"   % tLevel)
        # logger.vverbose("BookOpen: - type: %s"    % tType)
        # logger.vverbose("BookOpen: - name: %s"    % tName)
        # 
        # self.theTree.append({
        #     NWC.BookTree.HANDLE  : tHandle,
        #     NWC.BookTree.PARENT  : pHandle,
        #     NWC.BookTree.CLASS   : tClass,
        #     NWC.BookTree.LEVEL   : tLevel,
        #     NWC.BookTree.TYPE    : tType,
        #     NWC.BookTree.NAME    : tName,
        # })
        # lastIdx = len(self.theTree)-1
        # self.theIndex[tHandle] = lastIdx
        # 
        # if tLevel == NWC.ItemLevel.ROOT:
        #     if tType == NWC.ItemType.BOOK:  self.bookHandle = tHandle
        #     if tType == NWC.ItemType.CHARS: self.charHandle = tHandle
        #     if tType == NWC.ItemType.PLOTS: self.plotHandle = tHandle
        #     if tType == NWC.ItemType.NOTES: self.noteHandle = tHandle
        #     
        #     # Root items should have no further elements, so return here
        #     return tHandle
        # 
        # #
        # # Add additional values for specific item types
        # #
        # 
        # # Comments
        # if tType.name in ("BOOK","CHARS","PLOTS"):
        #     try:
        #         tComment = self.checkString(iValues[NWC.BookTree.COMMENT],None,True)
        #     except:
        #         logger.warning("BookOpen: - comment tag missing")
        #         tComment = None
        #     logger.vverbose("BookOpen: - comment: %s" % tComment)
        #     self.theTree[lastIdx][NWC.BookTree.COMMENT] = tComment
        # 
        # # SubType
        # if tType.name == "BOOK":
        #     try:
        #         tSubType = NWC.BookType[iValues[NWC.BookTree.SUBTYPE].upper()]
        #     except:
        #         logger.error("BookOpen: - subtype tag missing")
        #         return None
        #     logger.vverbose("BookOpen: - subtype: %s" % tSubType)
        #     self.theTree[lastIdx][NWC.BookTree.SUBTYPE] = tSubType
        #     
        # # Number
        # if tType.name == "BOOK":
        #     try:
        #         tNumber = self.checkInt(iValues[NWC.BookTree.NUMBER],None,True)
        #     except:
        #         logger.warning("BookOpen: - number tag missing")
        #         tNumber = None
        #     logger.vverbose("BookOpen: - number: %s" % tNumber)
        #     self.theTree[lastIdx][NWC.BookTree.NUMBER] = tNumber
        #     
        # # Compile
        # if tType.name == "BOOK":
        #     try:
        #         tCompile = self.checkBool(iValues[NWC.BookTree.COMPILE],False,False)
        #     except:
        #         logger.warning("BookOpen: - compile tag missing")
        #         tCompile = False
        #     logger.vverbose("BookOpen: - compile: %s" % tCompile)
        #     self.theTree[lastIdx][NWC.BookTree.COMPILE] = tCompile
        # 
        # # Importance
        # if tType.name in ("CHARS","PLOTS"):
        #     try:
        #         tImportance = self.checkInt(iValues[NWC.BookTree.IMPORTANCE],None,True)
        #     except:
        #         logger.warning("BookOpen: - importance tag missing")
        #         tImportance = None
        #     logger.vverbose("BookOpen: - importance: %s" % tImportance)
        #     self.theTree[lastIdx][NWC.BookTree.IMPORTANCE] = tImportance
        # 
        # # Role: only for Character Type
        # if tType.name == "CHARS":
        #     try:
        #         tRole = self.checkString(iValues[NWC.BookTree.ROLE],None,True)
        #     except:
        #         logger.warning("BookOpen: - role tag missing")
        #         tRole = None
        #     logger.vverbose("BookOpen: - role: %s" % tRole)
        #     self.theTree[lastIdx][NWC.BookTree.ROLE] = tRole
        # 
        # return tHandle
    
    def makeHandle(self,seed=""):
        itemHandle = sha256((str(time())+seed).encode()).hexdigest()[0:13]
        if itemHandle in self.theIndex.keys():
            logger.warning("Duplicate handle encountered! Retrying ...")
            itemHandle = self.makeHandle(seed+"!")
        return itemHandle
    
    def checkBool(self,checkValue,defaultValue,allowNone=False):
        if allowNone:
            if checkValue == None:   return None
            if checkValue == "None": return None
        if isinstance(checkValue,bool):
            return checkValue
        if isinstance(checkValue,str):
            if checkValue.lower() == "false": return False
            if checkValue.lower() == "true":  return True
        return defaultValue
    
    def checkInt(self,checkValue,defaultValue,allowNone=False):
        if allowNone:
            if checkValue == None:   return None
            if checkValue == "None": return None
        try:
            return int(checkValue)
        except:
            return defaultValue
    
    def checkString(self,checkValue,defaultValue,allowNone=False):
        if allowNone:
            if checkValue == None:   return None
            if checkValue == "None": return None
        if isinstance(checkValue,str): return str(checkValue)
        return defaultValue
        
    
# End Class DataStore
