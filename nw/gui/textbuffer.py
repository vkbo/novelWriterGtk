# -*- coding: utf-8 -*
"""novelWriter TextBuffer

 novelWriter – TextBuffer
==========================
 A wrapper for the GtkSource.Buffer

 File History:
 Created: 2017-10-15 [0.4.0]

"""

import logging
import nw
import gi
gi.require_version("GtkSource","3.0")

from gi.repository import GtkSource, Pango

logger = logging.getLogger(__name__)

class NWTextBuffer(GtkSource.Buffer):
    
    def __init__(self):
        
        GtkSource.Buffer.__init__(self)
        
        # Create Tags
        self.tagBold   = self.create_tag("nwBold",weight=Pango.Weight.BOLD)
        self.tagItalic = self.create_tag("nwItalic",style=Pango.Style.ITALIC)
        self.tagMark   = self.create_tag("nwMark",underline=Pango.Underline.SINGLE)
        self.tagStrike = self.create_tag("nwStrike",strikethrough=True,foreground="#aa0000")
        
        self.mapEnc = {
            "nwBold"   : ["strong", self.tagBold],
            "nwItalic" : ["em",     self.tagItalic],
            "nwMark"   : ["mark",   self.tagMark],
            "nwStrike" : ["strike", self.tagStrike],
        }
        
        self.mapDec = {
            "strong" : ["nwBold",   self.tagBold],
            "em"     : ["nwItalic", self.tagItalic],
            "mark"   : ["nwMark",   self.tagMark],
            "strike" : ["nwStrike", self.tagStrike],
        }
        
        return
    
    def getCursorIter(self):
        """Returns the Gtk.TextIter of the cursor
        """
        currMark = self.get_insert()
        currIter = self.get_iter_at_mark(currMark)
        return currIter
    
    def toggleStyle(self, styleTag):
        """Toggles the style of the selected text or the word
        where the cursor is positioned.
        """
        
        currIter  = self.getCursorIter()
        selBounds = self.get_selection_bounds()
        
        if len(selBounds) != 0:
            selStart, selEnd = selBounds
        elif currIter.inside_word():
            selStart = currIter.copy()
            selEnd   = currIter.copy()
            selStart.backward_word_start()
            selEnd.forward_word_end()
        else:
            return
        
        if selStart.has_tag(styleTag):
            self.remove_tag(styleTag,selStart,selEnd)
        else:
            self.apply_tag(styleTag,selStart,selEnd)
        
        return
    
    #
    # Encode and Decode the Buffer
    #
    
    def encodeText(self, getBounds=None):
        
        logger.verbose("Beginning encoding of text buffer")
        
        if getBounds is None:
            itStart, itEnd = self.get_bounds()
        else:
            itStart, itEnd = getBounds
        
        parText   = []
        textCount = [0,0,0]
        
        tagState = {}
        for tagKey in self.mapEnc.keys():
            tagState[tagKey] = False
        
        parBuffer = ""
        tagStack  = []
        itCurr    = itStart.copy()
        while True:
            # If a new tag is started, add the tag state to the stack
            # and insert the html tag.
            if itCurr.starts_tag():
                for startTag in itCurr.get_tags():
                    tagName = startTag.get_property("name")
                    if not tagName in self.mapEnc.keys():
                        logger.vverbose("Skipping non-nw tag in buffer")
                        continue
                    tagHtml = self.mapEnc[tagName][0]
                    if not tagName in tagStack:
                        tagStack.append(tagName)
                        parBuffer += "<%s>" % tagHtml
                        logger.vverbose("Tags += %-8s : [%s]" % (tagName,", ".join(tagStack)))
            
            # Iterate through all opened tags in reverse order, and check if
            # they have been closed. If so, add the html close tag and pop
            # the tag from the stack
            revStack = tagStack.copy()
            for tagName in reversed(revStack):
                if itCurr.ends_tag(self.mapEnc[tagName][1]):
                    tagHtml = self.mapEnc[tagName][0]
                    parBuffer += "</%s>" % tagHtml
                    if tagName in tagStack:
                        tagStack.remove(tagName)
                        logger.vverbose("Tags -= %-8s : [%s]" % (tagName,", ".join(tagStack)))
            revStack = []
            
            char = itCurr.get_char()
            if char == "<": char = "&lt;"
            if char == ">": char = "&gt;"
            parBuffer += char
            
            # If at the end of a line, close all open tags, save the buffer
            # as a new paragraph, reset the buffer and re-open all tags in
            # the stack
            if itCurr.ends_line() or itCurr.is_end():
                textCount[0] += 1
                parBuffer = parBuffer.rstrip("\n")
                if len(tagStack) > 0:
                    for tagName in reversed(tagStack):
                        tagHtml = self.mapEnc[tagName][0]
                        parBuffer += "</%s>" % tagHtml
                parText.append(parBuffer)
                
                parBuffer = ""
                if len(tagStack) > 0:
                    for tagName in tagStack:
                        tagHtml = self.mapEnc[tagName][0]
                        parBuffer += "<%s>" % tagHtml
            
            if itCurr.ends_sentence(): textCount[1] += 1
            if itCurr.ends_word():     textCount[2] += 1
            
            if itCurr.is_end():
                break
            else:
                itCurr.forward_char()
        
        logger.vverbose("Length of tag stack is %d" % len(tagStack))
        logger.verbose("Encoded buffer with %d paragraphs, %d sentences and %d words" % (
            tuple(textCount)
        ))
        
        return parText, textCount
    
    def decodeText(self, parText):
        
        logger.verbose("Beginning decoding of text buffer")
        
        validOpen  = []
        validClose = []
        for nwTag in self.mapDec.keys():
            validOpen.append("<%s>" % nwTag)
            validClose.append("</%s>" % nwTag)
        
        self.set_max_undo_levels(0)
        itStart, itEnd = self.get_bounds()
        self.delete(itStart,itEnd)
        
        parCount = 0
        for parItem in parText:
            parStack  = []
            stackItem = ""
            for char in parItem:
                if char == "<":
                    parStack.append(stackItem)
                    stackItem = char
                elif char == ">":
                    parStack.append(stackItem+char)
                    stackItem = ""
                else:
                    stackItem += char
            parStack.append(stackItem)
            
            tagStack = []
            for stackItem in parStack:
                itemType = 0
                if len(stackItem) > 2:
                    if stackItem[0:2] == "</":
                        itemType = 2
                    elif stackItem[0] == "<":
                        itemType = 1
                
                if itemType == 1:
                    if not stackItem in validOpen: continue
                    tagHtml = stackItem[1:-1].lower()
                    if not tagHtml in self.mapDec.keys():
                        logger.warning("BUG: Some inconsistency in tag names, got %s" % tagHtml)
                        continue
                    tagName = self.mapDec[tagHtml][0]
                    if not tagName in tagStack:
                        tagStack.append(tagName)
                        logger.vverbose("Tags += %-8s : [%s]" % (tagName,", ".join(tagStack)))
                    
                elif itemType == 2:
                    if not stackItem in validClose: continue
                    tagHtml = stackItem[2:-1].lower()
                    if not tagHtml in self.mapDec.keys():
                        logger.warning("BUG: Some inconsistency in tag names, got %s" % tagHtml)
                        continue
                    tagName = self.mapDec[tagHtml][0]
                    if tagName in tagStack:
                        tagStack.remove(tagName)
                        logger.vverbose("Tags -= %-8s : [%s]" % (tagName,", ".join(tagStack)))
                    
                else:
                    itStart, itEnd = self.get_bounds()
                    stackItem = stackItem.replace("&lt;","<")
                    stackItem = stackItem.replace("&gt;",">")
                    if len(tagStack) == 0:
                        self.insert(itEnd,stackItem)
                    else:
                        self.insert_with_tags_by_name(itEnd,stackItem,*tagStack)
                    
            parCount += 1
            if parCount < len(parText):
                itStart, itEnd = self.get_bounds()
                self.insert(itEnd,"\n")
            
        self.set_max_undo_levels(100)
        logger.vverbose("Length of tag stack is %d" % len(tagStack))
        
        return
    
# End Class NWTextBuffer
