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

from module.engine import S
from module.engine import st_ui
from module.engine import bc_ui
from module.engine import d_ui
from module.engine import sb_ui
from module.engine import gl_ui
from module.engine import if_ui
from module.engine import s_ui
from module.engine import oh_ui
from module.engine import pre_ui




#-------------------------------------------------------------------------------------------- Preset_Rays
class Preset_Rays(c4d.gui.GeDialog):      

    #-------------------------------------------------------------------------------------------- создание интерфейса диалога генератора
    def CreateLayout(self):

        doc = c4d.documents.GetActiveDocument()

        #-------------------------------------------------------------------------------------------- контейнеры для картинок
        BC_1 = c4d.BaseContainer()
        BC_1.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        BC_1.SetBool(c4d.BITMAPBUTTON_TOGGLE, True)
        BC_1.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_WIDTH, False)
        BC_1.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_HEIGHT, False)
        BC_1.SetBool(c4d.BITMAPBUTTON_NOBORDERDRAW, False)
        BC_1.SetLong(c4d.BITMAPBUTTON_ICONID1, pre_ui.PRESET_1)

        BC_2 = c4d.BaseContainer()
        BC_2.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        BC_2.SetBool(c4d.BITMAPBUTTON_TOGGLE, True)
        BC_2.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_WIDTH, False)
        BC_2.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_HEIGHT, False)
        BC_2.SetBool(c4d.BITMAPBUTTON_NOBORDERDRAW, False)
        BC_2.SetLong(c4d.BITMAPBUTTON_ICONID1, pre_ui.PRESET_2)

        BC_3 = c4d.BaseContainer()
        BC_3.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        BC_3.SetBool(c4d.BITMAPBUTTON_TOGGLE, True)
        BC_3.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_WIDTH, False)
        BC_3.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_HEIGHT, False)
        BC_3.SetBool(c4d.BITMAPBUTTON_NOBORDERDRAW, False)
        BC_3.SetLong(c4d.BITMAPBUTTON_ICONID1, pre_ui.PRESET_3)

        BC_4 = c4d.BaseContainer()
        BC_4.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        BC_4.SetBool(c4d.BITMAPBUTTON_TOGGLE, True)
        BC_4.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_WIDTH, False)
        BC_4.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_HEIGHT, False)
        BC_4.SetBool(c4d.BITMAPBUTTON_NOBORDERDRAW, False)
        BC_4.SetLong(c4d.BITMAPBUTTON_ICONID1, pre_ui.PRESET_4)

        BC_5 = c4d.BaseContainer()
        BC_5.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        BC_5.SetBool(c4d.BITMAPBUTTON_TOGGLE, True)
        BC_5.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_WIDTH, False)
        BC_5.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_HEIGHT, False)
        BC_5.SetBool(c4d.BITMAPBUTTON_NOBORDERDRAW, False)
        BC_5.SetLong(c4d.BITMAPBUTTON_ICONID1, pre_ui.PRESET_5)

        #-----------------------

        BC_6 = c4d.BaseContainer()
        BC_6.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        BC_6.SetBool(c4d.BITMAPBUTTON_TOGGLE, True)
        BC_6.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_WIDTH, False)
        BC_6.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_HEIGHT, False)
        BC_6.SetBool(c4d.BITMAPBUTTON_NOBORDERDRAW, False)
        BC_6.SetLong(c4d.BITMAPBUTTON_ICONID1, pre_ui.PRESET_6)

        BC_7 = c4d.BaseContainer()
        BC_7.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        BC_7.SetBool(c4d.BITMAPBUTTON_TOGGLE, True)
        BC_7.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_WIDTH, False)
        BC_7.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_HEIGHT, False)
        BC_7.SetBool(c4d.BITMAPBUTTON_NOBORDERDRAW, False)
        BC_7.SetLong(c4d.BITMAPBUTTON_ICONID1, pre_ui.PRESET_7)

        BC_8 = c4d.BaseContainer()
        BC_8.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        BC_8.SetBool(c4d.BITMAPBUTTON_TOGGLE, True)
        BC_8.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_WIDTH, False)
        BC_8.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_HEIGHT, False)
        BC_8.SetBool(c4d.BITMAPBUTTON_NOBORDERDRAW, False)
        BC_8.SetLong(c4d.BITMAPBUTTON_ICONID1, pre_ui.PRESET_8)

        BC_9 = c4d.BaseContainer()
        BC_9.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        BC_9.SetBool(c4d.BITMAPBUTTON_TOGGLE, True)
        BC_9.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_WIDTH, False)
        BC_9.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_HEIGHT, False)
        BC_9.SetBool(c4d.BITMAPBUTTON_NOBORDERDRAW, False)
        BC_9.SetLong(c4d.BITMAPBUTTON_ICONID1, pre_ui.PRESET_9)

        BC_10 = c4d.BaseContainer()
        BC_10.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        BC_10.SetBool(c4d.BITMAPBUTTON_TOGGLE, True)
        BC_10.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_WIDTH, False)
        BC_10.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_HEIGHT, False)
        BC_10.SetBool(c4d.BITMAPBUTTON_NOBORDERDRAW, False)
        BC_10.SetLong(c4d.BITMAPBUTTON_ICONID1, pre_ui.PRESET_10)

        #-----------------------

        BC_11 = c4d.BaseContainer()
        BC_11.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        BC_11.SetBool(c4d.BITMAPBUTTON_TOGGLE, True)
        BC_11.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_WIDTH, False)
        BC_11.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_HEIGHT, False)
        BC_11.SetBool(c4d.BITMAPBUTTON_NOBORDERDRAW, False)
        BC_11.SetLong(c4d.BITMAPBUTTON_ICONID1, pre_ui.PRESET_11)

        BC_12 = c4d.BaseContainer()
        BC_12.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        BC_12.SetBool(c4d.BITMAPBUTTON_TOGGLE, True)
        BC_12.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_WIDTH, False)
        BC_12.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_HEIGHT, False)
        BC_12.SetBool(c4d.BITMAPBUTTON_NOBORDERDRAW, False)
        BC_12.SetLong(c4d.BITMAPBUTTON_ICONID1, pre_ui.PRESET_12)

        BC_13 = c4d.BaseContainer()
        BC_13.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        BC_13.SetBool(c4d.BITMAPBUTTON_TOGGLE, True)
        BC_13.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_WIDTH, False)
        BC_13.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_HEIGHT, False)
        BC_13.SetBool(c4d.BITMAPBUTTON_NOBORDERDRAW, False)
        BC_13.SetLong(c4d.BITMAPBUTTON_ICONID1, pre_ui.PRESET_13)

        BC_14 = c4d.BaseContainer()
        BC_14.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        BC_14.SetBool(c4d.BITMAPBUTTON_TOGGLE, True)
        BC_14.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_WIDTH, False)
        BC_14.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_HEIGHT, False)
        BC_14.SetBool(c4d.BITMAPBUTTON_NOBORDERDRAW, False)
        BC_14.SetLong(c4d.BITMAPBUTTON_ICONID1, pre_ui.PRESET_14)

        BC_15 = c4d.BaseContainer()
        BC_15.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        BC_15.SetBool(c4d.BITMAPBUTTON_TOGGLE, True)
        BC_15.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_WIDTH, False)
        BC_15.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_HEIGHT, False)
        BC_15.SetBool(c4d.BITMAPBUTTON_NOBORDERDRAW, False)
        BC_15.SetLong(c4d.BITMAPBUTTON_ICONID1, pre_ui.PRESET_15)

        #-----------------------

        BC_16 = c4d.BaseContainer()
        BC_16.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        BC_16.SetBool(c4d.BITMAPBUTTON_TOGGLE, True)
        BC_16.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_WIDTH, False)
        BC_16.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_HEIGHT, False)
        BC_16.SetBool(c4d.BITMAPBUTTON_NOBORDERDRAW, False)
        BC_16.SetLong(c4d.BITMAPBUTTON_ICONID1, pre_ui.PRESET_16)

        BC_17 = c4d.BaseContainer()
        BC_17.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        BC_17.SetBool(c4d.BITMAPBUTTON_TOGGLE, True)
        BC_17.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_WIDTH, False)
        BC_17.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_HEIGHT, False)
        BC_17.SetBool(c4d.BITMAPBUTTON_NOBORDERDRAW, False)
        BC_17.SetLong(c4d.BITMAPBUTTON_ICONID1, pre_ui.PRESET_17)

        BC_18 = c4d.BaseContainer()
        BC_18.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        BC_18.SetBool(c4d.BITMAPBUTTON_TOGGLE, True)
        BC_18.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_WIDTH, False)
        BC_18.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_HEIGHT, False)
        BC_18.SetBool(c4d.BITMAPBUTTON_NOBORDERDRAW, False)
        BC_18.SetLong(c4d.BITMAPBUTTON_ICONID1, pre_ui.PRESET_18)

        BC_19 = c4d.BaseContainer()
        BC_19.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        BC_19.SetBool(c4d.BITMAPBUTTON_TOGGLE, True)
        BC_19.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_WIDTH, False)
        BC_19.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_HEIGHT, False)
        BC_19.SetBool(c4d.BITMAPBUTTON_NOBORDERDRAW, False)
        BC_19.SetLong(c4d.BITMAPBUTTON_ICONID1, pre_ui.PRESET_19)

        BC_20 = c4d.BaseContainer()
        BC_20.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        BC_20.SetBool(c4d.BITMAPBUTTON_TOGGLE, True)
        BC_20.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_WIDTH, False)
        BC_20.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_HEIGHT, False)
        BC_20.SetBool(c4d.BITMAPBUTTON_NOBORDERDRAW, False)
        BC_20.SetLong(c4d.BITMAPBUTTON_ICONID1, pre_ui.PRESET_20)

        #-----------------------

        BC_21 = c4d.BaseContainer()
        BC_21.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        BC_21.SetBool(c4d.BITMAPBUTTON_TOGGLE, True)
        BC_21.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_WIDTH, False)
        BC_21.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_HEIGHT, False)
        BC_21.SetBool(c4d.BITMAPBUTTON_NOBORDERDRAW, False)
        BC_21.SetLong(c4d.BITMAPBUTTON_ICONID1, pre_ui.PRESET_21)

        # BC_22 = c4d.BaseContainer()
        # BC_22.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        # BC_22.SetBool(c4d.BITMAPBUTTON_TOGGLE, True)
        # BC_22.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_WIDTH, False)
        # BC_22.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_HEIGHT, False)
        # BC_22.SetBool(c4d.BITMAPBUTTON_NOBORDERDRAW, False)
        # BC_22.SetLong(c4d.BITMAPBUTTON_ICONID1, pre_ui.PRESET_22)

        # BC_23 = c4d.BaseContainer()
        # BC_23.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        # BC_23.SetBool(c4d.BITMAPBUTTON_TOGGLE, True)
        # BC_23.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_WIDTH, False)
        # BC_23.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_HEIGHT, False)
        # BC_23.SetBool(c4d.BITMAPBUTTON_NOBORDERDRAW, False)
        # BC_23.SetLong(c4d.BITMAPBUTTON_ICONID1, pre_ui.PRESET_23)

        # BC_24 = c4d.BaseContainer()
        # BC_24.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        # BC_24.SetBool(c4d.BITMAPBUTTON_TOGGLE, True)
        # BC_24.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_WIDTH, False)
        # BC_24.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_HEIGHT, False)
        # BC_24.SetBool(c4d.BITMAPBUTTON_NOBORDERDRAW, False)
        # BC_24.SetLong(c4d.BITMAPBUTTON_ICONID1, pre_ui.PRESET_24)

        # BC_25 = c4d.BaseContainer()
        # BC_25.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        # BC_25.SetBool(c4d.BITMAPBUTTON_TOGGLE, True)
        # BC_25.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_WIDTH, False)
        # BC_25.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_HEIGHT, False)
        # BC_25.SetBool(c4d.BITMAPBUTTON_NOBORDERDRAW, False)
        # BC_25.SetLong(c4d.BITMAPBUTTON_ICONID1, pre_ui.PRESET_25)

        #-----------------------

        # BC_26 = c4d.BaseContainer()
        # BC_26.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        # BC_26.SetBool(c4d.BITMAPBUTTON_TOGGLE, True)
        # BC_26.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_WIDTH, False)
        # BC_26.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_HEIGHT, False)
        # BC_26.SetBool(c4d.BITMAPBUTTON_NOBORDERDRAW, False)
        # BC_26.SetLong(c4d.BITMAPBUTTON_ICONID1, pre_ui.PRESET_26)

        # BC_27 = c4d.BaseContainer()
        # BC_27.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        # BC_27.SetBool(c4d.BITMAPBUTTON_TOGGLE, True)
        # BC_27.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_WIDTH, False)
        # BC_27.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_HEIGHT, False)
        # BC_27.SetBool(c4d.BITMAPBUTTON_NOBORDERDRAW, False)
        # BC_27.SetLong(c4d.BITMAPBUTTON_ICONID1, pre_ui.PRESET_27)

        # BC_28 = c4d.BaseContainer()
        # BC_28.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        # BC_28.SetBool(c4d.BITMAPBUTTON_TOGGLE, True)
        # BC_28.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_WIDTH, False)
        # BC_28.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_HEIGHT, False)
        # BC_28.SetBool(c4d.BITMAPBUTTON_NOBORDERDRAW, False)
        # BC_28.SetLong(c4d.BITMAPBUTTON_ICONID1, pre_ui.PRESET_28)

        # BC_29 = c4d.BaseContainer()
        # BC_29.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        # BC_29.SetBool(c4d.BITMAPBUTTON_TOGGLE, True)
        # BC_29.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_WIDTH, False)
        # BC_29.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_HEIGHT, False)
        # BC_29.SetBool(c4d.BITMAPBUTTON_NOBORDERDRAW, False)
        # BC_29.SetLong(c4d.BITMAPBUTTON_ICONID1, pre_ui.PRESET_29)

        # BC_30 = c4d.BaseContainer()
        # BC_30.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        # BC_30.SetBool(c4d.BITMAPBUTTON_TOGGLE, True)
        # BC_30.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_WIDTH, False)
        # BC_30.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_HEIGHT, False)
        # BC_30.SetBool(c4d.BITMAPBUTTON_NOBORDERDRAW, False)
        # BC_30.SetLong(c4d.BITMAPBUTTON_ICONID1, pre_ui.PRESET_30)

        RS_noGI = c4d.BaseContainer()
        RS_noGI.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        RS_noGI.SetBool(c4d.BITMAPBUTTON_TOGGLE, True)
        RS_noGI.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_WIDTH, False)
        RS_noGI.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_HEIGHT, False)
        RS_noGI.SetBool(c4d.BITMAPBUTTON_NOBORDERDRAW, False)
        RS_noGI.SetLong(c4d.BITMAPBUTTON_ICONID1, pre_ui.RenderS_noGI)

        RS_GI = c4d.BaseContainer()
        RS_GI.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        RS_GI.SetBool(c4d.BITMAPBUTTON_TOGGLE, True)
        RS_GI.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_WIDTH, False)
        RS_GI.SetBool(c4d.BITMAPBUTTON_IGNORE_BITMAP_HEIGHT, False)
        RS_GI.SetBool(c4d.BITMAPBUTTON_NOBORDERDRAW, False)
        RS_GI.SetLong(c4d.BITMAPBUTTON_ICONID1, pre_ui.RenderS_GI)
        #--------------------------------------------------------------------------------------------


        #-------------------------------------------------------------------------------------------- интерфейс

        self.SetTitle("Rays Preset Scene v 1.0.29")

        self.GroupBegin(pre_ui.PRESETS_STUDIO, c4d.BFH_CENTER, 1, 0, "", 0, 0, 0)

        self.AddCustomGui(pre_ui.RenderS_noGI, c4d.CUSTOMGUI_BITMAPBUTTON, "", c4d.BFH_SCALEFIT, 0, 0, RS_noGI)
        self.AddCustomGui(pre_ui.RenderS_GI, c4d.CUSTOMGUI_BITMAPBUTTON, "", c4d.BFH_SCALEFIT, 0, 0, RS_GI)
        self.GroupSpace(0, 0)

        self.GroupEnd()

        self.GroupBegin(pre_ui.PRESETS_STUDIO, c4d.BFH_CENTER, 3, 0, "", 0, 0, 0)
        self.GroupSpace(0, 0)

        self.AddCustomGui(pre_ui.PRESET_1, c4d.CUSTOMGUI_BITMAPBUTTON, "", c4d.BFH_SCALEFIT, 0, 0, BC_1)
        self.AddCustomGui(pre_ui.PRESET_2, c4d.CUSTOMGUI_BITMAPBUTTON, "", c4d.BFH_SCALEFIT, 0, 0, BC_2)
        self.AddCustomGui(pre_ui.PRESET_3, c4d.CUSTOMGUI_BITMAPBUTTON, "", c4d.BFH_SCALEFIT, 0, 0, BC_3)
        self.AddCustomGui(pre_ui.PRESET_4, c4d.CUSTOMGUI_BITMAPBUTTON, "", c4d.BFH_SCALEFIT, 0, 0, BC_4)
        self.AddCustomGui(pre_ui.PRESET_5, c4d.CUSTOMGUI_BITMAPBUTTON, "", c4d.BFH_SCALEFIT, 0, 0, BC_5)

        self.AddCustomGui(pre_ui.PRESET_6, c4d.CUSTOMGUI_BITMAPBUTTON, "", c4d.BFH_SCALEFIT, 0, 0, BC_6)
        self.AddCustomGui(pre_ui.PRESET_7, c4d.CUSTOMGUI_BITMAPBUTTON, "", c4d.BFH_SCALEFIT, 0, 0, BC_7)
        self.AddCustomGui(pre_ui.PRESET_8, c4d.CUSTOMGUI_BITMAPBUTTON, "", c4d.BFH_SCALEFIT, 0, 0, BC_8)
        self.AddCustomGui(pre_ui.PRESET_9, c4d.CUSTOMGUI_BITMAPBUTTON, "", c4d.BFH_SCALEFIT, 0, 0, BC_9)
        self.AddCustomGui(pre_ui.PRESET_10, c4d.CUSTOMGUI_BITMAPBUTTON, "", c4d.BFH_SCALEFIT, 0, 0, BC_10)
        
        self.AddCustomGui(pre_ui.PRESET_11, c4d.CUSTOMGUI_BITMAPBUTTON, "", c4d.BFH_SCALEFIT, 0, 0, BC_11)
        self.AddCustomGui(pre_ui.PRESET_12, c4d.CUSTOMGUI_BITMAPBUTTON, "", c4d.BFH_SCALEFIT, 0, 0, BC_12)
        self.AddCustomGui(pre_ui.PRESET_13, c4d.CUSTOMGUI_BITMAPBUTTON, "", c4d.BFH_SCALEFIT, 0, 0, BC_13)
        self.AddCustomGui(pre_ui.PRESET_14, c4d.CUSTOMGUI_BITMAPBUTTON, "", c4d.BFH_SCALEFIT, 0, 0, BC_14)
        self.AddCustomGui(pre_ui.PRESET_15, c4d.CUSTOMGUI_BITMAPBUTTON, "", c4d.BFH_SCALEFIT, 0, 0, BC_15)

        self.AddCustomGui(pre_ui.PRESET_16, c4d.CUSTOMGUI_BITMAPBUTTON, "", c4d.BFH_SCALEFIT, 0, 0, BC_16)
        self.AddCustomGui(pre_ui.PRESET_17, c4d.CUSTOMGUI_BITMAPBUTTON, "", c4d.BFH_SCALEFIT, 0, 0, BC_17)
        self.AddCustomGui(pre_ui.PRESET_18, c4d.CUSTOMGUI_BITMAPBUTTON, "", c4d.BFH_SCALEFIT, 0, 0, BC_18)
        self.AddCustomGui(pre_ui.PRESET_19, c4d.CUSTOMGUI_BITMAPBUTTON, "", c4d.BFH_SCALEFIT, 0, 0, BC_19)
        self.AddCustomGui(pre_ui.PRESET_20, c4d.CUSTOMGUI_BITMAPBUTTON, "", c4d.BFH_SCALEFIT, 0, 0, BC_20)
        
        self.AddCustomGui(pre_ui.PRESET_21, c4d.CUSTOMGUI_BITMAPBUTTON, "", c4d.BFH_SCALEFIT, 0, 0, BC_21)

        # self.GroupEnd()

        # self.GroupBegin(pre_ui.PRESETS_FLOOR, c4d.BFH_CENTER, 3, 0, "Color Studio Presets", 0, 0, 0)
        
        
        # self.AddCustomGui(pre_ui.PRESET_22, c4d.CUSTOMGUI_BITMAPBUTTON, "", c4d.BFH_SCALEFIT, 0, 0, BC_22)
        # self.AddCustomGui(pre_ui.PRESET_23, c4d.CUSTOMGUI_BITMAPBUTTON, "", c4d.BFH_SCALEFIT, 0, 0, BC_23)
        # self.AddCustomGui(pre_ui.PRESET_24, c4d.CUSTOMGUI_BITMAPBUTTON, "", c4d.BFH_SCALEFIT, 0, 0, BC_24)
        # self.AddCustomGui(pre_ui.PRESET_25, c4d.CUSTOMGUI_BITMAPBUTTON, "", c4d.BFH_SCALEFIT, 0, 0, BC_25)
        
        # self.AddCustomGui(pre_ui.PRESET_26, c4d.CUSTOMGUI_BITMAPBUTTON, "", c4d.BFH_SCALEFIT, 0, 0, BC_26)
        # self.AddCustomGui(pre_ui.PRESET_27, c4d.CUSTOMGUI_BITMAPBUTTON, "", c4d.BFH_SCALEFIT, 0, 0, BC_27)
        # self.AddCustomGui(pre_ui.PRESET_28, c4d.CUSTOMGUI_BITMAPBUTTON, "", c4d.BFH_SCALEFIT, 0, 0, BC_28)
        # self.AddCustomGui(pre_ui.PRESET_29, c4d.CUSTOMGUI_BITMAPBUTTON, "", c4d.BFH_SCALEFIT, 0, 0, BC_29)
        # # self.AddCustomGui(pre_ui.PRESET_30, c4d.CUSTOMGUI_BITMAPBUTTON, "", c4d.BFH_SCALEFIT, 0, 0, BC_30)
      
        # self.GroupEnd()

        self.GroupEnd()
        #-------------------------------------------------------------------------------------------- конец интерфейса
        

        return True

    #-------------------------------------------------------------------------------------------- Command
    def Command(self, id, msg):
        
        doc = c4d.documents.GetActiveDocument()
        # поиск деталей
        if id == pre_ui.RenderS_noGI:

            #---------------------------------------------------------------------------- rd_1
            rd_1 = c4d.documents.RenderData()
            doc.InsertRenderData(rd_1)
            rd_1.SetName('Physical Render fullHD')

            rd_1[c4d.RDATA_XRES] = 1920
            rd_1[c4d.RDATA_YRES] = 1080
            rd_1[c4d.RDATA_LOCKRATIO] = True
            rd_1[c4d.RDATA_FRAMERATE] = 25
            rd_1[c4d.RDATA_SAVEIMAGE] = False
            rd_1[c4d.RDATA_FORMAT] = 1023671
            rd_1[c4d.RDATA_AUTOLIGHT] = False
            
            vpost_1   = rd_1.GetFirstVideoPost()
            rd_1[c4d.RDATA_RENDERENGINE] = c4d.RDATA_RENDERENGINE_PHYSICAL
            
            vpost_phy_1 = c4d.BaseList2D(c4d.VPxmbsampler)
            rd_1.InsertVideoPost(vpost_phy_1)
    
            vpost_phy_1[c4d.VP_XMB_RAYTRACING_QUALITY] = 2
            vpost_phy_1[c4d.VP_XMB_RAYTRACING_SAMPLES] = 6
            vpost_phy_1[c4d.VP_XMB_RAYTRACING_SAMPLES_SHADING_MIN] = 4
            vpost_phy_1[c4d.VP_XMB_RAYTRACING_SAMPLES_SHADING_MAX] = 7
            vpost_phy_1[c4d.VP_XMB_RAYTRACING_SAMPLES_SHADING_ERROR] = 0.01
            #---------------------------------------------------------------------------- rd_1 end
            
            #---------------------------------------------------------------------------- rd_2
            rd_2 = c4d.documents.RenderData()
            doc.InsertRenderData(rd_2)
            rd_2.SetName('Physical Render HD low')
            rd_2.InsertUnder(rd_1)

            rd_2[c4d.RDATA_XRES] = 1280
            rd_2[c4d.RDATA_YRES] = 720
            rd_2[c4d.RDATA_LOCKRATIO] = True
            rd_2[c4d.RDATA_FRAMERATE] = 25
            rd_2[c4d.RDATA_SAVEIMAGE] = False
            rd_2[c4d.RDATA_FORMAT] = 1023671
            rd_2[c4d.RDATA_AUTOLIGHT] = False
            
            vpost_2   = rd_2.GetFirstVideoPost()
            rd_2[c4d.RDATA_RENDERENGINE] = c4d.RDATA_RENDERENGINE_PHYSICAL
            
            vpost_phy_2 = c4d.BaseList2D(c4d.VPxmbsampler)
            rd_2.InsertVideoPost(vpost_phy_2)

            vpost_phy_2[c4d.VP_XMB_RAYTRACING_QUALITY] = 1
            vpost_phy_2[c4d.VP_XMB_RAYTRACING_SAMPLES] = 4
            vpost_phy_2[c4d.VP_XMB_RAYTRACING_SAMPLES_SHADING_MIN] = 2
            vpost_phy_2[c4d.VP_XMB_RAYTRACING_SAMPLES_SHADING_MAX] = 5
            vpost_phy_2[c4d.VP_XMB_RAYTRACING_SAMPLES_SHADING_ERROR] = 0.05
            #---------------------------------------------------------------------------- rd_2 end
            
            
            #---------------------------------------------------------------------------- rd_3
            rd_3 = c4d.documents.RenderData()
            doc.InsertRenderData(rd_3)
            rd_3.SetName('Physical Render Preview Low')
            rd_3.InsertUnder(rd_1)
            rd_3.InsertAfter(rd_2)

            rd_3[c4d.RDATA_XRES] = 800
            rd_3[c4d.RDATA_YRES] = 450
            rd_3[c4d.RDATA_LOCKRATIO] = True
            rd_3[c4d.RDATA_FRAMERATE] = 25
            rd_3[c4d.RDATA_SAVEIMAGE] = False
            rd_3[c4d.RDATA_FORMAT] = 1023671
            rd_3[c4d.RDATA_AUTOLIGHT] = False
            
            vpost_3   = rd_3.GetFirstVideoPost()
            rd_3[c4d.RDATA_RENDERENGINE] = c4d.RDATA_RENDERENGINE_PHYSICAL
            
            vpost_phy_3 = c4d.BaseList2D(c4d.VPxmbsampler)
            rd_3.InsertVideoPost(vpost_phy_3)

            vpost_phy_3[c4d.VP_XMB_RAYTRACING_QUALITY] = 0
            vpost_phy_3[c4d.VP_XMB_RAYTRACING_SAMPLES] = 2
            vpost_phy_3[c4d.VP_XMB_RAYTRACING_SAMPLES_SHADING_MIN] = 0
            vpost_phy_3[c4d.VP_XMB_RAYTRACING_SAMPLES_SHADING_MAX] = 3
            vpost_phy_3[c4d.VP_XMB_RAYTRACING_SAMPLES_SHADING_ERROR] = 0.2
            #---------------------------------------------------------------------------- rd_3 end

            doc.SetActiveRenderData(rd_3)
            
            c4d.EventAdd()
        
        if id == pre_ui.RenderS_GI:

            #---------------------------------------------------------------------------- rd_1
            rd_1 = c4d.documents.RenderData()
            doc.InsertRenderData(rd_1)
            rd_1.SetName('Physical GI Render fullHD')

            rd_1[c4d.RDATA_XRES] = 1920
            rd_1[c4d.RDATA_YRES] = 1080
            rd_1[c4d.RDATA_LOCKRATIO] = True
            rd_1[c4d.RDATA_FRAMERATE] = 25
            rd_1[c4d.RDATA_SAVEIMAGE] = False
            rd_1[c4d.RDATA_FORMAT] = 1023671
            rd_1[c4d.RDATA_AUTOLIGHT] = False
            
            vpost_1   = rd_1.GetFirstVideoPost()
            rd_1[c4d.RDATA_RENDERENGINE] = c4d.RDATA_RENDERENGINE_PHYSICAL
            
            vpost_phy_1 = c4d.BaseList2D(c4d.VPxmbsampler)
            rd_1.InsertVideoPost(vpost_phy_1)

            vpost_phy_1[c4d.VP_XMB_RAYTRACING_QUALITY] = 2
            vpost_phy_1[c4d.VP_XMB_RAYTRACING_SAMPLES] = 6
            vpost_phy_1[c4d.VP_XMB_RAYTRACING_SAMPLES_SHADING_MIN] = 4
            vpost_phy_1[c4d.VP_XMB_RAYTRACING_SAMPLES_SHADING_MAX] = 7
            vpost_phy_1[c4d.VP_XMB_RAYTRACING_SAMPLES_SHADING_ERROR] = 0.01


            vpost_gi_1 = c4d.BaseList2D(1021096)
            rd_1.InsertVideoPost(vpost_gi_1)

            vpost_gi_1[c4d.GI_SETUP_DATA_PRIMARY_METHOD] = 6040
            vpost_gi_1[c4d.GI_SETUP_DATA_SECONDARY_METHOD] = 6040
            vpost_gi_1[c4d.GI_SETUP_DATA_DIFFUSE_DEPTH] = 2
            vpost_gi_1[c4d.GI_SETUP_DATA_GAMMA_VALUE] = 1
            vpost_gi_1[c4d.GI_SETUP_DATA_QMC_COUNT_METHOD] = 6060
            vpost_gi_1[c4d.GI_SETUP_DATA_QMC_COUNT] = 60
            #---------------------------------------------------------------------------- rd_1 end
            
            #---------------------------------------------------------------------------- rd_2
            rd_2 = c4d.documents.RenderData()
            doc.InsertRenderData(rd_2)
            rd_2.SetName('Physical GI Render HD low')
            rd_2.InsertUnder(rd_1)

            rd_2[c4d.RDATA_XRES] = 1280
            rd_2[c4d.RDATA_YRES] = 720
            rd_2[c4d.RDATA_LOCKRATIO] = True
            rd_2[c4d.RDATA_FRAMERATE] = 25
            rd_2[c4d.RDATA_SAVEIMAGE] = False
            rd_2[c4d.RDATA_FORMAT] = 1023671
            rd_2[c4d.RDATA_AUTOLIGHT] = False
            
            vpost_2   = rd_2.GetFirstVideoPost()
            rd_2[c4d.RDATA_RENDERENGINE] = c4d.RDATA_RENDERENGINE_PHYSICAL
            
            vpost_phy_2 = c4d.BaseList2D(c4d.VPxmbsampler)
            rd_2.InsertVideoPost(vpost_phy_2)

            vpost_phy_2[c4d.VP_XMB_RAYTRACING_QUALITY] = 1
            vpost_phy_2[c4d.VP_XMB_RAYTRACING_SAMPLES] = 4
            vpost_phy_2[c4d.VP_XMB_RAYTRACING_SAMPLES_SHADING_MIN] = 2
            vpost_phy_2[c4d.VP_XMB_RAYTRACING_SAMPLES_SHADING_MAX] = 5
            vpost_phy_2[c4d.VP_XMB_RAYTRACING_SAMPLES_SHADING_ERROR] = 0.05

            vpost_gi_2 = c4d.BaseList2D(1021096)
            rd_2.InsertVideoPost(vpost_gi_2)

            vpost_gi_2[c4d.GI_SETUP_DATA_PRIMARY_METHOD] = 6040
            vpost_gi_2[c4d.GI_SETUP_DATA_SECONDARY_METHOD] = 6040
            vpost_gi_2[c4d.GI_SETUP_DATA_DIFFUSE_DEPTH] = 2
            vpost_gi_2[c4d.GI_SETUP_DATA_GAMMA_VALUE] = 1
            vpost_gi_2[c4d.GI_SETUP_DATA_QMC_COUNT_METHOD] = 6060
            vpost_gi_2[c4d.GI_SETUP_DATA_QMC_COUNT] = 30
            #---------------------------------------------------------------------------- rd_2 end
            
            
            #---------------------------------------------------------------------------- rd_3
            rd_3 = c4d.documents.RenderData()
            doc.InsertRenderData(rd_3)
            rd_3.SetName('Physical GI Render Preview Low')
            rd_3.InsertUnder(rd_1)
            rd_3.InsertAfter(rd_2)

            rd_3[c4d.RDATA_XRES] = 800
            rd_3[c4d.RDATA_YRES] = 450
            rd_3[c4d.RDATA_LOCKRATIO] = True
            rd_3[c4d.RDATA_FRAMERATE] = 25
            rd_3[c4d.RDATA_SAVEIMAGE] = False
            rd_3[c4d.RDATA_FORMAT] = 1023671
            rd_3[c4d.RDATA_AUTOLIGHT] = False
            
            vpost_3   = rd_3.GetFirstVideoPost()
            rd_3[c4d.RDATA_RENDERENGINE] = c4d.RDATA_RENDERENGINE_PHYSICAL
            
            vpost_phy_3 = c4d.BaseList2D(c4d.VPxmbsampler)
            rd_3.InsertVideoPost(vpost_phy_3)

            vpost_phy_3[c4d.VP_XMB_RAYTRACING_QUALITY] = 0
            vpost_phy_3[c4d.VP_XMB_RAYTRACING_SAMPLES] = 2
            vpost_phy_3[c4d.VP_XMB_RAYTRACING_SAMPLES_SHADING_MIN] = 0
            vpost_phy_3[c4d.VP_XMB_RAYTRACING_SAMPLES_SHADING_MAX] = 3
            vpost_phy_3[c4d.VP_XMB_RAYTRACING_SAMPLES_SHADING_ERROR] = 0.2

            vpost_gi_3 = c4d.BaseList2D(1021096)
            rd_3.InsertVideoPost(vpost_gi_3)
            
            vpost_gi_3[c4d.GI_SETUP_DATA_PRIMARY_METHOD] = 6040
            vpost_gi_3[c4d.GI_SETUP_DATA_SECONDARY_METHOD] = 6040
            vpost_gi_3[c4d.GI_SETUP_DATA_DIFFUSE_DEPTH] = 2
            vpost_gi_3[c4d.GI_SETUP_DATA_GAMMA_VALUE] = 1
            vpost_gi_3[c4d.GI_SETUP_DATA_QMC_COUNT_METHOD] = 6060
            vpost_gi_3[c4d.GI_SETUP_DATA_QMC_COUNT] = 10
            #-------------------------------------------------
            
            
            
            #---------------------------------------------------------------------------- rd_3 end

            doc.SetActiveRenderData(rd_1)
            rd_1.ChangeNBit(c4d.NBIT_OM1_FOLD, c4d.NBITCONTROL_SET)

            doc.SetActiveRenderData(rd_3)
            
            c4d.EventAdd()

        if id == pre_ui.PRESET_1:

            targetLight = c4d.BaseObject(c4d.Onull)
            targetLight.SetName('Target for Lights (St with 2L)')
            doc.InsertObject(targetLight)
            targetLight[c4d.ID_BASEOBJECT_USECOLOR] = 2
            targetLight[c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(0.933, 0.894, 0.212)
            targetLight[c4d.NULLOBJECT_ICONCOL] = True

            studio = c4d.BaseObject(st_ui.STUDIO)
            studio.SetName('Studio with 2L')
            doc.InsertObject(studio)

            studio[st_ui.ST_MODE] = 1
            studio[st_ui.ST_WIDTH] = 400
            studio[st_ui.ST_HIDTH] = 590
            studio[st_ui.ST_DEFTH] = 450
            studio[st_ui.ST_ROUNDING] = 295
            studio[st_ui.ST_SUB_RENDER] = 3

            sb_l = c4d.BaseObject(sb_ui.SBOX)
            sb_l.SetName('Left Softbox (M)')
            doc.InsertObject(sb_l)

            sb_l[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(-175, 280, -130)
            # sb_l[c4d.ID_BASEOBJECT_REL_ROTATION] = c4d.Vector(math.radians(-54), math.radians(-47), math.radians(4.5))
            sb_l[sb_ui.SB_WIDTH] = 100
            sb_l[sb_ui.SB_HIDTH] = 440
            sb_l[sb_ui.SB_DIST] = 515

            c4d.CallButton(sb_l, sb_ui.SB_ADD_TARGET_TAG)
            c4d.EventAdd()
            target_sb_l = sb_l.GetTag(5676)
            target_sb_l[c4d.TARGETEXPRESSIONTAG_LINK] = targetLight

            sb_l[sb_ui.SB_LIGHT_COLOR] = c4d.Vector(1, 0.889, 0.71)
            sb_l[sb_ui.SB_BRIGHTNESS] = 0.85

            sb_r = c4d.BaseObject(sb_ui.SBOX)
            sb_r.SetName('Right Softbox')
            doc.InsertObject(sb_r)

            sb_r[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(134, 274, 157)
            # sb_r[c4d.ID_BASEOBJECT_REL_ROTATION] = c4d.Vector(math.radians(138.5), math.radians(-47.7), 0)
            sb_r[sb_ui.SB_MODE] = 1
            sb_r[sb_ui.SB_WIDTH] = 210
            sb_r[sb_ui.SB_DIST] = 340

            c4d.CallButton(sb_r, sb_ui.SB_ADD_TARGET_TAG)
            c4d.EventAdd()
            target_sb_r = sb_r.GetTag(5676)
            target_sb_r[c4d.TARGETEXPRESSIONTAG_LINK] = targetLight

            sb_r[sb_ui.SB_BRIGHTNESS] = 0.8
            sb_r[sb_ui.SB_USED] = True
            sb_r[sb_ui.SB_LINK] = sb_l

            gl = c4d.BaseObject(gl_ui.GLOBALLIGHT)
            gl.SetName('Global Light')
            doc.InsertObject(gl)

            gl[gl_ui.GL_USED] = True
            gl[gl_ui.GL_LINK] = sb_l
            gl[gl_ui.GL_INVERT_COLOR] = True
            gl[gl_ui.GL_LIGHT_STR] = 0.45

            c4d.EventAdd()

        if id == pre_ui.PRESET_2:

            studio = c4d.BaseObject(st_ui.STUDIO)
            studio.SetName('Studio with 4O')
            doc.InsertObject(studio)

            studio[st_ui.ST_MODE] = 1
            studio[st_ui.ST_WIDTH] = 400
            studio[st_ui.ST_HIDTH] = 590
            studio[st_ui.ST_DEFTH] = 450
            studio[st_ui.ST_ROUNDING] = 295
            studio[st_ui.ST_SUB_RENDER] = 3

            oh_1 = c4d.BaseObject(oh_ui.OVERHEAD)
            oh_1.SetName('Overhead Softbox 1 (M)')
            doc.InsertObject(oh_1)

            oh_1[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(-220, 300, 0)
            oh_1[oh_ui.OH_WIDTH] = 90
            oh_1[oh_ui.OH_HIDTH] = 600
            oh_1[oh_ui.OH_DIST] = 350
            oh_1[oh_ui.OH_BRIGHTNESS] = 0.7
            oh_1[oh_ui.OH_LIGHT_SHADOW_DENSITY] = 0.86

            oh_2 = c4d.BaseObject(oh_ui.OVERHEAD)
            oh_2.SetName('Overhead Softbox 2')
            doc.InsertObject(oh_2)

            oh_2[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(-80, 300, 0)
            oh_2[oh_ui.OH_WIDTH] = 90
            oh_2[oh_ui.OH_HIDTH] = 600
            oh_2[oh_ui.OH_DIST] = 350
            oh_2[oh_ui.OH_USED] = True
            oh_2[oh_ui.OH_LINK] = oh_1
            oh_2[oh_ui.OH_BRIGHTNESS] = 0.7
            oh_2[oh_ui.OH_LIGHT_SHADOW_DENSITY] = 0.86

            oh_3 = c4d.BaseObject(oh_ui.OVERHEAD)
            oh_3.SetName('Overhead Softbox 3')
            doc.InsertObject(oh_3)

            oh_3[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(80, 300, 0)
            oh_3[oh_ui.OH_WIDTH] = 90
            oh_3[oh_ui.OH_HIDTH] = 600
            oh_3[oh_ui.OH_DIST] = 350
            oh_3[oh_ui.OH_USED] = True
            oh_3[oh_ui.OH_LINK] = oh_1
            oh_3[oh_ui.OH_BRIGHTNESS] = 0.7
            oh_3[oh_ui.OH_LIGHT_SHADOW_DENSITY] = 0.86

            oh_4 = c4d.BaseObject(oh_ui.OVERHEAD)
            oh_4.SetName('Overhead Softbox 4')
            doc.InsertObject(oh_4)

            oh_4[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(220, 300, 0)
            oh_4[oh_ui.OH_WIDTH] = 90
            oh_4[oh_ui.OH_HIDTH] = 600
            oh_4[oh_ui.OH_DIST] = 350
            oh_4[oh_ui.OH_USED] = True
            oh_4[oh_ui.OH_LINK] = oh_1
            oh_4[oh_ui.OH_BRIGHTNESS] = 0.7
            oh_4[oh_ui.OH_LIGHT_SHADOW_DENSITY] = 0.86

            gl = c4d.BaseObject(gl_ui.GLOBALLIGHT)
            gl.SetName('Global Light')
            doc.InsertObject(gl)

            gl[gl_ui.GL_USED] = True
            gl[gl_ui.GL_LINK] = oh_1
            gl[gl_ui.GL_INVERT_COLOR] = True
            gl[gl_ui.GL_LIGHT_STR] = 0.3

            c4d.EventAdd()

        if id == pre_ui.PRESET_3:

            targetLight = c4d.BaseObject(c4d.Onull)
            targetLight.SetName('Target for Lights (St with 4O & 1S)')
            doc.InsertObject(targetLight)
            targetLight[c4d.ID_BASEOBJECT_USECOLOR] = 2
            targetLight[c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(0.933, 0.894, 0.212)
            targetLight[c4d.NULLOBJECT_ICONCOL] = True

            studio = c4d.BaseObject(st_ui.STUDIO)
            studio.SetName('Studio with 4O & 1S')
            doc.InsertObject(studio)

            studio[st_ui.ST_MODE] = 1
            studio[st_ui.ST_WIDTH] = 400
            studio[st_ui.ST_HIDTH] = 590
            studio[st_ui.ST_DEFTH] = 450
            studio[st_ui.ST_ROUNDING] = 295
            studio[st_ui.ST_SUB_RENDER] = 3

            sb_1 = c4d.BaseObject(sb_ui.SBOX)
            sb_1.SetName('Softbox (M)')
            doc.InsertObject(sb_1)

            sb_1[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(233, 220, -275)
            sb_1[sb_ui.SB_WIDTH] = 100
            sb_1[sb_ui.SB_HIDTH] = 163
            sb_1[sb_ui.SB_DIST] = 485

            c4d.CallButton(sb_1, sb_ui.SB_ADD_TARGET_TAG)
            c4d.EventAdd()
            target_sb_1 = sb_1.GetTag(5676)
            target_sb_1[c4d.TARGETEXPRESSIONTAG_LINK] = targetLight

            sb_1[sb_ui.SB_LIGHT_COLOR] = c4d.Vector(0.759, 0.914, 0.904)
            sb_1[sb_ui.SB_BRIGHTNESS] = 1


            oh_1 = c4d.BaseObject(oh_ui.OVERHEAD)
            oh_1.SetName('Overhead Softbox 1')
            doc.InsertObject(oh_1)

            oh_1[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(-220, 300, 0)
            oh_1[oh_ui.OH_WIDTH] = 120
            oh_1[oh_ui.OH_HIDTH] = 500
            oh_1[oh_ui.OH_DIST] = 350
            oh_1[oh_ui.OH_USED] = True
            oh_1[oh_ui.OH_INVERT_COLOR] = True
            oh_1[oh_ui.OH_LINK] = sb_1
            oh_1[oh_ui.OH_BRIGHTNESS] = 0.7
            oh_1[oh_ui.OH_LIGHT_SHADOW_DENSITY] = 0.86

            oh_2 = c4d.BaseObject(oh_ui.OVERHEAD)
            oh_2.SetName('Overhead Softbox 2')
            doc.InsertObject(oh_2)

            oh_2[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(-80, 300, 0)
            oh_2[oh_ui.OH_WIDTH] = 120
            oh_2[oh_ui.OH_HIDTH] = 500
            oh_2[oh_ui.OH_DIST] = 350
            oh_2[oh_ui.OH_USED] = True
            oh_2[oh_ui.OH_INVERT_COLOR] = True
            oh_2[oh_ui.OH_LINK] = sb_1
            oh_2[oh_ui.OH_BRIGHTNESS] = 0.7
            oh_2[oh_ui.OH_LIGHT_SHADOW_DENSITY] = 0.86

            oh_3 = c4d.BaseObject(oh_ui.OVERHEAD)
            oh_3.SetName('Overhead Softbox 3')
            doc.InsertObject(oh_3)

            oh_3[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(80, 300, 0)
            oh_3[oh_ui.OH_WIDTH] = 120
            oh_3[oh_ui.OH_HIDTH] = 500
            oh_3[oh_ui.OH_DIST] = 350
            oh_3[oh_ui.OH_USED] = True
            oh_3[oh_ui.OH_INVERT_COLOR] = True
            oh_3[oh_ui.OH_LINK] = sb_1
            oh_3[oh_ui.OH_BRIGHTNESS] = 0.7
            oh_3[oh_ui.OH_LIGHT_SHADOW_DENSITY] = 0.86

            oh_4 = c4d.BaseObject(oh_ui.OVERHEAD)
            oh_4.SetName('Overhead Softbox 4')
            doc.InsertObject(oh_4)

            oh_4[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(220, 300, 0)
            oh_4[oh_ui.OH_WIDTH] = 120
            oh_4[oh_ui.OH_HIDTH] = 500
            oh_4[oh_ui.OH_DIST] = 350
            oh_4[oh_ui.OH_USED] = True
            oh_4[oh_ui.OH_INVERT_COLOR] = True
            oh_4[oh_ui.OH_LINK] = sb_1
            oh_4[oh_ui.OH_BRIGHTNESS] = 0.7
            oh_4[oh_ui.OH_LIGHT_SHADOW_DENSITY] = 0.86

            gl = c4d.BaseObject(gl_ui.GLOBALLIGHT)
            gl.SetName('Global Light')
            doc.InsertObject(gl)

            gl[gl_ui.GL_USED] = True
            gl[gl_ui.GL_LINK] = sb_1
            gl[gl_ui.GL_INVERT_COLOR] = True
            gl[gl_ui.GL_LIGHT_STR] = 0.3

            c4d.EventAdd()

        if id == pre_ui.PRESET_4:

            targetLight = c4d.BaseObject(c4d.Onull)
            targetLight.SetName('Target for Lights (St with 1O, 1S, 1B)')
            doc.InsertObject(targetLight)
            targetLight[c4d.ID_BASEOBJECT_USECOLOR] = 2
            targetLight[c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(0.933, 0.894, 0.212)
            targetLight[c4d.NULLOBJECT_ICONCOL] = True

            studio = c4d.BaseObject(st_ui.STUDIO)
            studio.SetName('Studio with 1O, 1S, 1B')
            doc.InsertObject(studio)

            studio[st_ui.ST_MODE] = 1
            studio[st_ui.ST_WIDTH] = 400
            studio[st_ui.ST_HIDTH] = 590
            studio[st_ui.ST_DEFTH] = 450
            studio[st_ui.ST_ROUNDING] = 295
            studio[st_ui.ST_SUB_RENDER] = 3

            sb_1 = c4d.BaseObject(sb_ui.SBOX)
            sb_1.SetName('Softbox 1')
            doc.InsertObject(sb_1)

            sb_1[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(-421, 177, -122)
            sb_1[sb_ui.SB_WIDTH] = 815
            sb_1[sb_ui.SB_HIDTH] = 228
            sb_1[sb_ui.SB_DIST] = 498

            c4d.CallButton(sb_1, sb_ui.SB_ADD_TARGET_TAG)
            c4d.EventAdd()
            target_sb_1 = sb_1.GetTag(5676)
            target_sb_1[c4d.TARGETEXPRESSIONTAG_LINK] = targetLight

            sb_1[sb_ui.SB_LIGHT_COLOR] = c4d.Vector(0.925, 0.803, 0.539)
            sb_1[sb_ui.SB_BRIGHTNESS] = 1.4


            oh_1 = c4d.BaseObject(oh_ui.OVERHEAD)
            oh_1.SetName('Overhead Softbox 1')
            doc.InsertObject(oh_1)

            oh_1[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(0, 300, 0)
            oh_1[oh_ui.OH_WIDTH] = 483
            oh_1[oh_ui.OH_HIDTH] = 483
            oh_1[oh_ui.OH_DIST] = 227.5
            oh_1[oh_ui.OH_LIGHT_COLOR] = c4d.Vector(1, 0, 0)
            oh_1[oh_ui.OH_BRIGHTNESS] = 1.1
            oh_1[oh_ui.OH_LIGHT_SHADOW_DENSITY] = 0.86

            gl = c4d.BaseObject(gl_ui.GLOBALLIGHT)
            gl.SetName('Global Light')
            doc.InsertObject(gl)

            gl[gl_ui.GL_USED] = True
            gl[gl_ui.GL_LINK] = sb_1
            gl[gl_ui.GL_INVERT_COLOR] = True
            gl[gl_ui.GL_LIGHT_STR] = 0.4

            bc = c4d.BaseObject(bc_ui.BOUNCE)
            bc.SetName('BounceCard')
            doc.InsertObject(bc)

            bc[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(99.744, 115.69, 0)

            c4d.CallButton(bc, bc_ui.BC_ADD_TARGET_TAG)
            c4d.EventAdd()
            target_bc = bc.GetTag(5676)
            target_bc[c4d.TARGETEXPRESSIONTAG_LINK] = targetLight

            bc[bc_ui.BC_WIDTH] = 272
            bc[bc_ui.BC_HIDTH] = 143
            bc[bc_ui.BC_LIGHT_COLOR] = c4d.Vector(0.582, 0.892, 0.97)

            c4d.EventAdd()

        if id == pre_ui.PRESET_5:

            targetLight = c4d.BaseObject(c4d.Onull)
            targetLight.SetName('Target for Lights (St with 2S)')
            doc.InsertObject(targetLight)
            targetLight[c4d.ID_BASEOBJECT_USECOLOR] = 2
            targetLight[c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(0.933, 0.894, 0.212)
            targetLight[c4d.NULLOBJECT_ICONCOL] = True

            studio = c4d.BaseObject(st_ui.STUDIO)
            studio.SetName('Studio with 2S')
            doc.InsertObject(studio)

            studio[st_ui.ST_MODE] = 1
            studio[st_ui.ST_WIDTH] = 400
            studio[st_ui.ST_HIDTH] = 590
            studio[st_ui.ST_DEFTH] = 450
            studio[st_ui.ST_ROUNDING] = 295
            studio[st_ui.ST_SUB_RENDER] = 3

            sb_1 = c4d.BaseObject(sb_ui.SBOX)
            sb_1.SetName('Softbox 1')
            doc.InsertObject(sb_1)

            sb_1[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(-142, 131, -125)
            sb_1[sb_ui.SB_WIDTH] = 283
            sb_1[sb_ui.SB_HIDTH] = 228
            sb_1[sb_ui.SB_DIST] = 228

            c4d.CallButton(sb_1, sb_ui.SB_ADD_TARGET_TAG)
            c4d.EventAdd()
            target_sb_1 = sb_1.GetTag(5676)
            target_sb_1[c4d.TARGETEXPRESSIONTAG_LINK] = targetLight

            sb_1[sb_ui.SB_LIGHT_COLOR] = c4d.Vector(0.925, 0.925, 0.925)
            sb_1[sb_ui.SB_BRIGHTNESS] = 0.94

            sb_2 = c4d.BaseObject(sb_ui.SBOX)
            sb_2.SetName('Softbox 2')
            doc.InsertObject(sb_2)

            sb_2[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(98, 273, 104)
            sb_2[sb_ui.SB_MODE] = 1
            sb_2[sb_ui.SB_WIDTH] = 280
            sb_2[sb_ui.SB_DIST] = 288

            c4d.CallButton(sb_2, sb_ui.SB_ADD_TARGET_TAG)
            c4d.EventAdd()
            target_sb_2 = sb_2.GetTag(5676)
            target_sb_2[c4d.TARGETEXPRESSIONTAG_LINK] = targetLight

            sb_2[sb_ui.SB_LIGHT_COLOR] = c4d.Vector(0.765, 0.9, 0.821)
            sb_2[sb_ui.SB_BRIGHTNESS] = 0.8

            gl = c4d.BaseObject(gl_ui.GLOBALLIGHT)
            gl.SetName('Global Light')
            doc.InsertObject(gl)

            gl[gl_ui.GL_USED] = True
            gl[gl_ui.GL_LINK] = sb_2
            gl[gl_ui.GL_INVERT_COLOR] = True
            gl[gl_ui.GL_LIGHT_STR] = 0.1

            c4d.EventAdd()

        if id == pre_ui.PRESET_6:

            targetLight = c4d.BaseObject(c4d.Onull)
            targetLight.SetName('Target for Lights (St with 3S)')
            doc.InsertObject(targetLight)
            targetLight[c4d.ID_BASEOBJECT_USECOLOR] = 2
            targetLight[c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(0.933, 0.894, 0.212)
            targetLight[c4d.NULLOBJECT_ICONCOL] = True

            studio = c4d.BaseObject(st_ui.STUDIO)
            studio.SetName('Studio with 3S')
            doc.InsertObject(studio)

            studio[st_ui.ST_MODE] = 1
            studio[st_ui.ST_WIDTH] = 400
            studio[st_ui.ST_HIDTH] = 590
            studio[st_ui.ST_DEFTH] = 450
            studio[st_ui.ST_ROUNDING] = 295
            studio[st_ui.ST_SUB_RENDER] = 3

            sb_1 = c4d.BaseObject(sb_ui.SBOX)
            sb_1.SetName('Softbox 1')
            doc.InsertObject(sb_1)

            sb_1[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(-238, 320, 233)
            sb_1[sb_ui.SB_WIDTH] = 282
            sb_1[sb_ui.SB_HIDTH] = 228
            sb_1[sb_ui.SB_DIST] = 287

            c4d.CallButton(sb_1, sb_ui.SB_ADD_TARGET_TAG)
            c4d.EventAdd()
            target_sb_1 = sb_1.GetTag(5676)
            target_sb_1[c4d.TARGETEXPRESSIONTAG_LINK] = targetLight

            sb_1[sb_ui.SB_LIGHT_COLOR] = c4d.Vector(0.925, 0.925, 0.925)
            sb_1[sb_ui.SB_BRIGHTNESS] = 0.94

            sb_2 = c4d.BaseObject(sb_ui.SBOX)
            sb_2.SetName('Softbox 2')
            doc.InsertObject(sb_2)

            sb_2[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(238, 320, 233)
            sb_2[sb_ui.SB_WIDTH] = 282
            sb_2[sb_ui.SB_HIDTH] = 228
            sb_2[sb_ui.SB_DIST] = 287

            c4d.CallButton(sb_2, sb_ui.SB_ADD_TARGET_TAG)
            c4d.EventAdd()
            target_sb_2 = sb_2.GetTag(5676)
            target_sb_2[c4d.TARGETEXPRESSIONTAG_LINK] = targetLight

            sb_2[sb_ui.SB_LIGHT_COLOR] = c4d.Vector(0.925, 0.925, 0.925)
            sb_2[sb_ui.SB_BRIGHTNESS] = 0.8

            sb_3 = c4d.BaseObject(sb_ui.SBOX)
            sb_3.SetName('Softbox FrontTop')
            doc.InsertObject(sb_3)

            sb_3[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(0, 270, -275)
            sb_3[sb_ui.SB_WIDTH] = 692
            sb_3[sb_ui.SB_HIDTH] = 228
            sb_3[sb_ui.SB_DIST] = 484

            c4d.CallButton(sb_3, sb_ui.SB_ADD_TARGET_TAG)
            c4d.EventAdd()
            target_sb_3 = sb_3.GetTag(5676)
            target_sb_3[c4d.TARGETEXPRESSIONTAG_LINK] = targetLight

            sb_3[sb_ui.SB_LIGHT_COLOR] = c4d.Vector(0.925, 0.925, 0.925)
            sb_3[sb_ui.SB_BRIGHTNESS] = 0.94

            gl = c4d.BaseObject(gl_ui.GLOBALLIGHT)
            gl.SetName('Global Light')
            doc.InsertObject(gl)

            gl[gl_ui.GL_LIGHT_COLOR] = c4d.Vector(0.765, 0.871, 0.9)
            gl[gl_ui.GL_LIGHT_STR] = 0.4

            c4d.EventAdd()

        if id == pre_ui.PRESET_7:

            studio = c4d.BaseObject(st_ui.STUDIO)
            studio.SetName('Studio with 3S, 1O')
            doc.InsertObject(studio)

            studio[st_ui.ST_MODE] = 1
            studio[st_ui.ST_WIDTH] = 400
            studio[st_ui.ST_HIDTH] = 590
            studio[st_ui.ST_DEFTH] = 450
            studio[st_ui.ST_ROUNDING] = 295
            studio[st_ui.ST_SUB_RENDER] = 3

            sb_1 = c4d.BaseObject(sb_ui.SBOX)
            sb_1.SetName('Softbox 1')
            doc.InsertObject(sb_1)

            sb_1[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(-413, 254, 0)
            sb_1[c4d.ID_BASEOBJECT_REL_ROTATION] = c4d.Vector(math.radians(-89), math.radians(-8), 0)
            sb_1[sb_ui.SB_WIDTH] = 500
            sb_1[sb_ui.SB_HIDTH] = 500
            sb_1[sb_ui.SB_DIST] = 400
            sb_1[sb_ui.SB_LIGHT_COLOR] = c4d.Vector(0.925, 0.925, 0.925)
            sb_1[sb_ui.SB_BRIGHTNESS] = 0.94

            sb_2 = c4d.BaseObject(sb_ui.SBOX)
            sb_2.SetName('Softbox 2')
            doc.InsertObject(sb_2)

            sb_2[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(413, 254, 0)
            sb_2[c4d.ID_BASEOBJECT_REL_ROTATION] = c4d.Vector(math.radians(89), math.radians(-8), 0)
            sb_2[sb_ui.SB_WIDTH] = 500
            sb_2[sb_ui.SB_HIDTH] = 500
            sb_2[sb_ui.SB_DIST] = 400
            sb_2[sb_ui.SB_LIGHT_COLOR] = c4d.Vector(0.925, 0.925, 0.925)
            sb_2[sb_ui.SB_BRIGHTNESS] = 0.9

            sb_3 = c4d.BaseObject(sb_ui.SBOX)
            sb_3.SetName('Softbox FrontTop')
            doc.InsertObject(sb_3)

            sb_3[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(0, 232, -814)
            sb_3[c4d.ID_BASEOBJECT_REL_ROTATION] = c4d.Vector(0, math.radians(-2), 0)
            sb_3[sb_ui.SB_WIDTH] = 800
            sb_3[sb_ui.SB_HIDTH] = 500
            sb_3[sb_ui.SB_DIST] = 1000
            sb_3[sb_ui.SB_LIGHT_COLOR] = c4d.Vector(0.925, 0.925, 0.925)
            sb_3[sb_ui.SB_BRIGHTNESS] = 0.94
            sb_3[sb_ui.SB_V_EDITOR] = False

            oh_1 = c4d.BaseObject(oh_ui.OVERHEAD)
            oh_1.SetName('Overhead Softbox 1')
            doc.InsertObject(oh_1)

            oh_1[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(0, 500, 0)
            oh_1[oh_ui.OH_WIDTH] = 730
            oh_1[oh_ui.OH_HIDTH] = 450
            oh_1[oh_ui.OH_DIST] = 478
            oh_1[oh_ui.OH_BRIGHTNESS] = 0.9
            oh_1[oh_ui.OH_LIGHT_COLOR] = c4d.Vector(0.91, 0.982, 1)

            gl = c4d.BaseObject(gl_ui.GLOBALLIGHT)
            gl.SetName('Global Light')
            doc.InsertObject(gl)

            gl[gl_ui.GL_LIGHT_COLOR] = c4d.Vector(0.765, 0.871, 0.9)
            gl[gl_ui.GL_LIGHT_STR] = 0.4

            c4d.EventAdd()

        if id == pre_ui.PRESET_8:

            targetLight = c4d.BaseObject(c4d.Onull)
            targetLight.SetName('Target for Lights (St with 1S)')
            doc.InsertObject(targetLight)
            targetLight[c4d.ID_BASEOBJECT_USECOLOR] = 2
            targetLight[c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(0.933, 0.894, 0.212)
            targetLight[c4d.NULLOBJECT_ICONCOL] = True

            studio = c4d.BaseObject(st_ui.STUDIO)
            studio.SetName('Studio with 1S')
            doc.InsertObject(studio)

            studio[st_ui.ST_MODE] = 1
            studio[st_ui.ST_WIDTH] = 400
            studio[st_ui.ST_HIDTH] = 590
            studio[st_ui.ST_DEFTH] = 450
            studio[st_ui.ST_ROUNDING] = 295
            studio[st_ui.ST_SUB_RENDER] = 3

            sb_1 = c4d.BaseObject(sb_ui.SBOX)
            sb_1.SetName('Softbox 1')
            doc.InsertObject(sb_1)

            sb_1[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(-150, 240, 120)
            sb_1[sb_ui.SB_MODE] = 1
            sb_1[sb_ui.SB_WIDTH] = 312
            sb_1[sb_ui.SB_DIST] = 370

            c4d.CallButton(sb_1, sb_ui.SB_ADD_TARGET_TAG)
            c4d.EventAdd()
            target_sb_1 = sb_1.GetTag(5676)
            target_sb_1[c4d.TARGETEXPRESSIONTAG_LINK] = targetLight

            sb_1[sb_ui.SB_LIGHT_COLOR] = c4d.Vector(0.903, 0.645, 0.506)
            sb_1[sb_ui.SB_BRIGHTNESS] = 1.15

            gl = c4d.BaseObject(gl_ui.GLOBALLIGHT)
            gl.SetName('Global Light')
            doc.InsertObject(gl)

            gl[gl_ui.GL_USED] = True
            gl[gl_ui.GL_LINK] = sb_1
            gl[gl_ui.GL_INVERT_COLOR] = True
            gl[gl_ui.GL_LIGHT_STR] = 0.4

            c4d.EventAdd()

        if id == pre_ui.PRESET_9:

            studio = c4d.BaseObject(st_ui.STUDIO)
            studio.SetName('Studio with 2O')
            doc.InsertObject(studio)

            studio[st_ui.ST_MODE] = 1
            studio[st_ui.ST_WIDTH] = 400
            studio[st_ui.ST_HIDTH] = 590
            studio[st_ui.ST_DEFTH] = 450
            studio[st_ui.ST_ROUNDING] = 295
            studio[st_ui.ST_SUB_RENDER] = 3

            oh_1 = c4d.BaseObject(oh_ui.OVERHEAD)
            oh_1.SetName('Overhead Softbox 1')
            doc.InsertObject(oh_1)

            oh_1[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(0, 314, 0)
            oh_1[oh_ui.OH_WIDTH] = 394
            oh_1[oh_ui.OH_HIDTH] = 312
            oh_1[oh_ui.OH_DIST] = 427
            oh_1[oh_ui.OH_BRIGHTNESS] = 1
            oh_1[oh_ui.OH_LIGHT_COLOR] = c4d.Vector(0.871, 0.747, 0.658)

            oh_2 = c4d.BaseObject(oh_ui.OVERHEAD)
            oh_2.SetName('Overhead Softbox 2')
            doc.InsertObject(oh_2)

            oh_2[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(0, 320, 280)
            oh_2[c4d.ID_BASEOBJECT_REL_ROTATION] = c4d.Vector(0, math.radians(-16), 0)
            oh_2[oh_ui.OH_WIDTH] = 860
            oh_2[oh_ui.OH_HIDTH] = 222
            oh_2[oh_ui.OH_DIST] = 450
            oh_2[oh_ui.OH_BRIGHTNESS] = 0.6
            oh_2[oh_ui.OH_LIGHT_COLOR] = c4d.Vector(0.842, 0.892, 0.946)

            gl = c4d.BaseObject(gl_ui.GLOBALLIGHT)
            gl.SetName('Global Light')
            doc.InsertObject(gl)

            gl[gl_ui.GL_LIGHT_COLOR] = c4d.Vector(0.619, 0.821, 0.914)
            gl[gl_ui.GL_LIGHT_STR] = 0.4

            c4d.EventAdd()

        if id == pre_ui.PRESET_10:

            studio = c4d.BaseObject(st_ui.STUDIO)
            studio.SetName('Studio with 1O')
            doc.InsertObject(studio)

            studio[st_ui.ST_MODE] = 1
            studio[st_ui.ST_WIDTH] = 400
            studio[st_ui.ST_HIDTH] = 590
            studio[st_ui.ST_DEFTH] = 450
            studio[st_ui.ST_ROUNDING] = 295
            studio[st_ui.ST_SUB_RENDER] = 3

            oh_1 = c4d.BaseObject(oh_ui.OVERHEAD)
            oh_1.SetName('Overhead Softbox 1')
            doc.InsertObject(oh_1)

            oh_1[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(0, 320, 280)
            oh_1[c4d.ID_BASEOBJECT_REL_ROTATION] = c4d.Vector(0, math.radians(-16), 0)
            oh_1[oh_ui.OH_WIDTH] = 860
            oh_1[oh_ui.OH_HIDTH] = 222
            oh_1[oh_ui.OH_DIST] = 450
            oh_1[oh_ui.OH_BRIGHTNESS] = 1.1
            oh_1[oh_ui.OH_LIGHT_COLOR] = c4d.Vector(0.842, 0.892, 0.946)

            gl = c4d.BaseObject(gl_ui.GLOBALLIGHT)
            gl.SetName('Global Light')
            doc.InsertObject(gl)

            gl[gl_ui.GL_LIGHT_COLOR] = c4d.Vector(0.619, 0.821, 0.914)
            gl[gl_ui.GL_LIGHT_STR] = 0.25

            c4d.EventAdd()

        if id == pre_ui.PRESET_11:

            studio = c4d.BaseObject(st_ui.STUDIO)
            studio.SetName('Studio with 2S')
            doc.InsertObject(studio)

            studio[st_ui.ST_MODE] = 1
            studio[st_ui.ST_WIDTH] = 400
            studio[st_ui.ST_HIDTH] = 590
            studio[st_ui.ST_DEFTH] = 450
            studio[st_ui.ST_ROUNDING] = 295
            studio[st_ui.ST_SUB_RENDER] = 3

            sb_1 = c4d.BaseObject(sb_ui.SBOX)
            sb_1.SetName('Softbox 1')
            doc.InsertObject(sb_1)

            sb_1[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(-413, 254, 0)
            sb_1[c4d.ID_BASEOBJECT_REL_ROTATION] = c4d.Vector(math.radians(-89), math.radians(-8), 0)
            sb_1[sb_ui.SB_WIDTH] = 500
            sb_1[sb_ui.SB_HIDTH] = 500
            sb_1[sb_ui.SB_DIST] = 400
            sb_1[sb_ui.SB_LIGHT_COLOR] = c4d.Vector(0.9, 0.653, 0.405)
            sb_1[sb_ui.SB_BRIGHTNESS] = 1

            sb_2 = c4d.BaseObject(sb_ui.SBOX)
            sb_2.SetName('Softbox 2')
            doc.InsertObject(sb_2)

            sb_2[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(413, 254, 0)
            sb_2[c4d.ID_BASEOBJECT_REL_ROTATION] = c4d.Vector(math.radians(89), math.radians(-8), 0)
            sb_2[sb_ui.SB_WIDTH] = 500
            sb_2[sb_ui.SB_HIDTH] = 500
            sb_2[sb_ui.SB_DIST] = 400
            sb_2[sb_ui.SB_USED] = True
            sb_2[sb_ui.SB_LINK] = sb_1
            sb_2[sb_ui.SB_INVERT_COLOR] = True
            sb_2[sb_ui.SB_BRIGHTNESS] = 1

            gl = c4d.BaseObject(gl_ui.GLOBALLIGHT)
            gl.SetName('Global Light')
            doc.InsertObject(gl)

            gl[gl_ui.GL_LIGHT_COLOR] = c4d.Vector(0.619, 0.821, 0.914)
            gl[gl_ui.GL_LIGHT_STR] = 0.20

            c4d.EventAdd()

        if id == pre_ui.PRESET_12:

            targetLight = c4d.BaseObject(c4d.Onull)
            targetLight.SetName('Target for Lights (St with 1S)')
            doc.InsertObject(targetLight)
            targetLight[c4d.ID_BASEOBJECT_USECOLOR] = 2
            targetLight[c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(0.933, 0.894, 0.212)
            targetLight[c4d.NULLOBJECT_ICONCOL] = True

            studio = c4d.BaseObject(st_ui.STUDIO)
            studio.SetName('Studio with 1S')
            doc.InsertObject(studio)

            studio[st_ui.ST_MODE] = 1
            studio[st_ui.ST_WIDTH] = 400
            studio[st_ui.ST_HIDTH] = 590
            studio[st_ui.ST_DEFTH] = 450
            studio[st_ui.ST_ROUNDING] = 295
            studio[st_ui.ST_SUB_RENDER] = 3

            sb_1 = c4d.BaseObject(sb_ui.SBOX)
            sb_1.SetName('Softbox 1')
            doc.InsertObject(sb_1)

            sb_1[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(-110, 293, -145)
            sb_1[sb_ui.SB_MODE] = 1
            sb_1[sb_ui.SB_WIDTH] = 312
            sb_1[sb_ui.SB_DIST] = 370

            c4d.CallButton(sb_1, sb_ui.SB_ADD_TARGET_TAG)
            c4d.EventAdd()
            target_sb_1 = sb_1.GetTag(5676)
            target_sb_1[c4d.TARGETEXPRESSIONTAG_LINK] = targetLight

            sb_1[sb_ui.SB_LIGHT_COLOR] = c4d.Vector(0.9, 0.855, 0.765)
            sb_1[sb_ui.SB_BRIGHTNESS] = 1.15

            gl = c4d.BaseObject(gl_ui.GLOBALLIGHT)
            gl.SetName('Global Light')
            doc.InsertObject(gl)

            gl[gl_ui.GL_USED] = True
            gl[gl_ui.GL_LINK] = sb_1
            gl[gl_ui.GL_INVERT_COLOR] = True
            gl[gl_ui.GL_LIGHT_STR] = 0.4

            c4d.EventAdd()

        if id == pre_ui.PRESET_13:

            targetLight = c4d.BaseObject(c4d.Onull)
            targetLight.SetName('Target for Lights (St with 1S, 1O)')
            doc.InsertObject(targetLight)
            targetLight[c4d.ID_BASEOBJECT_USECOLOR] = 2
            targetLight[c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(0.933, 0.894, 0.212)
            targetLight[c4d.NULLOBJECT_ICONCOL] = True

            studio = c4d.BaseObject(st_ui.STUDIO)
            studio.SetName('Studio with 1S, 1O')
            doc.InsertObject(studio)

            studio[st_ui.ST_MODE] = 1
            studio[st_ui.ST_WIDTH] = 400
            studio[st_ui.ST_HIDTH] = 590
            studio[st_ui.ST_DEFTH] = 450
            studio[st_ui.ST_ROUNDING] = 295
            studio[st_ui.ST_SUB_RENDER] = 3

            sb_1 = c4d.BaseObject(sb_ui.SBOX)
            sb_1.SetName('Softbox 1')
            doc.InsertObject(sb_1)

            sb_1[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(-246, 170, -134)
            sb_1[sb_ui.SB_WIDTH] = 288
            sb_1[sb_ui.SB_HIDTH] = 288
            sb_1[sb_ui.SB_DIST] = 260

            c4d.CallButton(sb_1, sb_ui.SB_ADD_TARGET_TAG)
            c4d.EventAdd()
            target_sb_1 = sb_1.GetTag(5676)
            target_sb_1[c4d.TARGETEXPRESSIONTAG_LINK] = targetLight

            sb_1[sb_ui.SB_LIGHT_COLOR] = c4d.Vector(1, 0.959, 0.91)
            sb_1[sb_ui.SB_BRIGHTNESS] = 1

            oh_1 = c4d.BaseObject(oh_ui.OVERHEAD)
            oh_1.SetName('Overhead Softbox 1')
            doc.InsertObject(oh_1)

            oh_1[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(0, 320, 280)
            oh_1[c4d.ID_BASEOBJECT_REL_ROTATION] = c4d.Vector(0, math.radians(-16), 0)
            oh_1[oh_ui.OH_WIDTH] = 860
            oh_1[oh_ui.OH_HIDTH] = 222
            oh_1[oh_ui.OH_DIST] = 450
            oh_1[oh_ui.OH_BRIGHTNESS] = 1.1
            oh_1[oh_ui.OH_LIGHT_COLOR] = c4d.Vector(0.855, 0.902, 0.95)

            gl = c4d.BaseObject(gl_ui.GLOBALLIGHT)
            gl.SetName('Global Light')
            doc.InsertObject(gl)

            gl[gl_ui.GL_LIGHT_COLOR] = c4d.Vector(0.914, 0.771, 0.619)
            gl[gl_ui.GL_LIGHT_STR] = 0.25

            c4d.EventAdd()

        if id == pre_ui.PRESET_14:

            targetLight = c4d.BaseObject(c4d.Onull)
            targetLight.SetName('Target for Lights (St with 1S, 1O)')
            doc.InsertObject(targetLight)
            targetLight[c4d.ID_BASEOBJECT_USECOLOR] = 2
            targetLight[c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(0.933, 0.894, 0.212)
            targetLight[c4d.NULLOBJECT_ICONCOL] = True

            studio = c4d.BaseObject(st_ui.STUDIO)
            studio.SetName('Studio with 1S, 1O')
            doc.InsertObject(studio)

            studio[st_ui.ST_MODE] = 1
            studio[st_ui.ST_WIDTH] = 400
            studio[st_ui.ST_HIDTH] = 590
            studio[st_ui.ST_DEFTH] = 450
            studio[st_ui.ST_ROUNDING] = 295
            studio[st_ui.ST_SUB_RENDER] = 3

            sb_1 = c4d.BaseObject(sb_ui.SBOX)
            sb_1.SetName('Softbox 1')
            doc.InsertObject(sb_1)

            sb_1[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(-246, 170, -134)
            sb_1[sb_ui.SB_WIDTH] = 288
            sb_1[sb_ui.SB_HIDTH] = 288
            sb_1[sb_ui.SB_DIST] = 260

            c4d.CallButton(sb_1, sb_ui.SB_ADD_TARGET_TAG)
            c4d.EventAdd()
            target_sb_1 = sb_1.GetTag(5676)
            target_sb_1[c4d.TARGETEXPRESSIONTAG_LINK] = targetLight

            sb_1[sb_ui.SB_LIGHT_COLOR] = c4d.Vector(0.4, 1, 0.54)
            sb_1[sb_ui.SB_BRIGHTNESS] = 1

            sb_2 = c4d.BaseObject(sb_ui.SBOX)
            sb_2.SetName('Softbox 2')
            doc.InsertObject(sb_2)

            sb_2[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(246, 170, -134)
            sb_2[sb_ui.SB_WIDTH] = 288
            sb_2[sb_ui.SB_HIDTH] = 288
            sb_2[sb_ui.SB_DIST] = 260

            c4d.CallButton(sb_2, sb_ui.SB_ADD_TARGET_TAG)
            c4d.EventAdd()
            target_sb_2 = sb_2.GetTag(5676)
            target_sb_2[c4d.TARGETEXPRESSIONTAG_LINK] = targetLight

            sb_2[sb_ui.SB_USED] = True
            sb_2[sb_ui.SB_LINK] = sb_1
            sb_2[sb_ui.SB_BRIGHTNESS] = 1

            oh_1 = c4d.BaseObject(oh_ui.OVERHEAD)
            oh_1.SetName('Overhead Softbox 1')
            doc.InsertObject(oh_1)

            oh_1[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(0, 320, 280)
            oh_1[c4d.ID_BASEOBJECT_REL_ROTATION] = c4d.Vector(0, math.radians(-16), 0)
            oh_1[oh_ui.OH_WIDTH] = 860
            oh_1[oh_ui.OH_HIDTH] = 222
            oh_1[oh_ui.OH_DIST] = 450
            oh_1[oh_ui.OH_BRIGHTNESS] = 0.7
            oh_1[oh_ui.OH_LIGHT_COLOR] = c4d.Vector(0.855, 0.902, 0.95)
            oh_1[oh_ui.OH_USED] = True
            oh_1[oh_ui.OH_INVERT_COLOR] = True
            oh_1[oh_ui.OH_LINK] = sb_1

            c4d.EventAdd()

        if id == pre_ui.PRESET_15:

            targetLight = c4d.BaseObject(c4d.Onull)
            targetLight.SetName('Target for Lights (St with 1S, 1O)')
            doc.InsertObject(targetLight)
            targetLight[c4d.ID_BASEOBJECT_USECOLOR] = 2
            targetLight[c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(0.933, 0.894, 0.212)
            targetLight[c4d.NULLOBJECT_ICONCOL] = True

            studio = c4d.BaseObject(st_ui.STUDIO)
            studio.SetName('Studio with 1S, 1O')
            doc.InsertObject(studio)

            studio[st_ui.ST_MODE] = 1
            studio[st_ui.ST_WIDTH] = 400
            studio[st_ui.ST_HIDTH] = 590
            studio[st_ui.ST_DEFTH] = 450
            studio[st_ui.ST_ROUNDING] = 295
            studio[st_ui.ST_SUB_RENDER] = 3

            sb_1 = c4d.BaseObject(sb_ui.SBOX)
            sb_1.SetName('Softbox 1')
            doc.InsertObject(sb_1)

            sb_1[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(-246, 170, -134)
            sb_1[sb_ui.SB_WIDTH] = 288
            sb_1[sb_ui.SB_HIDTH] = 288
            sb_1[sb_ui.SB_DIST] = 260

            c4d.CallButton(sb_1, sb_ui.SB_ADD_TARGET_TAG)
            c4d.EventAdd()
            target_sb_1 = sb_1.GetTag(5676)
            target_sb_1[c4d.TARGETEXPRESSIONTAG_LINK] = targetLight

            sb_1[sb_ui.SB_LIGHT_COLOR] = c4d.Vector(0.952, 1, 0.76)
            sb_1[sb_ui.SB_BRIGHTNESS] = 0.9

            sb_2 = c4d.BaseObject(sb_ui.SBOX)
            sb_2.SetName('Softbox 2')
            doc.InsertObject(sb_2)

            sb_2[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(246, 170, -134)
            sb_2[sb_ui.SB_WIDTH] = 288
            sb_2[sb_ui.SB_HIDTH] = 288
            sb_2[sb_ui.SB_DIST] = 260

            c4d.CallButton(sb_2, sb_ui.SB_ADD_TARGET_TAG)
            c4d.EventAdd()
            target_sb_2 = sb_2.GetTag(5676)
            target_sb_2[c4d.TARGETEXPRESSIONTAG_LINK] = targetLight

            sb_2[sb_ui.SB_USED] = True
            sb_2[sb_ui.SB_LINK] = sb_1
            sb_2[sb_ui.SB_BRIGHTNESS] = 0.8

            oh_1 = c4d.BaseObject(oh_ui.OVERHEAD)
            oh_1.SetName('Overhead Softbox 1')
            doc.InsertObject(oh_1)

            oh_1[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(0, 320, 280)
            oh_1[c4d.ID_BASEOBJECT_REL_ROTATION] = c4d.Vector(0, math.radians(-16), 0)
            oh_1[oh_ui.OH_WIDTH] = 860
            oh_1[oh_ui.OH_HIDTH] = 222
            oh_1[oh_ui.OH_DIST] = 450
            oh_1[oh_ui.OH_BRIGHTNESS] = 0.9
            oh_1[oh_ui.OH_LIGHT_COLOR] = c4d.Vector(0.855, 0.902, 0.95)
            oh_1[oh_ui.OH_USED] = True
            oh_1[oh_ui.OH_INVERT_COLOR] = True
            oh_1[oh_ui.OH_LINK] = sb_1

            c4d.EventAdd()

        if id == pre_ui.PRESET_16:

            targetLight = c4d.BaseObject(c4d.Onull)
            targetLight.SetName('Target for Lights (St with 1S, 1O)')
            doc.InsertObject(targetLight)
            targetLight[c4d.ID_BASEOBJECT_USECOLOR] = 2
            targetLight[c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(0.933, 0.894, 0.212)
            targetLight[c4d.NULLOBJECT_ICONCOL] = True

            studio = c4d.BaseObject(st_ui.STUDIO)
            studio.SetName('Studio with 1S, 1O')
            doc.InsertObject(studio)

            studio[st_ui.ST_MODE] = 1
            studio[st_ui.ST_WIDTH] = 400
            studio[st_ui.ST_HIDTH] = 590
            studio[st_ui.ST_DEFTH] = 450
            studio[st_ui.ST_ROUNDING] = 295
            studio[st_ui.ST_SUB_RENDER] = 3
            studio[st_ui.ST_STUDIO_COLOR] = c4d.Vector(0.961, 0.812, 0.204)

            sb_1 = c4d.BaseObject(sb_ui.SBOX)
            sb_1.SetName('Softbox 1')
            doc.InsertObject(sb_1)

            sb_1[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(-246, 170, -134)
            sb_1[sb_ui.SB_WIDTH] = 288
            sb_1[sb_ui.SB_HIDTH] = 288
            sb_1[sb_ui.SB_DIST] = 260

            c4d.CallButton(sb_1, sb_ui.SB_ADD_TARGET_TAG)
            c4d.EventAdd()
            target_sb_1 = sb_1.GetTag(5676)
            target_sb_1[c4d.TARGETEXPRESSIONTAG_LINK] = targetLight

            sb_1[sb_ui.SB_LIGHT_COLOR] = c4d.Vector(1, 1, 1)
            sb_1[sb_ui.SB_BRIGHTNESS] = 0.9

            sb_2 = c4d.BaseObject(sb_ui.SBOX)
            sb_2.SetName('Softbox 2')
            doc.InsertObject(sb_2)

            sb_2[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(246, 170, -134)
            sb_2[sb_ui.SB_WIDTH] = 288
            sb_2[sb_ui.SB_HIDTH] = 288
            sb_2[sb_ui.SB_DIST] = 260

            c4d.CallButton(sb_2, sb_ui.SB_ADD_TARGET_TAG)
            c4d.EventAdd()
            target_sb_2 = sb_2.GetTag(5676)
            target_sb_2[c4d.TARGETEXPRESSIONTAG_LINK] = targetLight

            sb_2[sb_ui.SB_USED] = True
            sb_2[sb_ui.SB_LINK] = sb_1
            sb_2[sb_ui.SB_BRIGHTNESS] = 0.8

            oh_1 = c4d.BaseObject(oh_ui.OVERHEAD)
            oh_1.SetName('Overhead Softbox 1')
            doc.InsertObject(oh_1)

            oh_1[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(0, 320, 280)
            oh_1[c4d.ID_BASEOBJECT_REL_ROTATION] = c4d.Vector(0, math.radians(-16), 0)
            oh_1[oh_ui.OH_WIDTH] = 860
            oh_1[oh_ui.OH_HIDTH] = 222
            oh_1[oh_ui.OH_DIST] = 450
            oh_1[oh_ui.OH_BRIGHTNESS] = 0.9
            oh_1[oh_ui.OH_LIGHT_COLOR] = c4d.Vector(0.855, 0.902, 0.95)
            oh_1[oh_ui.OH_USED] = True
            oh_1[oh_ui.OH_INVERT_COLOR] = True
            oh_1[oh_ui.OH_LINK] = sb_1

            c4d.EventAdd()

        if id == pre_ui.PRESET_17:

            targetLight = c4d.BaseObject(c4d.Onull)
            targetLight.SetName('Target for Lights (St with 1S, 1O)')
            doc.InsertObject(targetLight)
            targetLight[c4d.ID_BASEOBJECT_USECOLOR] = 2
            targetLight[c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(0.933, 0.894, 0.212)
            targetLight[c4d.NULLOBJECT_ICONCOL] = True

            studio = c4d.BaseObject(st_ui.STUDIO)
            studio.SetName('Studio with 1S, 1O')
            doc.InsertObject(studio)

            studio[st_ui.ST_MODE] = 1
            studio[st_ui.ST_WIDTH] = 400
            studio[st_ui.ST_HIDTH] = 590
            studio[st_ui.ST_DEFTH] = 450
            studio[st_ui.ST_ROUNDING] = 295
            studio[st_ui.ST_SUB_RENDER] = 3
            studio[st_ui.ST_STUDIO_COLOR] = c4d.Vector(0.894, 0.067, 0.38)

            sb_1 = c4d.BaseObject(sb_ui.SBOX)
            sb_1.SetName('Softbox 1')
            doc.InsertObject(sb_1)

            sb_1[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(-246, 170, -134)
            sb_1[sb_ui.SB_WIDTH] = 288
            sb_1[sb_ui.SB_HIDTH] = 288
            sb_1[sb_ui.SB_DIST] = 260

            c4d.CallButton(sb_1, sb_ui.SB_ADD_TARGET_TAG)
            c4d.EventAdd()
            target_sb_1 = sb_1.GetTag(5676)
            target_sb_1[c4d.TARGETEXPRESSIONTAG_LINK] = targetLight

            sb_1[sb_ui.SB_LIGHT_COLOR] = c4d.Vector(1, 1, 1)
            sb_1[sb_ui.SB_BRIGHTNESS] = 0.9

            sb_2 = c4d.BaseObject(sb_ui.SBOX)
            sb_2.SetName('Softbox 2')
            doc.InsertObject(sb_2)

            sb_2[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(246, 170, -134)
            sb_2[sb_ui.SB_WIDTH] = 288
            sb_2[sb_ui.SB_HIDTH] = 288
            sb_2[sb_ui.SB_DIST] = 260

            c4d.CallButton(sb_2, sb_ui.SB_ADD_TARGET_TAG)
            c4d.EventAdd()
            target_sb_2 = sb_2.GetTag(5676)
            target_sb_2[c4d.TARGETEXPRESSIONTAG_LINK] = targetLight

            sb_2[sb_ui.SB_USED] = True
            sb_2[sb_ui.SB_LINK] = sb_1
            sb_2[sb_ui.SB_BRIGHTNESS] = 0.8

            oh_1 = c4d.BaseObject(oh_ui.OVERHEAD)
            oh_1.SetName('Overhead Softbox 1')
            doc.InsertObject(oh_1)

            oh_1[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(0, 320, 280)
            oh_1[c4d.ID_BASEOBJECT_REL_ROTATION] = c4d.Vector(0, math.radians(-16), 0)
            oh_1[oh_ui.OH_WIDTH] = 860
            oh_1[oh_ui.OH_HIDTH] = 222
            oh_1[oh_ui.OH_DIST] = 450
            oh_1[oh_ui.OH_BRIGHTNESS] = 0.9
            oh_1[oh_ui.OH_LIGHT_COLOR] = c4d.Vector(0.855, 0.902, 0.95)
            oh_1[oh_ui.OH_USED] = True
            oh_1[oh_ui.OH_INVERT_COLOR] = True
            oh_1[oh_ui.OH_LINK] = sb_1

            c4d.EventAdd()

        if id == pre_ui.PRESET_18:

            targetLight = c4d.BaseObject(c4d.Onull)
            targetLight.SetName('Target for Lights (St with 1S, 1O)')
            doc.InsertObject(targetLight)
            targetLight[c4d.ID_BASEOBJECT_USECOLOR] = 2
            targetLight[c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(0.933, 0.894, 0.212)
            targetLight[c4d.NULLOBJECT_ICONCOL] = True

            studio = c4d.BaseObject(st_ui.STUDIO)
            studio.SetName('Studio with 1S, 1O')
            doc.InsertObject(studio)

            studio[st_ui.ST_MODE] = 1
            studio[st_ui.ST_WIDTH] = 400
            studio[st_ui.ST_HIDTH] = 590
            studio[st_ui.ST_DEFTH] = 450
            studio[st_ui.ST_ROUNDING] = 295
            studio[st_ui.ST_SUB_RENDER] = 3
            studio[st_ui.ST_STUDIO_COLOR] = c4d.Vector(0.052, 0.088, 0.26)

            sb_1 = c4d.BaseObject(sb_ui.SBOX)
            sb_1.SetName('Softbox 1')
            doc.InsertObject(sb_1)

            sb_1[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(-246, 170, -134)
            sb_1[sb_ui.SB_WIDTH] = 288
            sb_1[sb_ui.SB_HIDTH] = 288
            sb_1[sb_ui.SB_DIST] = 260

            c4d.CallButton(sb_1, sb_ui.SB_ADD_TARGET_TAG)
            c4d.EventAdd()
            target_sb_1 = sb_1.GetTag(5676)
            target_sb_1[c4d.TARGETEXPRESSIONTAG_LINK] = targetLight

            sb_1[sb_ui.SB_LIGHT_COLOR] = c4d.Vector(1, 1, 1)
            sb_1[sb_ui.SB_BRIGHTNESS] = 0.9

            sb_2 = c4d.BaseObject(sb_ui.SBOX)
            sb_2.SetName('Softbox 2')
            doc.InsertObject(sb_2)

            sb_2[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(246, 170, -134)
            sb_2[sb_ui.SB_WIDTH] = 288
            sb_2[sb_ui.SB_HIDTH] = 288
            sb_2[sb_ui.SB_DIST] = 260

            c4d.CallButton(sb_2, sb_ui.SB_ADD_TARGET_TAG)
            c4d.EventAdd()
            target_sb_2 = sb_2.GetTag(5676)
            target_sb_2[c4d.TARGETEXPRESSIONTAG_LINK] = targetLight

            sb_2[sb_ui.SB_USED] = True
            sb_2[sb_ui.SB_LINK] = sb_1
            sb_2[sb_ui.SB_BRIGHTNESS] = 0.8

            oh_1 = c4d.BaseObject(oh_ui.OVERHEAD)
            oh_1.SetName('Overhead Softbox 1')
            doc.InsertObject(oh_1)

            oh_1[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(0, 320, 280)
            oh_1[c4d.ID_BASEOBJECT_REL_ROTATION] = c4d.Vector(0, math.radians(-16), 0)
            oh_1[oh_ui.OH_WIDTH] = 860
            oh_1[oh_ui.OH_HIDTH] = 222
            oh_1[oh_ui.OH_DIST] = 450
            oh_1[oh_ui.OH_BRIGHTNESS] = 0.9
            oh_1[oh_ui.OH_LIGHT_COLOR] = c4d.Vector(0.855, 0.902, 0.95)
            oh_1[oh_ui.OH_USED] = True
            oh_1[oh_ui.OH_INVERT_COLOR] = True
            oh_1[oh_ui.OH_LINK] = sb_1

            c4d.EventAdd()

        if id == pre_ui.PRESET_19:

            targetLight = c4d.BaseObject(c4d.Onull)
            targetLight.SetName('Target for Lights (St with 1S, 1O)')
            doc.InsertObject(targetLight)
            targetLight[c4d.ID_BASEOBJECT_USECOLOR] = 2
            targetLight[c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(0.933, 0.894, 0.212)
            targetLight[c4d.NULLOBJECT_ICONCOL] = True

            studio = c4d.BaseObject(st_ui.STUDIO)
            studio.SetName('Studio with 1S, 1O')
            doc.InsertObject(studio)

            studio[st_ui.ST_MODE] = 1
            studio[st_ui.ST_WIDTH] = 400
            studio[st_ui.ST_HIDTH] = 590
            studio[st_ui.ST_DEFTH] = 450
            studio[st_ui.ST_ROUNDING] = 295
            studio[st_ui.ST_SUB_RENDER] = 3
            studio[st_ui.ST_STUDIO_COLOR] = c4d.Vector(0.475, 0, 0.109)

            sb_1 = c4d.BaseObject(sb_ui.SBOX)
            sb_1.SetName('Softbox 1')
            doc.InsertObject(sb_1)

            sb_1[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(-246, 170, -134)
            sb_1[sb_ui.SB_WIDTH] = 288
            sb_1[sb_ui.SB_HIDTH] = 288
            sb_1[sb_ui.SB_DIST] = 260

            c4d.CallButton(sb_1, sb_ui.SB_ADD_TARGET_TAG)
            c4d.EventAdd()
            target_sb_1 = sb_1.GetTag(5676)
            target_sb_1[c4d.TARGETEXPRESSIONTAG_LINK] = targetLight

            sb_1[sb_ui.SB_LIGHT_COLOR] = c4d.Vector(1, 1, 1)
            sb_1[sb_ui.SB_BRIGHTNESS] = 0.9

            sb_2 = c4d.BaseObject(sb_ui.SBOX)
            sb_2.SetName('Softbox 2')
            doc.InsertObject(sb_2)

            sb_2[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(246, 170, -134)
            sb_2[sb_ui.SB_WIDTH] = 288
            sb_2[sb_ui.SB_HIDTH] = 288
            sb_2[sb_ui.SB_DIST] = 260

            c4d.CallButton(sb_2, sb_ui.SB_ADD_TARGET_TAG)
            c4d.EventAdd()
            target_sb_2 = sb_2.GetTag(5676)
            target_sb_2[c4d.TARGETEXPRESSIONTAG_LINK] = targetLight

            sb_2[sb_ui.SB_USED] = True
            sb_2[sb_ui.SB_LINK] = sb_1
            sb_2[sb_ui.SB_BRIGHTNESS] = 0.8

            oh_1 = c4d.BaseObject(oh_ui.OVERHEAD)
            oh_1.SetName('Overhead Softbox 1')
            doc.InsertObject(oh_1)

            oh_1[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(0, 320, 280)
            oh_1[c4d.ID_BASEOBJECT_REL_ROTATION] = c4d.Vector(0, math.radians(-16), 0)
            oh_1[oh_ui.OH_WIDTH] = 860
            oh_1[oh_ui.OH_HIDTH] = 222
            oh_1[oh_ui.OH_DIST] = 450
            oh_1[oh_ui.OH_BRIGHTNESS] = 0.9
            oh_1[oh_ui.OH_LIGHT_COLOR] = c4d.Vector(0.855, 0.902, 0.95)
            oh_1[oh_ui.OH_USED] = True
            oh_1[oh_ui.OH_INVERT_COLOR] = True
            oh_1[oh_ui.OH_LINK] = sb_1

            c4d.EventAdd()

        if id == pre_ui.PRESET_20:

            targetLight = c4d.BaseObject(c4d.Onull)
            targetLight.SetName('Target for Lights (St with 1S, 1O)')
            doc.InsertObject(targetLight)
            targetLight[c4d.ID_BASEOBJECT_USECOLOR] = 2
            targetLight[c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(0.933, 0.894, 0.212)
            targetLight[c4d.NULLOBJECT_ICONCOL] = True

            studio = c4d.BaseObject(st_ui.STUDIO)
            studio.SetName('Studio with 1S, 1O')
            doc.InsertObject(studio)

            studio[st_ui.ST_MODE] = 1
            studio[st_ui.ST_WIDTH] = 400
            studio[st_ui.ST_HIDTH] = 590
            studio[st_ui.ST_DEFTH] = 450
            studio[st_ui.ST_ROUNDING] = 295
            studio[st_ui.ST_SUB_RENDER] = 3
            studio[st_ui.ST_STUDIO_COLOR] = c4d.Vector(0.176, 0.545, 0.396)

            sb_1 = c4d.BaseObject(sb_ui.SBOX)
            sb_1.SetName('Softbox 1')
            doc.InsertObject(sb_1)

            sb_1[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(-246, 170, -134)
            sb_1[sb_ui.SB_WIDTH] = 288
            sb_1[sb_ui.SB_HIDTH] = 288
            sb_1[sb_ui.SB_DIST] = 260

            c4d.CallButton(sb_1, sb_ui.SB_ADD_TARGET_TAG)
            c4d.EventAdd()
            target_sb_1 = sb_1.GetTag(5676)
            target_sb_1[c4d.TARGETEXPRESSIONTAG_LINK] = targetLight

            sb_1[sb_ui.SB_LIGHT_COLOR] = c4d.Vector(1, 1, 1)
            sb_1[sb_ui.SB_BRIGHTNESS] = 0.9

            sb_2 = c4d.BaseObject(sb_ui.SBOX)
            sb_2.SetName('Softbox 2')
            doc.InsertObject(sb_2)

            sb_2[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(246, 170, -134)
            sb_2[sb_ui.SB_WIDTH] = 288
            sb_2[sb_ui.SB_HIDTH] = 288
            sb_2[sb_ui.SB_DIST] = 260

            c4d.CallButton(sb_2, sb_ui.SB_ADD_TARGET_TAG)
            c4d.EventAdd()
            target_sb_2 = sb_2.GetTag(5676)
            target_sb_2[c4d.TARGETEXPRESSIONTAG_LINK] = targetLight

            sb_2[sb_ui.SB_USED] = True
            sb_2[sb_ui.SB_LINK] = sb_1
            sb_2[sb_ui.SB_BRIGHTNESS] = 0.8

            oh_1 = c4d.BaseObject(oh_ui.OVERHEAD)
            oh_1.SetName('Overhead Softbox 1')
            doc.InsertObject(oh_1)

            oh_1[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(0, 320, 280)
            oh_1[c4d.ID_BASEOBJECT_REL_ROTATION] = c4d.Vector(0, math.radians(-16), 0)
            oh_1[oh_ui.OH_WIDTH] = 860
            oh_1[oh_ui.OH_HIDTH] = 222
            oh_1[oh_ui.OH_DIST] = 450
            oh_1[oh_ui.OH_BRIGHTNESS] = 0.9
            oh_1[oh_ui.OH_LIGHT_COLOR] = c4d.Vector(0.855, 0.902, 0.95)
            oh_1[oh_ui.OH_USED] = True
            oh_1[oh_ui.OH_INVERT_COLOR] = True
            oh_1[oh_ui.OH_LINK] = sb_1

            c4d.EventAdd()

        if id == pre_ui.PRESET_21:

            targetLight = c4d.BaseObject(c4d.Onull)
            targetLight.SetName('Target for Lights (St with 1S, 1O)')
            doc.InsertObject(targetLight)
            targetLight[c4d.ID_BASEOBJECT_USECOLOR] = 2
            targetLight[c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(0.933, 0.894, 0.212)
            targetLight[c4d.NULLOBJECT_ICONCOL] = True

            studio = c4d.BaseObject(st_ui.STUDIO)
            studio.SetName('Studio with 1S, 1O')
            doc.InsertObject(studio)

            studio[st_ui.ST_MODE] = 1
            studio[st_ui.ST_WIDTH] = 400
            studio[st_ui.ST_HIDTH] = 590
            studio[st_ui.ST_DEFTH] = 450
            studio[st_ui.ST_ROUNDING] = 295
            studio[st_ui.ST_SUB_RENDER] = 3
            studio[st_ui.ST_STUDIO_COLOR] = c4d.Vector(0.396, 0.314, 0.573)

            sb_1 = c4d.BaseObject(sb_ui.SBOX)
            sb_1.SetName('Softbox 1')
            doc.InsertObject(sb_1)

            sb_1[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(-246, 170, -134)
            sb_1[sb_ui.SB_WIDTH] = 288
            sb_1[sb_ui.SB_HIDTH] = 288
            sb_1[sb_ui.SB_DIST] = 260

            c4d.CallButton(sb_1, sb_ui.SB_ADD_TARGET_TAG)
            c4d.EventAdd()
            target_sb_1 = sb_1.GetTag(5676)
            target_sb_1[c4d.TARGETEXPRESSIONTAG_LINK] = targetLight

            sb_1[sb_ui.SB_LIGHT_COLOR] = c4d.Vector(1, 1, 1)
            sb_1[sb_ui.SB_BRIGHTNESS] = 0.9

            sb_2 = c4d.BaseObject(sb_ui.SBOX)
            sb_2.SetName('Softbox 2')
            doc.InsertObject(sb_2)

            sb_2[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(246, 170, -134)
            sb_2[sb_ui.SB_WIDTH] = 288
            sb_2[sb_ui.SB_HIDTH] = 288
            sb_2[sb_ui.SB_DIST] = 260

            c4d.CallButton(sb_2, sb_ui.SB_ADD_TARGET_TAG)
            c4d.EventAdd()
            target_sb_2 = sb_2.GetTag(5676)
            target_sb_2[c4d.TARGETEXPRESSIONTAG_LINK] = targetLight

            sb_2[sb_ui.SB_USED] = True
            sb_2[sb_ui.SB_LINK] = sb_1
            sb_2[sb_ui.SB_BRIGHTNESS] = 0.8

            oh_1 = c4d.BaseObject(oh_ui.OVERHEAD)
            oh_1.SetName('Overhead Softbox 1')
            doc.InsertObject(oh_1)

            oh_1[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(0, 320, 280)
            oh_1[c4d.ID_BASEOBJECT_REL_ROTATION] = c4d.Vector(0, math.radians(-16), 0)
            oh_1[oh_ui.OH_WIDTH] = 860
            oh_1[oh_ui.OH_HIDTH] = 222
            oh_1[oh_ui.OH_DIST] = 450
            oh_1[oh_ui.OH_BRIGHTNESS] = 0.9
            oh_1[oh_ui.OH_LIGHT_COLOR] = c4d.Vector(0.855, 0.902, 0.95)
            oh_1[oh_ui.OH_USED] = True
            oh_1[oh_ui.OH_INVERT_COLOR] = True
            oh_1[oh_ui.OH_LINK] = sb_1

            c4d.EventAdd()

        return True
#-------------------------------------------------------------------------------------------- Preset_Rays

#-------------------------------------------------------------------------------------------- Preset_Start
class Preset_Start(c4d.plugins.CommandData):

    dialog = None

    def Execute(self, doc):
        if self.dialog is None:
            self.dialog = Preset_Rays()
        return self.dialog.Open(c4d.DLG_TYPE_ASYNC, pre_ui.PRESET_RAYS, -1, -1, 300 , 400 , 0)
#-------------------------------------------------------------------------------------------- end Preset_Start

# инициализация компонентов
if __name__ == '__main__':

    dir, file = os.path.split(__file__)

    #-------------------------------------------------------------------- регистрация превью для пресетов

    Preset_Rays_1 = bitmaps.BaseBitmap()
    Preset_Rays_1.InitWith(os.path.join(dir, S.pathiconspreset, S.IconPreset_1))
    gui.RegisterIcon(pre_ui.PRESET_1, Preset_Rays_1)

    Preset_Rays_2 = bitmaps.BaseBitmap()
    Preset_Rays_2.InitWith(os.path.join(dir, S.pathiconspreset, S.IconPreset_2))
    gui.RegisterIcon(pre_ui.PRESET_2, Preset_Rays_2)

    Preset_Rays_3 = bitmaps.BaseBitmap()
    Preset_Rays_3.InitWith(os.path.join(dir, S.pathiconspreset, S.IconPreset_3))
    gui.RegisterIcon(pre_ui.PRESET_3, Preset_Rays_3)

    Preset_Rays_4 = bitmaps.BaseBitmap()
    Preset_Rays_4.InitWith(os.path.join(dir, S.pathiconspreset, S.IconPreset_4))
    gui.RegisterIcon(pre_ui.PRESET_4, Preset_Rays_4)

    Preset_Rays_5 = bitmaps.BaseBitmap()
    Preset_Rays_5.InitWith(os.path.join(dir, S.pathiconspreset, S.IconPreset_5))
    gui.RegisterIcon(pre_ui.PRESET_5, Preset_Rays_5)

    #--------------------------------------------------------------------

    Preset_Rays_6 = bitmaps.BaseBitmap()
    Preset_Rays_6.InitWith(os.path.join(dir, S.pathiconspreset, S.IconPreset_6))
    gui.RegisterIcon(pre_ui.PRESET_6, Preset_Rays_6)

    Preset_Rays_7 = bitmaps.BaseBitmap()
    Preset_Rays_7.InitWith(os.path.join(dir, S.pathiconspreset, S.IconPreset_7))
    gui.RegisterIcon(pre_ui.PRESET_7, Preset_Rays_7)

    Preset_Rays_8 = bitmaps.BaseBitmap()
    Preset_Rays_8.InitWith(os.path.join(dir, S.pathiconspreset, S.IconPreset_8))
    gui.RegisterIcon(pre_ui.PRESET_8, Preset_Rays_8)

    Preset_Rays_9 = bitmaps.BaseBitmap()
    Preset_Rays_9.InitWith(os.path.join(dir, S.pathiconspreset, S.IconPreset_9))
    gui.RegisterIcon(pre_ui.PRESET_9, Preset_Rays_9)

    Preset_Rays_10 = bitmaps.BaseBitmap()
    Preset_Rays_10.InitWith(os.path.join(dir, S.pathiconspreset, S.IconPreset_10))
    gui.RegisterIcon(pre_ui.PRESET_10, Preset_Rays_10)

    #--------------------------------------------------------------------

    Preset_Rays_11 = bitmaps.BaseBitmap()
    Preset_Rays_11.InitWith(os.path.join(dir, S.pathiconspreset, S.IconPreset_11))
    gui.RegisterIcon(pre_ui.PRESET_11, Preset_Rays_11)

    Preset_Rays_12 = bitmaps.BaseBitmap()
    Preset_Rays_12.InitWith(os.path.join(dir, S.pathiconspreset, S.IconPreset_12))
    gui.RegisterIcon(pre_ui.PRESET_12, Preset_Rays_12)

    Preset_Rays_13 = bitmaps.BaseBitmap()
    Preset_Rays_13.InitWith(os.path.join(dir, S.pathiconspreset, S.IconPreset_13))
    gui.RegisterIcon(pre_ui.PRESET_13, Preset_Rays_13)

    Preset_Rays_14 = bitmaps.BaseBitmap()
    Preset_Rays_14.InitWith(os.path.join(dir, S.pathiconspreset, S.IconPreset_14))
    gui.RegisterIcon(pre_ui.PRESET_14, Preset_Rays_14)

    Preset_Rays_15 = bitmaps.BaseBitmap()
    Preset_Rays_15.InitWith(os.path.join(dir, S.pathiconspreset, S.IconPreset_15))
    gui.RegisterIcon(pre_ui.PRESET_15, Preset_Rays_15)

    #--------------------------------------------------------------------

    Preset_Rays_16 = bitmaps.BaseBitmap()
    Preset_Rays_16.InitWith(os.path.join(dir, S.pathiconspreset, S.IconPreset_16))
    gui.RegisterIcon(pre_ui.PRESET_16, Preset_Rays_16)

    Preset_Rays_17 = bitmaps.BaseBitmap()
    Preset_Rays_17.InitWith(os.path.join(dir, S.pathiconspreset, S.IconPreset_17))
    gui.RegisterIcon(pre_ui.PRESET_17, Preset_Rays_17)

    Preset_Rays_18 = bitmaps.BaseBitmap()
    Preset_Rays_18.InitWith(os.path.join(dir, S.pathiconspreset, S.IconPreset_18))
    gui.RegisterIcon(pre_ui.PRESET_18, Preset_Rays_18)

    Preset_Rays_19 = bitmaps.BaseBitmap()
    Preset_Rays_19.InitWith(os.path.join(dir, S.pathiconspreset, S.IconPreset_19))
    gui.RegisterIcon(pre_ui.PRESET_19, Preset_Rays_19)

    Preset_Rays_20 = bitmaps.BaseBitmap()
    Preset_Rays_20.InitWith(os.path.join(dir, S.pathiconspreset, S.IconPreset_20))
    gui.RegisterIcon(pre_ui.PRESET_20, Preset_Rays_20)

    #--------------------------------------------------------------------

    Preset_Rays_21 = bitmaps.BaseBitmap()
    Preset_Rays_21.InitWith(os.path.join(dir, S.pathiconspreset, S.IconPreset_21))
    gui.RegisterIcon(pre_ui.PRESET_21, Preset_Rays_21)

    # Preset_Rays_22 = bitmaps.BaseBitmap()
    # Preset_Rays_22.InitWith(os.path.join(dir, S.pathiconspreset, S.IconPreset_22))
    # gui.RegisterIcon(pre_ui.PRESET_22, Preset_Rays_22)

    # Preset_Rays_23 = bitmaps.BaseBitmap()
    # Preset_Rays_23.InitWith(os.path.join(dir, S.pathiconspreset, S.IconPreset_23))
    # gui.RegisterIcon(pre_ui.PRESET_23, Preset_Rays_23)

    # Preset_Rays_24 = bitmaps.BaseBitmap()
    # Preset_Rays_24.InitWith(os.path.join(dir, S.pathiconspreset, S.IconPreset_24))
    # gui.RegisterIcon(pre_ui.PRESET_24, Preset_Rays_24)

    # Preset_Rays_25 = bitmaps.BaseBitmap()
    # Preset_Rays_25.InitWith(os.path.join(dir, S.pathiconspreset, S.IconPreset_25))
    # gui.RegisterIcon(pre_ui.PRESET_25, Preset_Rays_25)

    #--------------------------------------------------------------------

    # Preset_Rays_26 = bitmaps.BaseBitmap()
    # Preset_Rays_26.InitWith(os.path.join(dir, S.pathiconspreset, S.IconPreset_26))
    # gui.RegisterIcon(pre_ui.PRESET_26, Preset_Rays_26)

    # Preset_Rays_27 = bitmaps.BaseBitmap()
    # Preset_Rays_27.InitWith(os.path.join(dir, S.pathiconspreset, S.IconPreset_27))
    # gui.RegisterIcon(pre_ui.PRESET_27, Preset_Rays_27)

    # Preset_Rays_28 = bitmaps.BaseBitmap()
    # Preset_Rays_28.InitWith(os.path.join(dir, S.pathiconspreset, S.IconPreset_28))
    # gui.RegisterIcon(pre_ui.PRESET_28, Preset_Rays_28)

    # Preset_Rays_29 = bitmaps.BaseBitmap()
    # Preset_Rays_29.InitWith(os.path.join(dir, S.pathiconspreset, S.IconPreset_29))
    # gui.RegisterIcon(pre_ui.PRESET_29, Preset_Rays_29)

    # Preset_Rays_30 = bitmaps.BaseBitmap()
    # Preset_Rays_30.InitWith(os.path.join(dir, S.pathiconspreset, S.IconPreset_30))
    # gui.RegisterIcon(pre_ui.PRESET_30, Preset_Rays_30)

    RS_noGI_RIS = bitmaps.BaseBitmap()
    RS_noGI_RIS.InitWith(os.path.join(dir, S.pathiconspreset, S.IconPreset_RS_noGI_RIS))
    gui.RegisterIcon(pre_ui.RenderS_noGI, RS_noGI_RIS)

    RS_GI_RIS = bitmaps.BaseBitmap()
    RS_GI_RIS.InitWith(os.path.join(dir, S.pathiconspreset, S.IconPreset_RS_GI_RIS))
    gui.RegisterIcon(pre_ui.RenderS_GI, RS_GI_RIS)

    #--------------------------------------------------------------------

    #-------------------------------------------------------------------- регистрация плагиновв

    # Presets Ray
    Preset_Start_C = c4d.bitmaps.BaseBitmap()
    Preset_Start_C.InitWith(os.path.join(dir, S.pathicons, S.presetsIcon))
    plugins.RegisterCommandPlugin(id = pre_ui.PRESET_RAYS, str = "Rays Preset Scene v 1.0.28", info = 0, help = "Rays Preset Scene", dat = Preset_Start(), icon = Preset_Start_C )