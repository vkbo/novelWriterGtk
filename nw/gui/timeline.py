# -*- coding: utf-8 -*
"""novelWriter GUI TimeLine

 novelWriter – GUI TimeLine
============================
 Class holding the book time line view

 File History:
 Created: 2017-11-02 [0.4.0]

"""

import logging
import nw
import gi
gi.require_version("Gtk","3.0")

from gi.repository import Gtk
from nw.file.book  import BookItem

logger = logging.getLogger(__name__)

class GuiTimeLine(Gtk.Alignment):
    
    def __init__(self, theBook):
        
        Gtk.Alignment.__init__(self)
        
        self.theBook = theBook
        self.tblRows = []
        self.tblCols = []
        
        # Book Alignment
        self.set_name("alignTimeLine")
        self.set_padding(20,40,40,40)
        
        self.gridTL = Gtk.Grid()
        self.gridTL.set_name("gridTimeLine")
        self.gridTL.set_row_spacing(4)
        self.gridTL.set_column_spacing(12)
        self.add(self.gridTL)
        
        return
    
    def loadContent(self):
        
        self.tblRows = []
        self.tblCols = []
        
        tmpChars = []
        tmpPlots = []
        
        for treeHandle in self.theBook.theTree.treeOrder:
            
            treeItem   = self.theBook.getItem(treeHandle)
            
            itemHandle = treeItem["handle"]
            itemParent = treeItem["parent"]
            itemLevel  = treeItem["entry"].itemLevel
            itemClass  = treeItem["entry"].itemClass
            itemType   = treeItem["entry"].itemType
            
            if itemLevel == BookItem.LEV_ITEM:
                if itemType == BookItem.TYP_CHAR:
                    tmpChars.append({
                        "handle" : itemHandle,
                        "name"   : treeItem["entry"].itemName,
                    })
                elif itemType == BookItem.TYP_PLOT:
                    tmpPlots.append({
                        "handle" : itemHandle,
                        "name"   : treeItem["entry"].itemName,
                    })
            elif itemLevel == BookItem.LEV_FILE:
                if itemType == BookItem.TYP_BOOK:
                    treeParent  = self.theBook.getItem(itemParent)
                    itemSubType = treeParent["entry"].itemSubType
                    if itemSubType in (BookItem.SUB_PRO,BookItem.SUB_CHAP,BookItem.SUB_EPI):
                        self.tblCols.append({
                            "handle"    : itemHandle,
                            "name"      : treeItem["entry"].itemName,
                            "parhandle" : itemParent,
                            "partype"   : treeParent["entry"].itemSubType,
                            "parnum"    : treeParent["entry"].itemNumber,
                        })
        
        self.tblRows = tmpChars+tmpPlots
        self.buildGrid()
        self.show_all()
        
        return
    
    def buildGrid(self):
        
        self.gridTL.attach(Gtk.Label(""),0,0,1,1)
        self.gridTL.attach(Gtk.Label(""),0,1,1,1)
        
        rowNum = 2
        for rowItem in self.tblRows:
            tmpLabel = Gtk.Label(rowItem["name"])
            tmpLabel.set_xalign(1.0)
            self.gridTL.attach(tmpLabel,0,rowNum,1,1)
            rowNum += 1
        
        chapOrder = []
        chapName  = {}
        chapCount = {}
        currChap  = None
        scnCount  = 1
        colNum    = 1
        for colItem in self.tblCols:
            
            parHandle = colItem["parhandle"]
            
            if not colItem["parhandle"] == currChap:
                currChap = colItem["parhandle"]
                scnCount = 1
            else:
                scnCount += 1
            
            tmpLabel = Gtk.Label("SCN %d" % scnCount)
            tmpLabel.set_xalign(0.5)
            self.gridTL.attach(tmpLabel,colNum,1,1,1)
            colNum += 1
            
            chapCount[parHandle] = scnCount
            if parHandle not in chapOrder:
                chapOrder.append(parHandle)
            if colItem["partype"] == BookItem.SUB_CHAP:
                chapName[parHandle] = "%s %d" % (colItem["partype"],colItem["parnum"])
            else:
                chapName[parHandle] = "%s" % colItem["partype"]
        
        colNum = 1
        for parHandle in chapOrder:
            tmpLabel = Gtk.Label()
            tmpLabel.set_markup("<b>%s</b>" % chapName[parHandle])
            tmpLabel.set_xalign(0.5)
            self.gridTL.attach(tmpLabel,colNum,0,chapCount[parHandle],1)
            colNum += chapCount[parHandle]
        
        return
    
# End Class GuiTimeLine
