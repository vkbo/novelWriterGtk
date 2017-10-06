# -*- coding: utf-8 -*
"""novelWriter Document File

 novelWriter – Document File
=============================
 Manages a single document

 File History:
 Created: 2017-10-06 [0.4.0]

"""

import logging

from os      import path
from hashlib import sha256

logger = logging.getLogger(__name__)

class DocFile():
    
    def __init__(self, docHandle):
        
        self.docHandle = docHandle
        
        return

# End Class DocFile
