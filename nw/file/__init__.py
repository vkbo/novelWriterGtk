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
        self.charData   = {}
        self.plotData   = {}
        
        self.bookHandle = None
        self.charHandle = None
        self.plotHandle = None
        self.noteHandle = None
        
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
                    
                    itemAttrib  = xItem.attrib
                    itemHandle  = itemAttrib["handle"]
                    itemParent  = itemAttrib["parent"]
                    
                    itemName    = ""
                    itemClass   = None
                    itemLevel   = None
                    itemType    = None
                    
                    charImport  = 0
                    charRole    = ""
                    charComment = ""
                    
                    plotImport  = 0
                    plotComment = ""
                    
                    for xValue in xItem:
                        if xValue.tag == "name":
                            itemName    = xValue.text
                            logger.verbose("BookOpen: Loading item '%s'" % itemName)
                            logger.vverbose("BookOpen: Item handle is %s" % itemHandle)
                            logger.vverbose("BookOpen: Item parent is %s" % itemParent)
                        elif xValue.tag == "class":
                            itemClass   = self.getEnumFromString(NWC.ItemClass,xValue.text)
                            logger.vverbose("BookOpen: Item class is %s" % itemClass)
                        elif xValue.tag == "level":
                            itemLevel   = self.getEnumFromString(NWC.ItemLevel,xValue.text)
                            logger.vverbose("BookOpen: Item level is %s" % itemLevel)
                        elif xValue.tag == "type":
                            itemType    = self.getEnumFromString(NWC.ItemType,xValue.text)
                            logger.vverbose("BookOpen: Item type is %s" % itemType)
                        elif xValue.tag == "charImportance":
                            charImport  = xValue.text
                            logger.vverbose("BookOpen: Character importance is %s" % charImport)
                        elif xValue.tag == "charRole":
                            charRole    = xValue.text
                            logger.vverbose("BookOpen: Chararcter role is '%s'" % charRole)
                        elif xValue.tag == "charComment":
                            charComment = xValue.text
                            logger.vverbose("BookOpen: Chararcter comment is '%s'" % charComment)
                        elif xValue.tag == "plotImportance":
                            plotImport  = xValue.text
                            logger.vverbose("BookOpen: Plot importance is %s" % plotImport)
                        elif xValue.tag == "plotComment":
                            plotComment = xValue.text
                            logger.vverbose("BookOpen: Plot comment is '%s'" % plotComment)
                        else:
                            logger.warning("BookOpen: Unknown item value '%s' in xml" % xValue.tag)
                            
                    self.appendTree(itemClass,itemLevel,itemType,itemHandle,itemParent,itemName)
                    
                    if itemLevel == NWC.ItemLevel.ROOT:
                        if itemType == NWC.ItemType.BOOK:
                            self.bookHandle = itemHandle
                            logger.verbose("BookOpen: Root book handle is %s" % itemHandle)
                        if itemType == NWC.ItemType.CHARS:
                            self.charHandle = itemHandle
                            logger.verbose("BookOpen: Root chars handle is %s" % itemHandle)
                        if itemType == NWC.ItemType.PLOTS:
                            self.plotHandle = itemHandle
                            logger.verbose("BookOpen: Root plots handle is %s" % itemHandle)
                        if itemType == NWC.ItemType.NOTES:
                            self.noteHandle = itemHandle
                            logger.verbose("BookOpen: Root notes handle is %s" % itemHandle)
                    if itemLevel == NWC.ItemLevel.ITEM:
                        if itemType == NWC.ItemType.CHARS:
                            self.appendChar(itemHandle,charImport,charRole,charComment)
                        elif itemType == NWC.ItemType.PLOTS:
                            self.appendPlot(itemHandle,plotImport,plotComment)
        
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
                if treeItem[NWC.BookTree.TYPE] == NWC.ItemType.CHARS:
                    if itemHandle in self.charData:
                        xValue = ET.SubElement(xItem,"charImportance")
                        xValue.text = str(self.charData[itemHandle][NWC.CharTree.IMPORTANCE])
                        xValue = ET.SubElement(xItem,"charRole")
                        xValue.text = str(self.charData[itemHandle][NWC.CharTree.ROLE])
                        xValue = ET.SubElement(xItem,"charComment")
                        xValue.text = str(self.charData[itemHandle][NWC.CharTree.COMMENT])
                if treeItem[NWC.BookTree.TYPE] == NWC.ItemType.PLOTS:
                    if itemHandle in self.plotData:
                        xValue = ET.SubElement(xItem,"plotImportance")
                        xValue.text = str(self.plotData[itemHandle][NWC.PlotTree.IMPORTANCE])
                        xValue = ET.SubElement(xItem,"plotComment")
                        xValue.text = str(self.plotData[itemHandle][NWC.PlotTree.COMMENT])
                        
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
    
    def addCharacter(self):
        
        parHandle = self.appendTree(
            NWC.ItemClass.CONTAINER,
            NWC.ItemLevel.ITEM,
            NWC.ItemType.CHARS,
            None,
            self.charHandle,
            "New Character"
        )
        self.appendChar(parHandle,0,"","")
        
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
        self.appendPlot(parHandle,0,"")
        
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
        
        return tHandle
    
    def appendChar(self,tHandle,cImportance,cRole,cComment):
        """
        Appends an entry to the character data dictionary
        """
        
        if cImportance == None: cImportance = 0
        if cRole       == None: cRole       = ""
        if cComment    == None: cComment    = ""
        
        self.charData[tHandle] = {
            NWC.CharTree.IMPORTANCE : cImportance,
            NWC.CharTree.ROLE       : cRole,
            NWC.CharTree.COMMENT    : cComment,
        }
        logger.verbose("Added data to character %s" % tHandle)
        
        return
    
    def appendPlot(self,tHandle,pImportance,pComment):
        """
        Appends an entry to the plot data dictionary
        """
        
        if pImportance == None: pImportance = 0
        if pComment    == None: pComment    = ""
        
        self.plotData[tHandle] = {
            NWC.PlotTree.IMPORTANCE : pImportance,
            NWC.PlotTree.COMMENT    : pComment,
        }
        logger.verbose("Added data to plot %s" % tHandle)
        
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
    
# End Class DataStore
