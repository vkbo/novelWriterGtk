# -*- coding: utf-8 -*
"""novelWriter Document File

 novelWriter – Document File
=============================
 Manages a single document

 File History:
 Created: 2017-10-06 [0.4.0]

"""

import logging
import nw
import gi
gi.require_version("Gtk","3.0")

from gi.repository import Gtk

logger = logging.getLogger(__name__)

class DocFile():
    
    def __init__(self, docPath, docSlug):
        
        self.docPath    = docPath
        self.docSlug    = docSlug
        
        self.textBuffer = None
        self.noteBuffer = None
        
        return
    
    def openDocument(self):
        
        self.textBuffer = Gtk.TextBuffer()
        
        return

# End Class DocFile
