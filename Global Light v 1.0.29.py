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
from module.engine import d_ui
from module.engine import sb_ui
from module.engine import gl_ui
from module.engine import oh_ui
from module.engine import bc_ui
from module.engine import h
from module.engine.helper import *




#----------------------------------------------------------------------------------------- GlobalLight
class GlobalLight(c4d.plugins.ObjectData):


    dialog = None


    #-------------------------------------------------------------------------------- Оптимизация кэша
    def __init__(self):

        self.SetOptimizeCache(True)
    #-------------------------------------------------------------------------------------------------


    #------------------------------------------------------------------- Значение поумолчанию настроек
    def Init(self, op):

        # инициализация настроек интерфейса
        self.InitAttr(op, c4d.Vector, [gl_ui.GL_LIGHT_COLOR])
        self.InitAttr(op, float, [gl_ui.GL_LIGHT_STR])
        self.InitAttr(op, bool, [gl_ui.GL_USED])
        self.InitAttr(op, bool, [gl_ui.GL_INVERT_COLOR])

        # значения поумолчанию
        op[gl_ui.GL_LIGHT_COLOR] = c4d.Vector(0.49, 0.983, 1)
        op[gl_ui.GL_LIGHT_STR] = 0.10

        op[gl_ui.GL_USED] = False
        op[gl_ui.GL_INVERT_COLOR] = True

        return True
    #-------------------------------------------------------------------------------------------------


    #------------------------------------------------------------------------------- Генератор объекта
    def GetVirtualObjects(self, op, hierarchyhelp):

        #-------------------------------------------------------------------------------------------------
        # базовый контейнер
        
        #-------------------------------------------------------------------------------------------------

        doc = op.GetDocument()
        # настройки рендера
        rd = doc.GetActiveRenderData()

        #-------------------------------------------------------------------------------------------------
        # свет
        # если стандартный или физический рендер тогда создать свет
        if rd[c4d.RDATA_RENDERENGINE] == S.Standard or rd[c4d.RDATA_RENDERENGINE] == S.Physical:

            self.base = c4d.BaseObject(c4d.Onull)
            self.base.SetName(op.GetName())
            
            self.light = c4d.BaseObject(5102)
            self.light.SetName(op.GetName() + ' light')
            self.light.InsertUnder(self.base)
            self.light[c4d.LIGHT_BRIGHTNESS] = op[gl_ui.GL_LIGHT_STR]
            self.light[c4d.LIGHT_COLOR] = op[gl_ui.GL_LIGHT_COLOR]
            self.light[c4d.LIGHT_DETAILS_AMBIENT] = 1
            self.light[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 1
            self.light[c4d.LIGHT_DETAILS_SPECULAR] = 0

        elif rd[c4d.RDATA_RENDERENGINE] != S.Standard or rd[c4d.RDATA_RENDERENGINE] != S.Physical:
            return None
        #-------------------------------------------------------------------------------------------------

        return self.base
    #------------------------------------------------------------------------- КОНЕЦ Генерации объекта


    #----------------------------------------------------------------------- Кнопки и сценарии нажатия
    def Message(self, op, type, data):

        if type == c4d.MSG_DESCRIPTION_COMMAND:

            # Helper
            if data["id"][0].id == gl_ui.GL_HELP:

                self.dialog = Helper()
                self.dialog.show(os.path.join(h.globallight_URL), S.STR_BROWSERDIALOG_TITLE, 200, 100, 700, 700)

        #-------------------------------------------------------------------------------------------------
        # ведущий свет
        if op[gl_ui.GL_USED] == True:

            if op[gl_ui.GL_LINK] != None and op[gl_ui.GL_INVERT_COLOR] == True:

                if op[gl_ui.GL_LINK].GetType() == sb_ui.SBOX:
                    instLight = op[gl_ui.GL_LINK]

                    CV = c4d.utils.RGBToHSV(instLight[sb_ui.SB_LIGHT_COLOR])

                    if CV[0] <= 0.5:
                        CR = c4d.Vector(CV[0] + 0.5 , CV[1], CV[2])
                        op[gl_ui.GL_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] >= 0.5:
                        CR = c4d.Vector(CV[0] - 0.5 , CV[1], CV[2])
                        op[gl_ui.GL_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] == 0.5:
                        CR = c4d.Vector(0, CV[1], CV[2])
                        op[gl_ui.GL_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)

                elif op[gl_ui.GL_LINK].GetType() == bc_ui.BOUNCE:
                    instLight = op[gl_ui.GL_LINK]

                    CV = c4d.utils.RGBToHSV(instLight[bc_ui.BC_LIGHT_COLOR])

                    if CV[0] <= 0.5:
                        CR = c4d.Vector(CV[0] + 0.5 , CV[1], CV[2])
                        op[gl_ui.GL_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] >= 0.5:
                        CR = c4d.Vector(CV[0] - 0.5 , CV[1], CV[2])
                        op[gl_ui.GL_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] == 0.5:
                        CR = c4d.Vector(0, CV[1], CV[2])
                        op[gl_ui.GL_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)

                elif op[gl_ui.GL_LINK].GetType() == oh_ui.OVERHEAD:
                    instLight = op[gl_ui.GL_LINK]

                    CV = c4d.utils.RGBToHSV(instLight[oh_ui.OH_LIGHT_COLOR])

                    if CV[0] <= 0.5:
                        CR = c4d.Vector(CV[0] + 0.5 , CV[1], CV[2])
                        op[gl_ui.GL_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] >= 0.5:
                        CR = c4d.Vector(CV[0] - 0.5 , CV[1], CV[2])
                        op[gl_ui.GL_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] == 0.5:
                        CR = c4d.Vector(0, CV[1], CV[2])
                        op[gl_ui.GL_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)

                elif op[gl_ui.GL_LINK].GetType() == d_ui.DAYLIGHT:
                    instLight = op[gl_ui.GL_LINK]

                    CV = c4d.utils.RGBToHSV(instLight[d_ui.DL_LIGHT_COLOR])

                    if CV[0] <= 0.5:
                        CR = c4d.Vector(CV[0] + 0.5 , CV[1], CV[2])
                        op[gl_ui.GL_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] >= 0.5:
                        CR = c4d.Vector(CV[0] - 0.5 , CV[1], CV[2])
                        op[gl_ui.GL_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] == 0.5:
                        CR = c4d.Vector(0, CV[1], CV[2])
                        op[gl_ui.GL_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)

                elif op[gl_ui.GL_LINK].GetType() == 5102:
                    instLight = op[gl_ui.GL_LINK]

                    CV = c4d.utils.RGBToHSV(instLight[c4d.LIGHT_COLOR])

                    if CV[0] <= 0.5:
                        CR = c4d.Vector(CV[0] + 0.5 , CV[1], CV[2])
                        op[gl_ui.GL_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] >= 0.5:
                        CR = c4d.Vector(CV[0] - 0.5 , CV[1], CV[2])
                        op[gl_ui.GL_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] == 0.5:
                        CR = c4d.Vector(0, CV[1], CV[2])
                        op[gl_ui.GL_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)

            elif op[gl_ui.GL_LINK] != None and op[gl_ui.GL_INVERT_COLOR] == False:

                if op[gl_ui.GL_LINK].GetType() == sb_ui.SBOX:
                    instLight = op[gl_ui.GL_LINK]

                    op[gl_ui.GL_LIGHT_COLOR] = instLight[sb_ui.SB_LIGHT_COLOR]

                elif op[gl_ui.GL_LINK].GetType() == bc_ui.BOUNCE:
                    instLight = op[gl_ui.GL_LINK]

                    op[gl_ui.GL_LIGHT_COLOR] = instLight[bc_ui.BC_LIGHT_COLOR]

                elif op[gl_ui.GL_LINK].GetType() == oh_ui.OVERHEAD:
                    instLight = op[gl_ui.GL_LINK]

                    op[gl_ui.GL_LIGHT_COLOR] = instLight[oh_ui.OH_LIGHT_COLOR]

                elif op[gl_ui.GL_LINK].GetType() == d_ui.DAYLIGHT:
                    instLight = op[gl_ui.GL_LINK]

                    op[gl_ui.GL_LIGHT_COLOR] = instLight[d_ui.DL_LIGHT_COLOR]

                elif op[gl_ui.GL_LINK].GetType() == 5102:
                    instLight = op[gl_ui.GL_LINK]

                    op[gl_ui.GL_LIGHT_COLOR] = instLight[c4d.LIGHT_COLOR]

        #-------------------------------------------------------------------------------------------------

        return True
    #----------------------------------------------------------------- КОНЕЦ Кнопки и сценарии нажатия


    #----------------------------------------------------------------------------- выкл/вкл интерфейса
    def GetDEnabling(self, op, id, t_data, flags, itemdesc):

        data = op.GetDataInstance()
        if data is None: return
        ID = id[0].id

        doc = op.GetDocument()
        rd = doc.GetActiveRenderData()

        #-------------------------------------------------------------------------------------------------

        if rd[c4d.RDATA_RENDERENGINE] == S.Standard:
            op[gl_ui.GL_RENDERER] = S.R_S

        elif rd[c4d.RDATA_RENDERENGINE] == S.Physical:
            op[gl_ui.GL_RENDERER] = S.R_P

        #------------------------------------------------------------------------------------------------- если не стандартный рендер и не физический рендер

        if rd[c4d.RDATA_RENDERENGINE] == S.Standard or rd[c4d.RDATA_RENDERENGINE] == S.Physical:

            if op[gl_ui.GL_USED] == True:
                if ID == gl_ui.GL_LINK:
                    return True

                if ID == gl_ui.GL_LIGHT_COLOR:
                    return False

                if ID == gl_ui.GL_INVERT_COLOR:
                    return True

            elif op[gl_ui.GL_USED] == False:
                if ID == gl_ui.GL_LINK:
                    return False

                if ID == gl_ui.GL_LIGHT_COLOR:
                    return True

                if ID == gl_ui.GL_INVERT_COLOR:
                    return False

        elif rd[c4d.RDATA_RENDERENGINE] != S.Standard or rd[c4d.RDATA_RENDERENGINE] != S.Physical:
            
            op[gl_ui.GL_RENDERER] = S.WARNING

            if ID == gl_ui.GL_LINK:
                return False

            if ID == gl_ui.GL_LIGHT_COLOR:
                return False

            if ID == gl_ui.GL_LINK:
                return False

            if ID == gl_ui.GL_LIGHT_COLOR:
                return False

            if ID == gl_ui.GL_LIGHT_STR:
                return False

            if ID == gl_ui.GL_USED:
                return False

            if ID == gl_ui.GL_INVERT_COLOR:
                return False
        #-------------------------------------------------------------------------------------------------

        return True
    #---------------------------------------------------------------------- КОНЕЦ  выкл/вкл интерфейса


#-------------------------------------------------------------------------------------- КОНЕЦ GlobalLight


# инициализация компонентов
if __name__ == '__main__':

    dir, file = os.path.split(__file__)
    doc = c4d.documents.GetActiveDocument()
    rd = doc.GetActiveRenderData()

    # GlobalLight
    iconGL = c4d.bitmaps.BaseBitmap()
    iconGL.InitWith(os.path.join(dir, S.pathicons, S.globallightIcon))
    if rd[c4d.RDATA_RENDERENGINE] == S.Standard or rd[c4d.RDATA_RENDERENGINE] == S.Physical:
        plugins.RegisterObjectPlugin(id = gl_ui.GLOBALLIGHT, str = "Global Light", g = GlobalLight, description = "GlobalLight", info = c4d.OBJECT_GENERATOR, icon = iconGL )