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
from nw.functions import getTimeStamp

logger = logging.getLogger(__name__)

class Book():
    
    def __init__(self):
        """The main book project class holding the tree of all its items, and all the buffers for
        the currently opened files.
        ToDo: Add field for book status, i.e. draft, idea, final, etc. Maybe a date field too."""
        
        self.bookLoaded   = False
        self.bookPath     = None
        self.docPath      = None
        self.theTree      = BookTree()
        
        # Book Settings
        self.bookTitle    = ""
        self.bookAuthors  = []
        
        # Connect Functions
        self.addFile      = self.theTree.addFile
        self.addChapter   = self.theTree.addChapter
        self.addCharacter = self.theTree.addCharacter
        self.addPlot      = self.theTree.addPlot
        self.getItem      = self.theTree.getItem
        self.updateItem   = self.theTree.updateItem
        self.changeOrder  = self.theTree.changeOrder
        
        return
    
    #
    # Project File I/O and Creation
    #
    
    def closeBook(self):
        
        logger.info("Closing book project")
        logger.debug("Resetting all project variables")
        
        self.bookLoaded  = False
        self.bookPath    = None
        self.docPath     = None
        self.theTree.clearTree()
        
        # Book Settings
        self.bookTitle   = ""
        self.bookAuthors = []
        
        return
    
    def openBook(self, bookPath):
        """Open a book project file. For robustness, we iterate through everything in the xml file
        and let the BookItem class determine whether the data is each element makes sense or not.
        Since both the open and save functions just iterates through everything, redundant data
        could possibly pass in and out of the buffer, but this could be prevented by adding a
        verify function in the BookItem class."""
        
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
                    if xItem.text is None: continue
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
                    if "handle" in xItem.attrib:
                        itemHandle = itemAttrib["handle"]
                    else:
                        logger.error("BookOpen: Entry missing handle, Skipping")
                        continue
                    if "parent" in xItem.attrib:
                        itemParent = itemAttrib["parent"]
                    else:
                        itemParent = None
                    if "order" in xItem.attrib:
                        itemOrder = itemAttrib["order"]
                    else:
                        itemOrder = None
                    bookItem = BookItem()
                    for xValue in xItem:
                        if xValue.tag == "meta":
                            for metaTag in xValue.attrib.keys():
                                bookItem.setFromTag(metaTag,xValue.attrib[metaTag])
                        elif xValue.tag == "scene":
                            for xScene in xValue:
                                if xScene.tag == "character":
                                    bookItem.addSceneChar(xScene.text)
                                if xScene.tag == "plot":
                                    bookItem.addScenePlot(xScene.text)
                        else:
                            bookItem.setFromTag(xValue.tag,xValue.text)
                    self.theTree.appendItem(itemHandle,itemParent,itemOrder,bookItem)
        
        self.bookLoaded = True
        self.theTree.validateTree()
        self.theTree.sortTree()
        
        return
    
    def saveBook(self):
        """Saves the main project file holding all the items of the project listed in the project
        tree. The items are saved in the order generated by sort function in the BookTree class.
        Root item are saved first, then container items, and lastly the file items. For robustness,
        this function will save anything found in the BookItem objects in the tree.
        ToDo: Write to a temporary file and rename, rather than overwriting the current file."""
        
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
        
        # Root element and book details
        nwXML = ET.Element("novelWriterXML",attrib={
            "fileVersion" : "1.0",
            "appVersion"  : str(nw.__version__),
            "timeStamp"   : getTimeStamp("-"),
        })
        xBook = ET.SubElement(nwXML,"book")
        xBookTitle = ET.SubElement(xBook,"title")
        xBookTitle.text = self.bookTitle
        for bookAuthor in self.bookAuthors:
            if bookAuthor is None or bookAuthor == "": continue
            xBookAuthor = ET.SubElement(xBook,"author")
            xBookAuthor.text = bookAuthor
        
        # Save all items in the tree in their created order
        xContent = ET.SubElement(nwXML,"content",attrib={"count":str(len(self.theTree.theTree))})
        itemIdx  = 0
        for treeItem in self.theTree.theTree:
            
            itemHandle = str(treeItem["handle"])
            parHandle  = str(treeItem["parent"])
            itemOrder  = str(treeItem["order"])
            
            xItem = ET.SubElement(xContent,"item",attrib={
                "handle" : str(itemHandle),
                "parent" : str(parHandle),
                "order"  : str(itemOrder),
            })
            
            # Save the metadata of the file also in the project file
            # This means we don't need to load the file to list its wor count
            fileMeta = {}
            for metaTag in treeItem["entry"].validMeta:
                metaValue = treeItem["entry"].getFromTag(metaTag)
                if not metaValue is None:
                    fileMeta[metaTag] = str(metaValue)
            if len(fileMeta) > 0:
                xMeta = ET.SubElement(xItem,"meta",attrib=fileMeta)
            
            # Set all defined values (not None) in each item in the tree
            for entryTag in treeItem["entry"].validTags:
                entryValue = treeItem["entry"].getFromTag(entryTag)
                if not entryValue is None:
                    xValue = ET.SubElement(xItem,entryTag)
                    xValue.text = str(entryValue)
            
            # Set scene items
            if len(treeItem["entry"].sceneChars) + len(treeItem["entry"].scenePlots) > 0:
                xValue = ET.SubElement(xItem,"scene")
                for sceneChar in treeItem["entry"].sceneChars:
                    xScene = ET.SubElement(xValue,"character")
                    xScene.text = str(sceneChar)
                for scenePlot in treeItem["entry"].scenePlots:
                    xScene = ET.SubElement(xValue,"plot")
                    xScene.text = str(scenePlot)
            
            itemIdx += 1
        
        # Write the xml tree to file
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
        
        self.bookTitle  = "New Book"
        self.bookLoaded = True
        self.theTree.validateTree()
        self.theTree.sortTree()
        
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
