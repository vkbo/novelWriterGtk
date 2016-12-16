#!/usr/bin/env python
# -*- coding: utf-8 -*

##
#  pyÉcrire
# ==========
#
#  Simple text editor for structuring and writing novels
#
#  By: Veronica Berglyd Olsen
##

import gtk
import pyecrire

from pyecrire.gui import GUI

ecr = GUI()
ecr.show_all()
gtk.main()
