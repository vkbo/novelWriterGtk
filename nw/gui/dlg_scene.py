# -*- coding: utf-8 -*
"""novelWriter Scene Options

 novelWriter – Scene Options
=============================
 Dialog window to select characters and plots for a scene file

 File History:
 Created: 2017-10-26 [0.4.0]

"""

import logging
import nw
import gi
gi.require_version("Gtk","3.0")

from gi.repository import Gtk
from nw.file.book  import BookItem

logger = logging.getLogger(__name__)

class SceneOpt(Gtk.Dialog):
    
    def __init__(self):
        
        Gtk.Dialog.__init__(self,"",None,0,
            ("Cancel",Gtk.ResponseType.CANCEL,"Save",Gtk.ResponseType.ACCEPT))
        
        
        
        return
    
# End Class SceneOpt
