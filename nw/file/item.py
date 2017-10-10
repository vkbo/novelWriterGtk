# -*- coding: utf-8 -*
"""novelWriter Book Item

 novelWriter – Book Item
=========================
 A single entry in the book tree

 File History:
 Created: 2017-10-10 [0.4.0]

"""

import logging
import nw
import nw.const as NWC

from os      import path
from hashlib import sha256

logger = logging.getLogger(__name__)

class BookItem():
    
    validTags     = [
        "class","level","type","subtype",
        "title","name","comment",
        "role","number","compile","importance"
    ]
    validClasses  = ["CONTAINER","DOCUMENT"]
    validLevels   = ["ROOT","ITEM","FILE"]
    validTypes    = ["BOOK","CHAR","PLOT","NOTE"]
    validSubTypes = ["FRONTMATTER","PROLOGUE","CHAPTER","EPILOGUE","BACKMATTER"]
    
    itemClass      = None
    itemLevel      = None
    itemType       = None
    itemSubType    = None
    itemTitle      = None
    itemName       = None
    itemComment    = None
    itemRole       = None
    itemNumber     = None
    itemCompile    = None
    itemImportance = None
    
    def __init__(self):
        
        self.tagMap = {
            "class"      : self.setClass,
            "level"      : self.setLevel,
            "type"       : self.setType,
            "subtype"    : self.setSubType,
            "title"      : self.setTitle,
            "name"       : self.setName,
            "comment"    : self.setComment,
            "role"       : self.setRole,
            "number"     : self.setNumber,
            "compile"    : self.setCompile,
            "importance" : self.setImportance,
        }
        
        return
    
    def getFromTag(self,getTag):
        if getTag in self.validTags:
            if getTag == "class":      return self.itemClass
            if getTag == "level":      return self.itemLevel
            if getTag == "type":       return self.itemType
            if getTag == "subtype":    return self.itemSubType
            if getTag == "title":      return self.itemTitle
            if getTag == "name":       return self.itemName
            if getTag == "comment":    return self.itemComment
            if getTag == "role":       return self.itemRole
            if getTag == "number":     return self.itemNumber
            if getTag == "compile":    return self.itemCompile
            if getTag == "importance": return self.itemImportance
        else:
            logger.error("Unknown tag '%s'" % setTag)
        return
    
    def setFromTag(self,setTag,newValue):
        if setTag in self.validTags:
            self.tagMap[setTag](newValue)
        else:
            logger.error("Unknown tag '%s'" % setTag)
        return
    
    def setClass(self,newClass):
        if not isinstance(newClass,str):
            logger.error("itemClass: Wrong type, expected string")
            return
        if newClass.upper() in self.validClasses:
            self.itemClass = newClass.upper()
        else:
            logger.error("itemClass: Invalid class '%s'" % newClass)
        return
    
    def setLevel(self,newLevel):
        if not isinstance(newLevel,str):
            logger.error("itemLevel: Wrong type, expected string")
            return
        if newLevel.upper() in self.validLevels:
            self.itemLevel = newLevel.upper()
        else:
            logger.error("itemLevel: Invalid level '%s'" % newLevel)
        return
    
    def setType(self,newType):
        if not isinstance(newType,str):
            logger.error("itemType: Wrong type, expected string")
            return
        if newType.upper() in self.validTypes:
            self.itemType = newType.upper()
        else:
            logger.error("itemType: Invalid type '%s'" % newType)
        return
    
    def setSubType(self,newSubType):
        if not isinstance(newSubType,str):
            logger.error("itemSubType: Wrong type, expected string")
            return
        if newSubType.upper() in self.validSubTypes:
            self.itemSubType = newSubType.upper()
        else:
            logger.error("itemSubType: Invalid subtype '%s'" % newSubType)
        return
    
    def setTitle(self,newTitle):
        if newTitle is None:
            self.itemTitle = None
        else:
            try:
                self.itemTitle = str(newTitle).strip()
            except:
                self.itemTitle = "New Title"
                logger.error("itemTitle: Failed to set title")
        return
    
    def setName(self,newName):
        if newName is None:
            self.itemName = None
        else:
            try:
                self.itemName = str(newName).strip()
            except:
                logger.error("itemName: Failed to set name")
                return
        return
    
    def setComment(self,newComment):
        if newComment is None:
            self.itemComment = None
        else:
            try:
                self.itemComment = str(newComment).strip()
            except:
                logger.error("itemComment: Failed to set comment")
                return
        return
    
    def setRole(self,newRole):
        if newRole is None:
            self.itemRole = None
        else:
            try:
                self.itemRole = str(newRole).strip()
            except:
                logger.error("itemRole: Failed to set role")
                return
        return
    
    def setNumber(self,newNumber):
        if newNumber is None:
            self.itemNumber = None
        else:
            try:
                intValue = int(newNumber)
                if intValue < 0: intValue = 0
                self.itemNumber = intValue
            except:
                logger.error("itemNumber: Failed to set number")
                return
        return
    
    def setImportance(self,newImportance):
        if newImportance is None:
            self.itemImportance = None
        else:
            try:
                intValue = int(newImportance)
                if intValue < 1: intValue = 1
                if intValue > 5: intValue = 5
                self.itemImportance = intValue
            except:
                logger.error("itemImportance: Failed to set importance")
                return
        return
    
    def setCompile(self,newCompile):
        if isinstance(newCompile,bool):
            self.itemCompile = newCompile
        elif isinstance(newCompile,str):
            if newCompile.lower() == "false":
                self.itemCompile = False
            elif newCompile.lower() == "true":
                self.itemCompile = True
            else:
                self.itemCompile = False
        else:
            self.itemCompile = False
        return
    
# End Class BookItem
