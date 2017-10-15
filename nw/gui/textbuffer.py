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
        self.tagStrike = self.create_tag("nwStrike",strikethrough=True)
        
        self.mapTags = {
            "nwBold"   : ["strong", self.tagBold],
            "nwItalic" : ["emph",   self.tagItalic],
            "nwMark"   : ["mark",   self.tagMark],
            "nwStrike" : ["strike", self.tagStrike],
        }
        
        return
    
    def encodeText(self, getBounds=None):
        
        if getBounds is None:
            itStart, itEnd = self.get_bounds()
        else:
            itStart, itEnd = getBounds
        
        parText   = []
        textCount = [0,0,0]
        
        tagState = {}
        for tagKey in self.mapTags.keys():
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
                    if not tagName in self.mapTags.keys():
                        logger.vverbose("Skipping non-nw tag in buffer")
                        continue
                    tagHtml = self.mapTags[tagName][0]
                    if not tagName in tagStack:
                        tagStack.append(tagName)
                        parBuffer += "<%s>" % tagHtml
                        logger.vverbose("Tags: %s" % (", ".join(tagStack)))
            
            parBuffer += itCurr.get_char()
            
            # Iterate through all opened tags in reverse order, and check if
            # they have been closed. If so, add the html close tag and pop
            # the tag from the stack
            revStack = tagStack.copy()
            for tagName in reversed(revStack):
                if itCurr.ends_tag(self.mapTags[tagName][1]):
                    logger.vverbose("Tags: %s" % (", ".join(tagStack)))
                    tagHtml = self.mapTags[tagName][0]
                    parBuffer += "</%s>" % tagHtml
                    tagStack.remove(tagName)
            revStack = []
            
            # If at the end of a line, close all open tags, save the buffer
            # as a new paragraph, reset the buffer and re-open all tags in
            # the stack
            if itCurr.ends_line() or itCurr.is_end():
                textCount[0] += 1
                parBuffer = parBuffer.rstrip("\n")
                if len(tagStack) > 0:
                    for tagName in reversed(tagStack):
                        tagHtml = self.mapTags[tagName][0]
                        parBuffer += "</%s>" % tagHtml
                parText.append(parBuffer)
                
                parBuffer = ""
                if len(tagStack) > 0:
                    for tagName in tagStack:
                        tagHtml = self.mapTags[tagName][0]
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
    
# End Class NWTextBuffer
