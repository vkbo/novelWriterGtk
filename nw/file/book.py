# -*- coding: utf-8 -*
"""novelWriter Book Project Class

 novelWriter – Book Project Class
==================================
 The class containign the book project itself

 File History:
 Created: 2017-10-06 [0.4.0]

"""

import logging
import nw
import lxml.etree as ET

from os           import path, mkdir
from nw.file.item import BookItem
from nw.file.tree import BookTree
from nw.file.doc  import DocFile

logger = logging.getLogger(__name__)

class Book():
    
    def __init__(self):
        
        self.bookLoaded  = False
        
        self.bookPath    = None
        self.docPath     = None
        self.theTree     = BookTree()
        
        # Book Settings
        self.bookTitle   = ""
        self.bookAuthors = []
        
        # Connect Functions
        self.addFile      = self.theTree.addFile
        self.addChapter   = self.theTree.addChapter
        self.addCharacter = self.theTree.addCharacter
        self.addPlot      = self.theTree.addPlot
        self.getItem      = self.theTree.getItem
        
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
            self.theTree.setPath(self.docPath)

        self.bookPath = bookPath
        
        nwXML = ET.parse(bookPath)
        xRoot = nwXML.getroot()
        
        nwxRoot     = xRoot.tag
        appVersion  = xRoot.attrib["appVersion"]
        fileVersion = xRoot.attrib["fileVersion"]

        logger.verbose("XML: Root is %s" % nwxRoot)
        logger.verbose("XML: File version is %s" % fileVersion)
        
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
                        if xValue.tag == "meta":
                            for metaTag in xValue.attrib.keys():
                                bookItem.setFromTag(metaTag,xValue.attrib[metaTag])
                        else:
                            bookItem.setFromTag(xValue.tag,xValue.text)
                    self.theTree.appendItem(itemHandle,itemParent,bookItem)
        
        self.bookLoaded = True
        self.theTree.validateTree()
        self.theTree.sortTree()
        
        return
    
    def saveBook(self):
        
        bookDir  = path.dirname(self.bookPath)
        bookFile = path.basename(self.bookPath)
        logger.vverbose("BookSave: Folder is %s" % bookDir)
        logger.vverbose("BookSave: File is %s" % bookFile)
        
        if bookFile[-4:] == ".nwx":
            self.docPath = path.join(bookDir,bookFile[:-4]+".nwd")
            self.theTree.setPath(self.docPath)
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
        
        xContent = ET.SubElement(nwXML,"content",attrib={"count":str(len(self.theTree.theTree))})
        itemIdx  = 0
        for treeItem in self.theTree.theTree:
            
            itemHandle = str(treeItem["handle"])
            parHandle  = str(treeItem["parent"])
            
            xItem = ET.SubElement(xContent,"item",attrib={
                "idx"    : str(itemIdx),
                "handle" : str(itemHandle),
                "parent" : str(parHandle),
            })
            
            fileMeta = {}
            for metaTag in treeItem["entry"].validMeta:
                metaValue = treeItem["entry"].getFromTag(metaTag)
                if not metaValue is None:
                    fileMeta[metaTag] = str(metaValue)
            if len(fileMeta) > 0:
                xMeta = ET.SubElement(xItem,"meta",attrib=fileMeta)
            
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
        
        self.theTree.createRootItem(BookItem.TYP_BOOK)
        self.theTree.createRootItem(BookItem.TYP_CHAR)
        self.theTree.createRootItem(BookItem.TYP_PLOT)
        self.theTree.createRootItem(BookItem.TYP_NOTE)
        
        return
    
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
    
# End Class Book
