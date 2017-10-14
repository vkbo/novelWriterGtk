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
import lxml.etree as ET

from os           import path, mkdir
from time         import time
from hashlib      import sha256
from nw.file.item import BookItem
from nw.file.doc  import DocFile

logger = logging.getLogger(__name__)

class Book():
    
    def __init__(self):
        
        self.bookLoaded  = False
        
        self.bookPath    = None
        self.docPath     = None
        self.theTree     = []
        self.theIndex    = {}
        self.lvlIndex    = {}
        self.rootIndex   = {}
        
        self.bookHandle  = None
        self.charHandle  = None
        self.plotHandle  = None
        self.noteHandle  = None
        
        # Book Settings
        self.bookTitle   = ""
        self.bookAuthors = []
        
        # Prepar empty indices
        for itemLevel in BookItem.validLevels: self.lvlIndex[itemLevel] = {}
        for itemType in BookItem.validTypes:   self.rootIndex[itemType] = None
        
        return
    
    #
    # Project File I/O and Creation
    #
    
    def openBook(self, bookPath):
        
        if not path.isfile(bookPath):
            logger.error("Path not found: %s" % bookPath)
            return
        
        if bookPath[-4:] == ".nwx":
            self.docPath = bookPath[:-4]+".nwd"

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
                    self.appendTree(itemHandle,itemParent,bookItem)
        
        self.bookLoaded = True
        self.validateTree()
        
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
            
            itemHandle = str(treeItem["handle"])
            parHandle  = str(treeItem["parent"])
            
            xItem = ET.SubElement(xContent,"item",attrib={
                "idx"    : str(itemIdx),
                "handle" : str(itemHandle),
                "parent" : str(parHandle),
            })
            
            for entryTag in treeItem["entry"].validTags:
                entryValue = treeItem["entry"].getFromTag(entryTag)
                if not entryValue is None:
                    xValue = ET.SubElement(xItem,entryTag)
                    xValue.text = str(entryValue)
                        
            itemIdx += 1
        
        with open(self.bookPath,"wb") as outFile:
            outFile.write(ET.tostring(
                nwXML,
                pretty_print    = True,
                encoding        = "utf-8",
                xml_declaration = True
            ))
        
        return True
    
    def createBook(self):
        
        logger.debug("Creating empty book project")
        
        bookHandle = self.makeHandle()
        charHandle = self.makeHandle()
        plotHandle = self.makeHandle()
        noteHandle = self.makeHandle()
        
        newBookItem = BookItem()
        newBookItem.setClass(BookItem.CLS_CONT)
        newBookItem.setLevel(BookItem.LEV_ROOT)
        newBookItem.setType(BookItem.TYP_BOOK)
        newBookItem.setName("Book")
        
        newCharItem = BookItem()
        newCharItem.setClass(BookItem.CLS_CONT)
        newCharItem.setLevel(BookItem.LEV_ROOT)
        newCharItem.setType(BookItem.TYP_CHAR)
        newCharItem.setName("Characters")
        
        newPlotItem = BookItem()
        newPlotItem.setClass(BookItem.CLS_CONT)
        newPlotItem.setLevel(BookItem.LEV_ROOT)
        newPlotItem.setType(BookItem.TYP_PLOT)
        newPlotItem.setName("Plots")
        
        newNoteItem = BookItem()
        newNoteItem.setClass(BookItem.CLS_CONT)
        newNoteItem.setLevel(BookItem.LEV_ROOT)
        newNoteItem.setType(BookItem.TYP_NOTE)
        newNoteItem.setName("Notes")
        
        self.appendTree(bookHandle,None,newBookItem)
        self.appendTree(charHandle,None,newCharItem)
        self.appendTree(plotHandle,None,newPlotItem)
        self.appendTree(noteHandle,None,newNoteItem)
        
        return True
    
    #
    #  Set Functions
    #
    
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
    
    #
    # Add Elements to Main Tree
    #
    
    def addFile(self, pHandle):
        
        parEntry = self.getTreeEntry(pHandle)["entry"]
        parClass = parEntry.itemClass
        parType  = parEntry.itemType
        
        if not parClass == BookItem.CLS_CONT:
            logger.debug("Item is not a folder, getting its parent")
            parParent = self.getTreeEntry(pHandle)["parent"]
            if not parParent is None:
                pHandle  = parParent
                parEntry = self.getTreeEntry(pHandle)["entry"]
                parClass = parEntry.itemClass
                parType  = parEntry.itemType
            else:
                logger.error("A file must be added to a folder")
        
        if parType == BookItem.TYP_BOOK:
            newClass   = BookItem.CLS_SCENE
            newName    = "New Scene"
            newCompile = True
        else:
            newClass   = BookItem.CLS_NOTE
            newName    = "New Note"
            newCompile = None
        
        newItem = BookItem()
        newItem.setClass(newClass)
        newItem.setLevel(BookItem.LEV_FILE)
        newItem.setType(parType)
        newItem.setName(newName)
        newItem.setCompile(newCompile)
        
        self.appendTree(None,pHandle,newItem,docItem)
        
        return
    
    def addChapter(self):
        
        newItem = BookItem()
        newItem.setClass(BookItem.CLS_CONT)
        newItem.setLevel(BookItem.LEV_ITEM)
        newItem.setType(BookItem.TYP_BOOK)
        newItem.setSubType(BookItem.SUB_CHAP)
        newItem.setName("New Chapter")
        newItem.setCompile(True)
        
        self.appendTree(None,self.rootIndex[BookItem.TYP_BOOK],newItem)
        
        return
    
    def addCharacter(self):
        
        newItem = BookItem()
        newItem.setClass(BookItem.CLS_CONT)
        newItem.setLevel(BookItem.LEV_ITEM)
        newItem.setType(BookItem.TYP_CHAR)
        newItem.setName("New Character")
        
        self.appendTree(None,self.rootIndex[BookItem.TYP_CHAR],newItem)
        
        return
    
    def addPlot(self):
        
        newItem = BookItem()
        newItem.setClass(BookItem.CLS_CONT)
        newItem.setLevel(BookItem.LEV_ITEM)
        newItem.setType(BookItem.TYP_PLOT)
        newItem.setName("New Plot")
        
        self.appendTree(None,self.rootIndex[BookItem.TYP_PLOT],newItem)
        
        return
    
    #
    # Data Tree Maintenance
    #
    
    def updateTreeEntry(self,tHandle,tTag,tValue):
        self.theTree[self.theIndex[tHandle]]["entry"].setFromTag(tTag,tValue.strip())
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
        
        if bookItem.itemLevel == BookItem.LEV_FILE:
            docItem = DocFile(self.docPath,tHandle,bookItem.itemClass)
        else:
            docItem = None
        
        self.theTree.append({
            "handle" : tHandle,
            "parent" : pHandle,
            "entry"  : bookItem,
            "doc"    : docItem,
        })
        lastIdx = len(self.theTree)-1
        self.theIndex[tHandle] = lastIdx
        self.lvlIndex[bookItem.itemLevel][tHandle] = lastIdx
        
        return
    
    def validateTree(self):
        
        errCount = 0
        
        # Checking ROOT level
        for treeItem in self.theTree:
            
            itemHandle = treeItem["handle"]
            itemParent = treeItem["parent"]
            bookEntry  = treeItem["entry"]
            itemIdx    = self.theIndex[itemHandle]
            
            if not bookEntry.itemLevel == BookItem.LEV_ROOT: continue
            logger.verbose("Checking ROOT with handle %s" % itemHandle)
            
            if not itemParent is None:
                self.theTree[itemIdx]["parent"] = None
                logger.warning("Parent was set for ROOT element %s" % itemHandle)
                errCount += 1
            
            for itemType in bookEntry.validTypes:
                if bookEntry.itemType == itemType:
                    if self.rootIndex[itemType] is None:
                        self.rootIndex[itemType] = itemHandle
                        logger.debug("Root handle for type %s set to %s" % (itemType,itemHandle))
                    else:
                        logger.warning("Encountered a second ROOT of type %s with handle %s" % (itemType,itemHandle))
                        errCount += 1
            
        # Checking ITEM level
        for treeItem in self.theTree:
            
            itemHandle = treeItem["handle"]
            itemParent = treeItem["parent"]
            bookEntry  = treeItem["entry"]
            itemIdx    = self.theIndex[itemHandle]
            hasError   = False
            
            if not bookEntry.itemLevel == BookItem.LEV_ITEM: continue
            logger.verbose("Checking ITEM with handle %s" % itemHandle)
            
            for itemType in bookEntry.validTypes:
                if bookEntry.itemType == itemType:
                    if itemParent is None:
                        logger.warning("Parent was missing for ITEM of type %s with handle %s" % (itemType,itemHandle))
                        self.theTree[itemIdx]["parent"] = self.rootIndex[itemType]
                        errCount += 1
        
        logger.info("Found %d error(s) while parsing the project file" % errCount)
        
        return
    
    #
    # Internal Functions
    #
    
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
    
# End Class Book
