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

from os      import path
from hashlib import sha256

logger = logging.getLogger(__name__)

class BookItem():
    
    TAG_CLASS   = "class"
    TAG_LEVEL   = "level"
    TAG_TYPE    = "type"
    TAG_SUBTYPE = "subtype"
    TAG_TITLE   = "title"
    TAG_NAME    = "name"
    TAG_COMMENT = "comment"
    TAG_ROLE    = "role"
    TAG_NUMBER  = "number"
    TAG_COMPILE = "compile"
    TAG_IMPORT  = "importance"
    
    META_PARS   = "parcount"
    META_SENTS  = "sentcount"
    META_WORDS  = "wordcount"
    META_CHARS  = "charcount"
    
    CLS_CONT    = "CONTAINER"
    CLS_SCENE   = "SCENE"
    CLS_NOTE    = "NOTE"
    
    LEV_ROOT    = "ROOT"
    LEV_ITEM    = "ITEM"
    LEV_FILE    = "FILE"
    
    TYP_BOOK    = "BOOK"
    TYP_CHAR    = "CHAR"
    TYP_PLOT    = "PLOT"
    TYP_NOTE    = "NOTE"
    
    SUB_FRONT   = "FRONTMATTER"
    SUB_PRO     = "PROLOGUE"
    SUB_CHAP    = "CHAPTER"
    SUB_EPI     = "EPILOGUE"
    SUB_BACK    = "BACKMATTER"
    
    validTags = [
        TAG_CLASS, TAG_LEVEL,  TAG_TYPE,    TAG_SUBTYPE,
        TAG_TITLE, TAG_NAME,   TAG_COMMENT,
        TAG_ROLE,  TAG_NUMBER, TAG_COMPILE, TAG_IMPORT
    ]
    validMeta      = [META_PARS,META_SENTS,META_WORDS,META_CHARS]
    validClasses   = [CLS_CONT,CLS_SCENE,CLS_NOTE]
    validLevels    = [LEV_ROOT,LEV_ITEM,LEV_FILE]
    validTypes     = [TYP_BOOK,TYP_CHAR,TYP_PLOT,TYP_NOTE]
    validSubTypes  = [SUB_FRONT,SUB_PRO,SUB_CHAP,SUB_EPI,SUB_BACK]
    
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
    
    metaParCount   = None
    metaSentCount  = None
    metaWordCount  = None
    metaCharCount  = None
    
    def __init__(self):
        
        self.tagMap = {
            self.TAG_CLASS   : self.setClass,
            self.TAG_LEVEL   : self.setLevel,
            self.TAG_TYPE    : self.setType,
            self.TAG_SUBTYPE : self.setSubType,
            self.TAG_TITLE   : self.setTitle,
            self.TAG_NAME    : self.setName,
            self.TAG_COMMENT : self.setComment,
            self.TAG_ROLE    : self.setRole,
            self.TAG_NUMBER  : self.setNumber,
            self.TAG_COMPILE : self.setCompile,
            self.TAG_IMPORT  : self.setImportance,
            self.META_PARS   : self.setParCount,
            self.META_SENTS  : self.setSentCount,
            self.META_WORDS  : self.setWordCount,
            self.META_CHARS  : self.setCharCount,
        }
        
        return
    
    def getFromTag(self,getTag):
        if getTag in self.validTags:
            if getTag == self.TAG_CLASS:   return self.itemClass
            if getTag == self.TAG_LEVEL:   return self.itemLevel
            if getTag == self.TAG_TYPE:    return self.itemType
            if getTag == self.TAG_SUBTYPE: return self.itemSubType
            if getTag == self.TAG_TITLE:   return self.itemTitle
            if getTag == self.TAG_NAME:    return self.itemName
            if getTag == self.TAG_COMMENT: return self.itemComment
            if getTag == self.TAG_ROLE:    return self.itemRole
            if getTag == self.TAG_NUMBER:  return self.itemNumber
            if getTag == self.TAG_COMPILE: return self.itemCompile
            if getTag == self.TAG_IMPORT:  return self.itemImportance
        elif getTag in self.validMeta:
            if getTag == self.META_PARS:   return self.metaParCount
            if getTag == self.META_SENTS:  return self.metaSentCount
            if getTag == self.META_WORDS:  return self.metaWordCount
            if getTag == self.META_CHARS:  return self.metaCharCount
        else:
            logger.error("Unknown tag '%s'" % setTag)
        return
    
    def setFromTag(self,setTag,newValue):
        if setTag in self.validTags:
            self.tagMap[setTag](newValue)
        elif setTag in self.validMeta:
            self.tagMap[setTag](newValue)
        else:
            logger.error("Unknown tag '%s'" % setTag)
        return
    
    def setCounts(self,newCounts):
        if len(newCounts) > 0: self.setParCount(newCounts[0])
        if len(newCounts) > 1: self.setSentCount(newCounts[1])
        if len(newCounts) > 2: self.setWordCount(newCounts[2])
        if len(newCounts) > 3: self.setCharCount(newCounts[3])
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
    
    def setParCount(self,newCount):
        if isinstance(newCount,int):
            if newCount >= 0: self.metaParCount = newCount
        elif isinstance(newCount,str):
            try:
                self.metaParCount = int(newCount)
            except:
                return
        return
    
    def setSentCount(self,newCount):
        if isinstance(newCount,int):
            if newCount >= 0: self.metaSentCount = newCount
        elif isinstance(newCount,str):
            try:
                self.metaSentCount = int(newCount)
            except:
                return
        return
    
    def setWordCount(self,newCount):
        if isinstance(newCount,int):
            if newCount >= 0: self.metaWordCount = newCount
        elif isinstance(newCount,str):
            try:
                self.metaWordCount = int(newCount)
            except:
                return
        return
    
    def setCharCount(self,newCount):
        if isinstance(newCount,int):
            if newCount >= 0: self.metaCharCount = newCount
        elif isinstance(newCount,str):
            try:
                self.metaCharCount = int(newCount)
            except:
                return
        return
    
    
# End Class BookItem
