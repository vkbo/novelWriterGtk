# -*- coding: utf-8 -*
"""novelWriter Book Tree Class

 novelWriter – Book Tree Class
===============================
 Holds the tree of items and files of the book project

 File History:
 Created: 2017-10-18 [0.4.0]

"""

import logging
import nw

from os           import path
from time         import time
from hashlib      import sha256
from nw.file.item import BookItem
from nw.file.doc  import DocFile

logger = logging.getLogger(__name__)

class BookTree():
    
    def __init__(self):
        
        self.docPath    = None
        self.theTree    = []
        self.treeLookup = {}
        self.rootOrder  = []
        self.itemOrder  = []
        self.fileOrder  = []
        self.fullOrder  = []
        
        self.fixedOrder = [
            BookItem.TYP_BOOK,
            BookItem.TYP_CHAR,
            BookItem.TYP_PLOT,
            BookItem.TYP_NOTE,
        ]
        self.fixedItems = {
            BookItem.TYP_BOOK : None,
            BookItem.TYP_CHAR : None,
            BookItem.TYP_PLOT : None,
            BookItem.TYP_NOTE : None,
        }
        
        return
    
    def clearTree(self):
        
        self.docPath    = None
        self.theTree    = []
        self.treeLookup = {}
        self.rootOrder  = []
        self.itemOrder  = []
        self.fileOrder  = []
        self.fullOrder  = []
        
        self.fixedOrder = [
            BookItem.TYP_BOOK,
            BookItem.TYP_CHAR,
            BookItem.TYP_PLOT,
            BookItem.TYP_NOTE,
        ]
        self.fixedItems = {
            BookItem.TYP_BOOK : None,
            BookItem.TYP_CHAR : None,
            BookItem.TYP_PLOT : None,
            BookItem.TYP_NOTE : None,
        }
        
        return
    
    #
    # Add Elements to Main Tree
    #
    
    def addFile(self, pHandle):
        
        parEntry = self.getItem(pHandle)["entry"]
        parClass = parEntry.itemClass
        parType  = parEntry.itemType
        
        if not parClass == BookItem.CLS_CONT:
            logger.debug("Item is not a folder, getting its parent")
            parParent = self.getItem(pHandle)["parent"]
            if not parParent is None:
                pHandle  = parParent
                parEntry = self.getItem(pHandle)["entry"]
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
        
        self.appendItem(None,pHandle,newItem)
        self.sortTree()
        
        return
    
    def addChapter(self):
        
        newItem = BookItem()
        newItem.setClass(BookItem.CLS_CONT)
        newItem.setLevel(BookItem.LEV_ITEM)
        newItem.setType(BookItem.TYP_BOOK)
        newItem.setSubType(BookItem.SUB_CHAP)
        newItem.setName("New Chapter")
        newItem.setCompile(True)
        
        self.appendItem(None,self.fixedItems[BookItem.TYP_BOOK],newItem)
        self.sortTree()
        
        return
    
    def addCharacter(self):
        
        newItem = BookItem()
        newItem.setClass(BookItem.CLS_CONT)
        newItem.setLevel(BookItem.LEV_ITEM)
        newItem.setType(BookItem.TYP_CHAR)
        newItem.setName("New Character")
        
        self.appendItem(None,self.fixedItems[BookItem.TYP_CHAR],newItem)
        self.sortTree()
        
        return
    
    def addPlot(self):
        
        newItem = BookItem()
        newItem.setClass(BookItem.CLS_CONT)
        newItem.setLevel(BookItem.LEV_ITEM)
        newItem.setType(BookItem.TYP_PLOT)
        newItem.setName("New Plot")
        
        self.appendItem(None,self.fixedItems[BookItem.TYP_PLOT],newItem)
        self.sortTree()
        
        return
    
    #
    # Tree Item Maintenance
    #
    
    def updateItem(self, itemHandle, tTag, tValue):
        self.theTree[self.treeLookup[itemHandle]]["entry"].setFromTag(tTag,tValue.strip())
        return
    
    def getItem(self, itemHandle):
        return self.theTree[self.treeLookup[itemHandle]]
    
    def createRootItem(self, rootType):
        
        if rootType in BookItem.validTypes:
            if rootType == BookItem.TYP_BOOK: rootName = "Book"
            if rootType == BookItem.TYP_CHAR: rootName = "Characters"
            if rootType == BookItem.TYP_PLOT: rootName = "Plots"
            if rootType == BookItem.TYP_NOTE: rootName = "Notes"
        else:
            logger.error("Cannot create root item of type '%s'" % str(rootType))
            return
        
        if self.fixedItems[rootType] is not None:
            logger.warning("Root item already exists")
            return
        
        rootHandle = self.makeHandle()
        rootItem   = BookItem()
        rootItem.setClass(BookItem.CLS_CONT)
        rootItem.setLevel(BookItem.LEV_ROOT)
        rootItem.setType(rootType)
        rootItem.setName(rootName)
        
        logger.info("Creating root item '%s' with handle %s" % (rootName, rootHandle))
        
        self.appendItem(rootHandle,None,rootItem)
        self.fixedItems[rootType] = rootHandle
        
        return
    
    def appendItem(self, tHandle, pHandle, bookItem):
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
        self.treeLookup[tHandle] = lastIdx
        # self.lvlIndex[bookItem.itemLevel][tHandle] = lastIdx
        
        return
    
    def validateTree(self):
        
        errCount = 0
        
        # Checking ROOT level
        for treeItem in self.theTree:
            
            itemHandle = treeItem["handle"]
            itemParent = treeItem["parent"]
            bookEntry  = treeItem["entry"]
            itemIdx    = self.treeLookup[itemHandle]
            
            if not bookEntry.itemLevel == BookItem.LEV_ROOT: continue
            logger.verbose("Checking ROOT with handle %s" % itemHandle)
            
            if itemParent is not None:
                self.theTree[itemIdx]["parent"] = None
                logger.warning("Parent was set for ROOT element %s" % itemHandle)
                errCount += 1
            
            for itemType in BookItem.validTypes:
                if bookEntry.itemType == itemType:
                    if self.fixedItems[itemType] is None:
                        self.fixedItems[itemType] = itemHandle
                        logger.debug("Root handle for type %s set to %s" % (itemType,itemHandle))
                    else:
                        logger.warning("Encountered a second ROOT of type %s with handle %s" % (itemType,itemHandle))
                        errCount += 1
        
        for rootType in self.fixedItems.keys():
            if self.fixedItems[rootType] is None:
                logger.info("Root item missing, creating it")
                self.createRootItem(rootType)
        
        # Checking ITEM level
        for treeItem in self.theTree:
            
            itemHandle = treeItem["handle"]
            itemParent = treeItem["parent"]
            bookEntry  = treeItem["entry"]
            itemIdx    = self.treeLookup[itemHandle]
            hasError   = False
            
            if not bookEntry.itemLevel == BookItem.LEV_ITEM: continue
            logger.verbose("Checking ITEM with handle %s" % itemHandle)
            
            for itemType in BookItem.validTypes:
                if bookEntry.itemType == itemType:
                    if itemParent is None:
                        logger.warning("Parent was missing for ITEM of type %s with handle %s" % (itemType,itemHandle))
                        self.theTree[itemIdx]["parent"] = self.fixedItems[itemType]
                        errCount += 1
        
        logger.info("Found %d error(s) while parsing the project file" % errCount)
        
        return
    
    def sortTree(self):
        
        # Resetting Indices
        self.rootOrder = []
        self.itemOrder = []
        self.fileOrder = []
        self.fullOrder = []
        
        # Temporary Indices
        itemTemp = {}
        fileTemp = {}
        
        # Scanning ROOT level
        logger.debug("Sorting ROOT entries")
        for rootType in self.fixedOrder:
            itemHandle = self.fixedItems[rootType]
            self.rootOrder.append(itemHandle)
            itemTemp[itemHandle] = []
            fileTemp[itemHandle] = []
        
        logger.debug("%d ROOT entries added to index" % len(self.rootOrder))
        
        # Scanning ITEM level
        logger.debug("Sorting ITEM entries")
        for treeItem in self.theTree:
            
            itemHandle = treeItem["handle"]
            itemParent = treeItem["parent"]
            bookEntry  = treeItem["entry"]
            itemIdx    = self.treeLookup[itemHandle]
            
            if not bookEntry.itemLevel == BookItem.LEV_ITEM: continue
            
            if itemParent in itemTemp.keys():
                itemTemp[itemParent].append(itemHandle)
                fileTemp[itemHandle] = []
            else:
                logger.warning("BUG: itemParent %s not found in itemTemp" % itemParent)
        
        for itemParent in self.rootOrder:
            self.itemOrder += itemTemp[itemParent]
        
        logger.debug("%d ITEM entries added to index" % len(self.itemOrder))
            
        # Scanning FILE level
        logger.debug("Sorting FILE entries")
        for treeItem in self.theTree:
            
            itemHandle = treeItem["handle"]
            itemParent = treeItem["parent"]
            bookEntry  = treeItem["entry"]
            itemIdx    = self.treeLookup[itemHandle]
            
            if not bookEntry.itemLevel == BookItem.LEV_FILE: continue
            
            if itemParent in fileTemp.keys():
                fileTemp[itemParent].append(itemHandle)
            else:
                logger.warning("BUG: itemParent %s not found in fileTemp" % itemParent)
        
        for itemParent in self.rootOrder:
            self.fileOrder += fileTemp[itemParent]
        for itemParent in self.itemOrder:
            self.fileOrder += fileTemp[itemParent]
        
        logger.debug("%d FILE entries added to index" % len(self.fileOrder))
        
        # Checking Index
        errCount = 0
        logger.debug("Checking index for consistency")
        self.fullOrder = self.rootOrder + self.itemOrder + self.fileOrder
        for itemHandle in self.treeLookup.keys():
            if itemHandle not in self.fullOrder:
                logger.warning("BUG: Handle %s not in index" % itemHandle)
                errCount += 1
        if errCount == 0:
            logger.debug("Index is consistent")
        else:
            logger.warning("BUG: %d errors found in the index" % errCount)
            
        uniqueSet = set(self.fullOrder)
        if len(uniqueSet) == len(self.fullOrder):
            logger.debug("No duplicates found in index")
        
        return
    
    #
    # Setters and Getters
    #
    
    def setPath(self, docPath):
        self.docPath = docPath
        return
    
    #
    # Internal Functions
    #
    
    def makeHandle(self,seed=""):
        itemHandle = sha256((str(time())+seed).encode()).hexdigest()[0:13]
        if itemHandle in self.treeLookup.keys():
            logger.warning("Duplicate handle encountered! Retrying ...")
            itemHandle = self.makeHandle(seed+"!")
        return itemHandle
    
    def checkString(self,checkValue,defaultValue,allowNone=False):
        if allowNone:
            if checkValue == None:   return None
            if checkValue == "None": return None
        if isinstance(checkValue,str): return str(checkValue)
        return defaultValue
    
# End Class BookTree
