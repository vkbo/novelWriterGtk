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
from itertools    import chain
from nw.file.item import BookItem
from nw.file.doc  import DocFile

logger = logging.getLogger(__name__)

class BookTree():
    
    ORD_UP    = 0
    ORD_DOWN  = 1
    ORD_NUP   = 2
    ORD_NDOWN = 3
    
    validOrder = [ORD_UP,ORD_DOWN,ORD_NUP,ORD_NDOWN]
    
    def __init__(self):
        
        self.docPath    = None
        self.theTree    = []
        self.treeLookup = {}
        self.parOfItems = {}
        self.parOfFiles = {}
        self.treeOrder  = []
        
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
        self.parOfItems = {}
        self.parOfFiles = {}
        self.treeOrder  = []
        
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
            logger.debug("BookTree: Entry is not a container, getting its parent")
            parParent = self.getItem(pHandle)["parent"]
            if not parParent is None:
                pHandle  = parParent
                parEntry = self.getItem(pHandle)["entry"]
                parClass = parEntry.itemClass
                parType  = parEntry.itemType
            else:
                logger.error("BookTree: A file must be added to a folder")
        
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
        
        self.appendItem(None,pHandle,None,newItem)
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
        
        self.appendItem(None,self.fixedItems[BookItem.TYP_BOOK],None,newItem)
        self.sortTree()
        
        return
    
    def addCharacter(self):
        
        newItem = BookItem()
        newItem.setClass(BookItem.CLS_CONT)
        newItem.setLevel(BookItem.LEV_ITEM)
        newItem.setType(BookItem.TYP_CHAR)
        newItem.setName("New Character")
        
        self.appendItem(None,self.fixedItems[BookItem.TYP_CHAR],None,newItem)
        self.sortTree()
        
        return
    
    def addPlot(self):
        
        newItem = BookItem()
        newItem.setClass(BookItem.CLS_CONT)
        newItem.setLevel(BookItem.LEV_ITEM)
        newItem.setType(BookItem.TYP_PLOT)
        newItem.setName("New Plot")
        
        self.appendItem(None,self.fixedItems[BookItem.TYP_PLOT],None,newItem)
        self.sortTree()
        
        return
    
    #
    # Tree Item Maintenance
    #
    
    def updateItem(self, itemHandle, tTag, tValue):
        self.theTree[self.treeLookup[itemHandle]]["entry"].setFromTag(tTag,tValue)
        return
    
    def getItem(self, itemHandle):
        return self.theTree[self.treeLookup[itemHandle]]
    
    def changeOrder(self, itemHandle, moveIt):
        
        treeItem   = self.getItem(itemHandle)
        itemParent = treeItem["parent"]
        itemEntry  = treeItem["entry"]
        
        if itemEntry.itemLevel == BookItem.LEV_FILE:
            currList = self.parOfFiles[itemParent]
        elif itemEntry.itemLevel == BookItem.LEV_ITEM:
            currList = self.parOfItems[itemParent]
        else:
            logger.error("BookTree: Cannot change order of ROOT elements")
            return
        
        if moveIt not in self.validOrder:
            logger.error("BUG: Unknown ordering requested")
            return
        
        if itemHandle not in currList:
            logger.error("BUG: Cannot change order of %s, as it is not where it should be" % itemHandle)
            return
        
        # If move withing parent, just swap the indices, and refresh the master index
        if moveIt == self.ORD_UP or moveIt == self.ORD_DOWN:
            
            currIndex = currList.index(itemHandle)
            
            if moveIt == self.ORD_UP:
                newIndex = currIndex - 1
            elif moveIt == self.ORD_DOWN:
                newIndex = currIndex + 1
            
            if newIndex < 0 or newIndex >= len(currList): return
            
            currList[currIndex], currList[newIndex] = currList[newIndex], currList[currIndex]
            
            if itemEntry.itemLevel == BookItem.LEV_FILE:
                self.parOfFiles[itemParent] = currList
            elif itemEntry.itemLevel == BookItem.LEV_ITEM:
                self.parOfItems[itemParent] = currList
            
            self.buildTreeOrder()
            self.updateEntryOrder()
        
        # If moving to a new node, update parent and set order to None
        elif moveIt == self.ORD_NUP or moveIt == self.ORD_NDOWN:
            
            # This is only allowed for FILE entries
            if itemEntry.itemLevel == BookItem.LEV_ITEM: return
            
            treeParent = self.getItem(itemParent)
            parParent  = treeParent["parent"]
            parEntry   = treeParent["entry"]
            
            if parParent is not None:
                # Move to next or previous node
                parList = self.parOfItems[parParent]
                if itemParent not in parList:
                    logger.error("BUG: Something unexpected happened while moving entry")
                    return
                parIndex = parList.index(itemParent)
                if moveIt == self.ORD_NUP:
                    newIndex = parIndex - 1
                elif moveIt == self.ORD_NDOWN:
                    newIndex = parIndex + 1
                
                if newIndex < 0 or newIndex >= len(parList):
                    self.theTree[self.treeLookup[itemHandle]]["parent"] = parParent
                    self.sortTree()
                else:
                    self.theTree[self.treeLookup[itemHandle]]["parent"] = parList[newIndex]
                    self.sortTree()
            else:
                # Move to last child node
                parList = self.parOfItems[itemParent]
                self.theTree[self.treeLookup[itemHandle]]["parent"] = parList[len(parList)-1]
                self.sortTree()
            
        return
    
    def createRootItem(self, rootType):
        
        if rootType in BookItem.validTypes:
            if rootType == BookItem.TYP_BOOK: rootName = "Book"
            if rootType == BookItem.TYP_CHAR: rootName = "Characters"
            if rootType == BookItem.TYP_PLOT: rootName = "Plots"
            if rootType == BookItem.TYP_NOTE: rootName = "Notes"
        else:
            logger.error("BookTree: Cannot create root item of type '%s'" % str(rootType))
            return
        
        if self.fixedItems[rootType] is not None:
            logger.warning("BookTree: Root item already exists")
            return
        
        rootHandle = self.makeHandle()
        rootItem   = BookItem()
        rootItem.setClass(BookItem.CLS_CONT)
        rootItem.setLevel(BookItem.LEV_ROOT)
        rootItem.setType(rootType)
        rootItem.setName(rootName)
        
        logger.info("BookTree: Creating root item '%s' with handle %s" % (rootName, rootHandle))
        
        self.appendItem(rootHandle,None,None,rootItem)
        self.fixedItems[rootType] = rootHandle
        
        return
    
    def appendItem(self, tHandle, pHandle, tOrder, bookItem):
        """
        Appends an entry to the main project tree.
        """
        
        tHandle = self.checkString(tHandle,self.makeHandle(),False)
        pHandle = self.checkString(pHandle,None,True)
        tOrder  = self.checkInt(tOrder,None,True)
        
        logger.verbose("BookTree: Adding entry %s with parent %s" % (str(tHandle),str(pHandle)))
        
        if bookItem.itemLevel == BookItem.LEV_FILE:
            docItem = DocFile(self.docPath,tHandle,bookItem.itemClass)
        else:
            docItem = None
        
        self.theTree.append({
            "handle" : tHandle,
            "parent" : pHandle,
            "order"  : tOrder,
            "entry"  : bookItem,
            "doc"    : docItem,
        })
        lastIdx = len(self.theTree)-1
        self.treeLookup[tHandle] = lastIdx
        
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
            logger.verbose("BookTree: Checking ROOT with handle %s" % itemHandle)
            
            if itemParent is not None:
                self.theTree[itemIdx]["parent"] = None
                logger.warning("BookTree: Parent was set for ROOT element %s" % itemHandle)
                errCount += 1
            
            for itemType in BookItem.validTypes:
                if bookEntry.itemType == itemType:
                    if self.fixedItems[itemType] is None:
                        self.fixedItems[itemType] = itemHandle
                        logger.debug("BookTree: Root handle for type %s set to %s" % (itemType,itemHandle))
                    else:
                        logger.warning("BookTree: Encountered a second ROOT of type %s with handle %s" % (itemType,itemHandle))
                        errCount += 1
        
        for rootType in self.fixedItems.keys():
            if self.fixedItems[rootType] is None:
                logger.info("BookTree: Root item missing, creating it")
                self.createRootItem(rootType)
        
        # Checking ITEM level
        for treeItem in self.theTree:
            
            itemHandle = treeItem["handle"]
            itemParent = treeItem["parent"]
            bookEntry  = treeItem["entry"]
            itemIdx    = self.treeLookup[itemHandle]
            hasError   = False
            
            if not bookEntry.itemLevel == BookItem.LEV_ITEM: continue
            logger.verbose("BookTree: Checking ITEM with handle %s" % itemHandle)
            
            for itemType in BookItem.validTypes:
                if bookEntry.itemType == itemType:
                    if itemParent is None:
                        logger.warning("BookTree: Parent was missing for ITEM of type %s with handle %s" % (itemType,itemHandle))
                        self.theTree[itemIdx]["parent"] = self.fixedItems[itemType]
                        errCount += 1
        
        logger.info("BookTree: Found %d error(s) while parsing the project tree" % errCount)
        
        return
    
    def sortTree(self):
        
        # Resetting Indices
        self.parOfItems = {}
        self.parOfFiles = {}
        
        treeOrder = []
        logger.debug("TreeSort: Reading previous order")
        tempOrder = [None] * len(self.theTree)
        for treeItem in self.theTree:
            itemHandle = treeItem["handle"]
            itemOrder  = treeItem["order"]
            itemName   = treeItem["entry"].itemName
            if itemOrder is not None and isinstance(itemOrder,int):
                if tempOrder[itemOrder] is None:
                    tempOrder[itemOrder] = itemHandle
                    logger.vverbose("TreeSort: Entry '%s' %s has order %s" % (
                        str(itemName), str(itemHandle), str(itemOrder)
                    ))
                else:
                    tempOrder.append(itemHandle)
                    logger.vverbose("TreeSort: Entry '%s' %s has no order, appending" % (
                        str(itemName), str(itemHandle)
                    ))
            else:
                tempOrder.append(itemHandle)
                logger.vverbose("TreeSort: Entry '%s' %s has no order, appending" % (
                    str(itemName), str(itemHandle)
                ))
        for tempItem in tempOrder:
            if tempItem is not None: treeOrder.append(tempItem)
        
        # Scanning ROOT level
        logger.debug("TreeSort: Sorting ROOT entries")
        for rootType in self.fixedOrder:
            itemHandle = self.fixedItems[rootType]
            self.parOfItems[itemHandle] = []
            self.parOfFiles[itemHandle] = []
        
        # Scanning ITEM level
        logger.debug("TreeSort: Sorting ITEM entries")
        for itemHandle in treeOrder:
            
            itemIdx    = self.treeLookup[itemHandle]
            treeItem   = self.theTree[itemIdx]
            
            itemHandle = treeItem["handle"]
            itemParent = treeItem["parent"]
            bookEntry  = treeItem["entry"]
            
            if not bookEntry.itemLevel == BookItem.LEV_ITEM: continue
            
            if itemParent in self.parOfItems.keys():
                self.parOfItems[itemParent].append(itemHandle)
                logger.vverbose("TreeSort: ITEM '%s' %s appended to %s" % (
                    bookEntry.itemName, str(itemHandle), str(itemParent)
                ))
                self.parOfFiles[itemHandle] = []
            else:
                logger.warning("BUG: itemParent %s not found in itemParent" % itemParent)
        
        # Scanning FILE level
        logger.verbose("TreeSort: Sorting FILE entries")
        for itemHandle in treeOrder:
            
            itemIdx    = self.treeLookup[itemHandle]
            treeItem   = self.theTree[itemIdx]
            
            itemHandle = treeItem["handle"]
            itemParent = treeItem["parent"]
            bookEntry  = treeItem["entry"]
            
            if not bookEntry.itemLevel == BookItem.LEV_FILE: continue
            
            if itemParent in self.parOfFiles.keys():
                self.parOfFiles[itemParent].append(itemHandle)
                logger.vverbose("TreeSort: FILE '%s' %s appended to %s" % (
                    bookEntry.itemName, str(itemHandle), str(itemParent)
                ))
            else:
                logger.warning("BUG: itemParent %s not found in fileParent" % itemParent)
        
        self.buildTreeOrder()
        self.updateEntryOrder()
        
        return
    
    def buildTreeOrder(self):
        
        # Resetting Indices
        self.treeOrder = []
        
        rootOrder = []
        itemOrder = []
        fileOrder = []
        
        for rootType in self.fixedOrder:
            itemHandle = self.fixedItems[rootType]
            rootOrder.append(itemHandle)
        
        logger.debug("TreeSort: %d ROOT entries added to index" % len(rootOrder))
        
        for itemParent in rootOrder:
            itemOrder += self.parOfItems[itemParent]
        
        logger.debug("TreeSort: %d ITEM entries added to index" % len(itemOrder))
        
        for itemParent in chain(rootOrder,itemOrder):
            fileOrder += self.parOfFiles[itemParent]
        
        logger.debug("TreeSort: %d FILE entries added to index" % len(fileOrder))
        
        errCount = 0
        logger.debug("TreeSort: Assempling index, and checking for consistency")
        self.treeOrder = rootOrder + itemOrder + fileOrder
        for itemHandle in self.treeLookup.keys():
            if itemHandle not in self.treeOrder:
                logger.warning("BUG: Handle %s not in index" % itemHandle)
                errCount += 1
        if errCount == 0:
            logger.debug("TreeSort: Index is consistent")
        else:
            logger.warning("BUG: %d errors found in the index" % errCount)
            
        uniqueSet = set(self.treeOrder)
        if len(uniqueSet) == len(self.treeOrder):
            logger.debug("TreeSort: No duplicates found in index")
            
        return
    
    def updateEntryOrder(self):
        
        logger.debug("TreeSort: Setting order parameter of tree entries")
        for itemOrder in range(len(self.treeOrder)):
            itemHandle = self.treeOrder[itemOrder]
            itemIdx    = self.treeLookup[itemHandle]
            self.theTree[itemIdx]["order"] = itemOrder
            logger.vverbose("TreeSort: Setting '%s' %s to order %d" % (
                str(self.theTree[itemIdx]["entry"].itemName), itemHandle, itemOrder
            ))
        
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
            logger.warning("BookTree: Duplicate handle encountered! Retrying ...")
            itemHandle = self.makeHandle(seed+"!")
        return itemHandle
    
    def checkString(self,checkValue,defaultValue,allowNone=False):
        if allowNone:
            if checkValue == None:   return None
            if checkValue == "None": return None
        if isinstance(checkValue,str): return str(checkValue)
        return defaultValue
    
    def checkInt(self,checkValue,defaultValue,allowNone=False):
        if allowNone:
            if checkValue == None:   return None
            if checkValue == "None": return None
        try:
            return int(checkValue)
        except:
            return defaultValue
    
# End Class BookTree
