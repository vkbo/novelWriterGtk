# -*- coding: utf-8 -*
#
#  pyÉcrire – Project Class
#
##

import logging as logger

import gi
gi.require_version('Gtk', '3.0')

from gi.repository      import Gtk
from pyecrire.functions import *

class Project():

    def __init__(self, config):

        self.mainConf = config
        print makeHandle("Test")
        print simplifyString("pyÉcrire")

        return

    def newProject(self, guiObject):

        return
