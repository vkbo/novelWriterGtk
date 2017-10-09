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
                    
                    itemAttrib     = xItem.attrib
                    itemHandle     = itemAttrib["handle"]
                    itemParent     = itemAttrib["parent"]
                    
                    itemName       = None
                    itemClass      = None
                    itemLevel      = None
                    itemType       = None
                    itemSubType    = None
                    itemNumber     = None
                    itemCompile    = None
                    itemComment    = None
                    itemImportance = None
                    itemRole       = None
                    
                    for xValue in xItem:
                        if   xValue.tag == "name":       itemName       = xValue.text
                        elif xValue.tag == "class":      itemClass      = xValue.text
                        elif xValue.tag == "level":      itemLevel      = xValue.text
                        elif xValue.tag == "type":       itemType       = xValue.text
                        elif xValue.tag == "subtype":    itemSubType    = xValue.text
                        elif xValue.tag == "number":     itemNumber     = xValue.text
                        elif xValue.tag == "compile":    itemCompile    = xValue.text
                        elif xValue.tag == "comment":    itemComment    = xValue.text
                        elif xValue.tag == "importance": itemImportance = xValue.text
                        elif xValue.tag == "role":       itemRole       = xValue.text
                        else:
                            logger.warning("BookOpen: Unknown item value '%s' in xml" % xValue.tag)
                            
                    self.appendTree(itemClass,itemLevel,itemType,itemHandle,itemParent,itemName)
                    
                    if itemLevel == NWC.ItemLevel.ROOT.name:
                        if itemType == NWC.ItemType.BOOK.name:
                            self.bookHandle = itemHandle
                            logger.verbose("BookOpen: Root book handle is %s" % itemHandle)
                        if itemType == NWC.ItemType.CHARS.name:
                            self.charHandle = itemHandle
                            logger.verbose("BookOpen: Root chars handle is %s" % itemHandle)
                        if itemType == NWC.ItemType.PLOTS.name:
                            self.plotHandle = itemHandle
                            logger.verbose("BookOpen: Root plots handle is %s" % itemHandle)
                        if itemType == NWC.ItemType.NOTES.name:
                            self.noteHandle = itemHandle
                            logger.verbose("BookOpen: Root notes handle is %s" % itemHandle)
                    if itemLevel == NWC.ItemLevel.ITEM.name:
                        if itemType == NWC.ItemType.BOOK.name:
                            self.appendChapter(itemHandle,itemSubType,itemNumber,itemCompile,itemComment)
                        elif itemType == NWC.ItemType.CHARS.name:
                            self.appendChar(itemHandle,itemImportance,itemRole,itemComment)
                        elif itemType == NWC.ItemType.PLOTS.name:
                            self.appendPlot(itemHandle,itemImportance,itemComment)
        
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
            NWC.ItemClass.CONTAINER,
            NWC.ItemLevel.ITEM,
            NWC.ItemType.BOOK,
            None,
            self.bookHandle,
            "New Chapter"
        )
        self.appendChapter(parHandle,NWC.BookType.CHAPTER,None,True,None)
        
        return
    
    def updateChapter(self,cHandle,cTarget,cValue):
        if cTarget == NWC.BookTree.NAME:
            self.theTree[self.theIndex[cHandle]][cTarget] = cValue.strip()
        elif cTarget in NWC.ChapterTree:
            self.chapterData[cHandle][cTarget] = cValue.strip()
        else:
            logger.debug("Trying to set an unknown field %s" % cTarget)
        return
    
    def addCharacter(self):
        
        parHandle = self.appendTree(
            NWC.ItemClass.CONTAINER,
            NWC.ItemLevel.ITEM,
            NWC.ItemType.CHARS,
            None,
            self.charHandle,
            "New Character"
        )
        self.appendChar(parHandle,None,None,None)
        
        return
    
    def updateCharacter(self,cHandle,cTarget,cValue):
        if cTarget == NWC.BookTree.NAME:
            self.theTree[self.theIndex[cHandle]][cTarget] = cValue.strip()
        elif cTarget in NWC.CharTree:
            self.charData[cHandle][cTarget] = cValue.strip()
        else:
            logger.debug("Trying to set an unknown field %s" % cTarget)
        return
    
    def addPlot(self):
        
        parHandle = self.appendTree(
            NWC.ItemClass.CONTAINER,
            NWC.ItemLevel.ITEM,
            NWC.ItemType.PLOTS,
            None,
            self.plotHandle,
            "New Plot"
        )
        self.appendPlot(parHandle,None,None)
        
        return
    
    def updatePlot(self,cHandle,cTarget,cValue):
        if cTarget == NWC.BookTree.NAME:
            self.theTree[self.theIndex[cHandle]][cTarget] = cValue.strip()
        elif cTarget in NWC.PlotTree:
            self.plotData[cHandle][cTarget] = cValue.strip()
        else:
            logger.debug("Trying to set an unknown field %s" % cTarget)
        return
    
    def getTreeEntry(self,itemHandle):
        return self.theTree[self.theIndex[itemHandle]]
    
    def appendTree(self,tClass,tLevel,tType,tHandle,pHandle,tName):
        """
        Appends an entry to the main project tree.
        """
        
        tClass  = self.checkEnumString(tClass,NWC.ItemClass,NWC.ItemClass.DOCUMENT,False)
        tLevel  = self.checkEnumString(tLevel,NWC.ItemLevel,NWC.ItemLevel.ROOT,False)
        tType   = self.checkEnumString(tType,NWC.ItemType,NWC.ItemType.NOTES,False)
        tHandle = self.checkString(tHandle,self.makeHandle(),False)
        pHandle = self.checkString(pHandle,None,True)
        tName   = self.checkString(tName,None,True)
        
        logger.verbose("BookOpen: Loading item '%s'"  % tName)
        logger.vverbose("BookOpen: Item class is %s"  % tClass)
        logger.vverbose("BookOpen: Item level is %s"  % tLevel)
        logger.vverbose("BookOpen: Item type is %s"   % tType)
        logger.vverbose("BookOpen: Item handle is %s" % tHandle)
        logger.vverbose("BookOpen: Item parent is %s" % pHandle)
        
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
        
        return tHandle
    
    def appendChapter(self,tHandle,cSubType,cNumber,cCompile,cComment):
        """
        Appends an entry to the chapter data dictionary
        """
        
        cSubType = self.checkEnumString(cSubType,NWC.BookType,NWC.BookType.CHAPTER,False)
        cNumber  = self.checkInt(cNumber,None,True)
        cCompile = self.checkBool(cCompile,False,False)
        cComment = self.checkString(cComment,None,True)
        
        logger.vverbose("BookOpen: Chapter subtype: %s"   % str(cSubType))
        logger.vverbose("BookOpen: Chapter number: %s"    % str(cNumber))
        logger.vverbose("BookOpen: Chapter compile: %s"   % str(cCompile))
        logger.vverbose("BookOpen: Chapter comment: '%s'" % str(cComment))
        
        self.theTree[self.theIndex[tHandle]][NWC.BookTree.SUBTYPE] = cSubType
        self.theTree[self.theIndex[tHandle]][NWC.BookTree.NUMBER]  = cNumber
        self.theTree[self.theIndex[tHandle]][NWC.BookTree.COMPILE] = cCompile
        self.theTree[self.theIndex[tHandle]][NWC.BookTree.COMMENT] = cComment
        
        return
    
    def appendChar(self,tHandle,cImportance,cRole,cComment):
        """
        Appends an entry to the character data dictionary
        """
        
        cImportance = self.checkInt(cImportance,None,True)
        cRole       = self.checkString(cRole,None,True)
        cComment    = self.checkString(cComment,None,True)
        
        logger.vverbose("BookOpen: Character importance; %s" % str(cImportance))
        logger.vverbose("BookOpen: Character role: '%s'"     % str(cRole))
        logger.vverbose("BookOpen: Character comment: '%s'"  % str(cComment))
        
        self.theTree[self.theIndex[tHandle]][NWC.BookTree.IMPORTANCE] = cImportance
        self.theTree[self.theIndex[tHandle]][NWC.BookTree.ROLE]       = cRole
        self.theTree[self.theIndex[tHandle]][NWC.BookTree.COMMENT]    = cComment
        
        return
    
    def appendPlot(self,tHandle,pImportance,pComment):
        """
        Appends an entry to the plot data dictionary
        """
        
        pImportance = self.checkInt(pImportance,None,True)
        pComment    = self.checkString(pComment,None,True)
        
        logger.vverbose("BookOpen: Plot importance; %s" % str(pImportance))
        logger.vverbose("BookOpen: Plot comment: '%s'"  % str(pComment))
        
        self.theTree[self.theIndex[tHandle]][NWC.BookTree.IMPORTANCE] = pImportance
        self.theTree[self.theIndex[tHandle]][NWC.BookTree.COMMENT]    = pComment
        
        return
    
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
    
    def checkEnumString(self,checkValue,enumItem,defaultValue,allowNone=False):
        if allowNone:
            if checkValue == None:   return None
            if checkValue == "None": return None
        for enumName in enumItem:
            if enumName.name == str(checkValue).upper():
                return enumName
        return defaultValue
    
    def checkBool(self,checkValue,defaultValue,allowNone=False):
        if allowNone:
            if checkValue == None:   return None
            if checkValue == "None": return None
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
