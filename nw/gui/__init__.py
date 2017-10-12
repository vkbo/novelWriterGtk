# -*- coding: utf-8 -*
"""novelWriter GUI Init

 novelWriter – GUI Init
===============================
 Init file for the GUI

 File History:
 Created: 2017-10-03 [0.4.0]

"""

import logging
import nw

from nw.gui.bookpane   import GuiBookPane
from nw.gui.charstree  import GuiCharsTree
from nw.gui.charspane  import GuiCharsPane
from nw.gui.charstree  import GuiCharsTree
from nw.gui.docdetails import GuiDocDetails
from nw.gui.doceditor  import GuiDocEditor
from nw.gui.maintree   import GuiMainTree
from nw.gui.noteeditor import GuiNoteEditor
from nw.gui.plotspane  import GuiPlotsPane
from nw.gui.plotstree  import GuiPlotsTree
from nw.gui.scenepane  import GuiSceneEditor
from nw.gui.winmain    import GuiWinMain

logger = logging.getLogger(__name__)
