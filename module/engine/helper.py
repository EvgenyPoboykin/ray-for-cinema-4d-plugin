# coding: utf-8

# plugin Ray v 1.0.28 for Cinema 4D (R16-19)

#-------------------------------------------------------
# Author: Poboykin Eugene Gennadievich (studiolatte.com)
#Usta-Ilimsk, the Irkutsk region, the Russian Federation
#-------------------------------------------------------
#Автор: Побойкин Евгений Геннадьевич (studiolatte.com)
#г. Уста-Илимск, Иркутской области, РФ
#-------------------------------------------------------


import os
import sys

folder = os.path.dirname(__file__)
if folder not in sys.path:
    sys.path.insert(0, folder)
from c4d.threading import C4DThread
import math
import c4d
from c4d import plugins, utils, bitmaps, gui, threading

class Helper(c4d.gui.GeDialog):

    title = ''
    path = ''
    pid = 0
    html = None

    def __init__(self, title = '', path = ''):
        
        self.title = title
        self.path = path
        DIALOG_NOMENUBAR = 55
        self.AddGadget(DIALOG_NOMENUBAR, 0)

    def CreateLayout(self):
        
        self.pid += 1
        self.SetTitle(self.title)
        self.html = self.AddCustomGui(0, c4d.CUSTOMGUI_HTMLVIEWER, '', c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 10, 10, c4d.BaseContainer())
        self.html.SetUrl(self.path, c4d.URL_ENCODING_UTF16)
        
        return True

    def show(self, path, title, x, y, width, height):
        
        self.path = path
        self.title = title
        self.Open(c4d.DLG_TYPE_ASYNC, self.pid, x, y, width, height)
        if self.html is not None:
            self.html.SetUrl(self.path, c4d.URL_ENCODING_UTF16)
        
        return