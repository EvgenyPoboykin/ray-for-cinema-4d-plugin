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
from module.engine import s_ui
from module.engine import h
from module.engine.helper import *




#-------------------------------------------------------------------------------------------- Daylight
class Daylight(c4d.plugins.ObjectData):


    dialog = None


    #-------------------------------------------------------------------------------- оптимизация кэша
    def __init__(self):

        self.SetOptimizeCache(True)
    #-------------------------------------------------------------------------------------------------


    #------------------------------------------------------------------- значение поумолчанию настроек
    def Init(self, op):

        # инициализация настроек интерфейса
        self.InitAttr(op, float, [d_ui.DL_ROT_X])
        self.InitAttr(op, float, [d_ui.DL_ROT_Y])

        self.InitAttr(op, c4d.Vector, [d_ui.DL_LIGHT_COLOR])
        self.InitAttr(op, float, [d_ui.DL_BRIGHTNESS])

        self.InitAttr(op, long, [d_ui.DL_LIGHT_SHADOWTYPE])
        self.InitAttr(op, float, [d_ui.DL_SHADOW_DENSITY])
        self.InitAttr(op, bool, [d_ui.DL_LOCK])
        self.InitAttr(op, c4d.Vector, [d_ui.DL_SHADOW_COLOR])
        self.InitAttr(op, float, [d_ui.DL_SHADOW_HUE])
        self.InitAttr(op, float, [d_ui.DL_SHADOW_BRIGHTNESS])

        self.InitAttr(op, bool, [d_ui.DL_USED_FOG])
        self.InitAttr(op, float, [d_ui.DL_FOG_STR])
        self.InitAttr(op, float, [d_ui.DL_FOG_DISTANCE])
        self.InitAttr(op, bool, [d_ui.DL_LOCK_FOG])
        self.InitAttr(op, c4d.Vector, [d_ui.DL_FOG_COLOR])
        self.InitAttr(op, float, [d_ui.DL_FOG_HUE])

        self.InitAttr(op, bool, [d_ui.DL_SHOW_IN_VIEWPORT])
        self.InitAttr(op, bool, [d_ui.DL_SHOW_FOG])

        # значения поумолчанию
        op[d_ui.DL_ROT_X] = math.radians(-45)
        op[d_ui.DL_ROT_Y] = math.radians(45)

        op[d_ui.DL_LIGHT_COLOR] = c4d.Vector(1, 0.896, 0.75)
        op[d_ui.DL_BRIGHTNESS] = 1.0

        op[d_ui.DL_LIGHT_SHADOWTYPE] = d_ui.DL_TRACE
        op[d_ui.DL_SHADOW_DENSITY] = 1.0
        op[d_ui.DL_LOCK] = True
        op[d_ui.DL_SHADOW_COLOR] = c4d.Vector(0, 0, 0)
        op[d_ui.DL_SHADOW_HUE] = 0.3
        op[d_ui.DL_SHADOW_BRIGHTNESS] = 0.15

        op[d_ui.DL_USED_FOG] = False
        op[d_ui.DL_FOG_STR] = 0.5
        op[d_ui.DL_FOG_DISTANCE] = 50000.0
        op[d_ui.DL_LOCK_FOG] = True
        op[d_ui.DL_FOG_COLOR] = c4d.Vector(0.77, 0.981, 1)
        op[d_ui.DL_FOG_HUE] = 0.5

        op[d_ui.DL_SHOW_IN_VIEWPORT] = True
        op[d_ui.DL_SHOW_FOG] = False

        return True
    #-------------------------------------------------------------------------------------------------


    #------------------------------------------------------------------------------- генерация объекта
    def GetVirtualObjects(self, op, hierarchyhelp):

        doc = op.GetDocument()
        rd = doc.GetActiveRenderData()

        if rd[c4d.RDATA_RENDERENGINE] == S.Standard or rd[c4d.RDATA_RENDERENGINE] == S.Physical:

            op[c4d.ID_BASEOBJECT_USECOLOR] = 2
            op[c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(0.894, 0.094, 0.4)

            self.base = c4d.BaseObject(c4d.Onull)
            self.base.SetName(op.GetName())

            self.circle = c4d.BaseObject(c4d.Onull)
            self.circle.InsertUnder(self.base)
            self.circle.SetName(op.GetName() + ' circles')
            self.circle[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_X] = op[d_ui.DL_ROT_X]
            self.circle[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Y] = -(op[d_ui.DL_ROT_Y])

            self.x_circle = c4d.BaseObject(5181)
            self.x_circle.InsertUnder(self.circle)
            self.x_circle.SetName(op.GetName() + ' X')
            self.x_circle[c4d.PRIM_CIRCLE_RADIUS] = 100
            self.x_circle[c4d.PRIM_PLANE] = 1

            self.y_circle = c4d.BaseObject(5181)
            self.y_circle.InsertUnder(self.circle)
            self.y_circle.SetName(op.GetName() + ' Y')
            self.y_circle[c4d.PRIM_CIRCLE_RADIUS] = 100
            self.y_circle[c4d.PRIM_PLANE] = 2

            self.fog = c4d.BaseObject(5106)
            self.fog.SetName(op.GetName() + ' fog')
            self.fog.InsertUnder(self.base)
            self.fog[c4d.ENVIRONMENT_FOGENABLE] = 1

            if op[d_ui.DL_USED_FOG] == False:

                self.fog[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 1
                self.fog[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 1

            elif op[d_ui.DL_USED_FOG] == True:

                self.fog[c4d.ENVIRONMENT_AMBIENT] = op[d_ui.DL_FOG_COLOR]
                self.fog[c4d.ENVIRONMENT_FOG] = op[d_ui.DL_FOG_COLOR]
                self.fog[c4d.ENVIRONMENT_FOGSTRENGTH] = op[d_ui.DL_FOG_STR]
                self.fog[c4d.ENVIRONMENT_FOGDISTANCE] = op[d_ui.DL_FOG_DISTANCE]
                if op[d_ui.DL_SHOW_FOG] == True:
                    self.fog[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 0

                elif op[d_ui.DL_SHOW_FOG] == False:
                    self.fog[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 1

            self.rotX = c4d.BaseObject(c4d.Onull)
            self.rotX.SetName(op.GetName() + ' rotation X')
            self.rotX.InsertUnder(self.base)
            self.rotX[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_X] = op[d_ui.DL_ROT_X]

            self.rotY = c4d.BaseObject(c4d.Onull)
            self.rotY.SetName(op.GetName() + ' rotation Y')
            self.rotY.InsertUnder(self.rotX)
            self.rotY[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Y] = -(op[d_ui.DL_ROT_Y])

            self.sun = c4d.BaseObject(5102)
            self.sun.SetName(op.GetName() + ' sun')
            self.sun.InsertUnder(self.rotY)
            self.sun[c4d.LIGHT_COLOR] = op[d_ui.DL_LIGHT_COLOR]
            self.sun[c4d.LIGHT_BRIGHTNESS] = op[d_ui.DL_BRIGHTNESS]
            self.sun[c4d.LIGHT_TYPE] = 3

            if op[d_ui.DL_LIGHT_SHADOWTYPE] == d_ui.DL_TRACE:

                self.sun[c4d.LIGHT_SHADOWTYPE] = 2

            elif op[d_ui.DL_LIGHT_SHADOWTYPE] == d_ui.DL_AREA:

                self.sun[c4d.LIGHT_SHADOWTYPE] = 3

            self.sun[c4d.LIGHT_SHADOW_DENSITY] = op[d_ui.DL_SHADOW_DENSITY]
            self.sun[c4d.LIGHT_SHADOW_COLOR] = op[d_ui.DL_SHADOW_COLOR]

            self.sun[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Z] = -5000#
            self.sun[c4d.LIGHT_DETAILS_OUTERDISTANCE] = -(self.sun[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Z])

            if op[d_ui.DL_SHOW_IN_VIEWPORT] == True:
                self.sun[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 0

            elif op[d_ui.DL_SHOW_IN_VIEWPORT] == False:
                self.sun[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 1

        elif rd[c4d.RDATA_RENDERENGINE] != S.Standard or rd[c4d.RDATA_RENDERENGINE] != S.Physical:
            return None

        return self.base
    #------------------------------------------------------------------------- КОНЕЦ Генерации объекта


    #----------------------------------------------------------------------- Кнопки и сценарии нажатия
    def Message(self, op, type, data):

        if type == c4d.MSG_DESCRIPTION_COMMAND:

            # Helper
            if data["id"][0].id == d_ui.DL_HELP:

                self.dialog = Helper()
                self.dialog.show(os.path.join(h.daylight_URL), S.STR_BROWSERDIALOG_TITLE, 200, 100, 700, 700)

        if op[d_ui.DL_LOCK] == True:

            CV = c4d.utils.RGBToHSV(op[d_ui.DL_LIGHT_COLOR])

            if CV[0] <= 0.5:
                CR = c4d.Vector(CV[0] + 0.5 , op[d_ui.DL_SHADOW_HUE], op[d_ui.DL_SHADOW_BRIGHTNESS])
                op[d_ui.DL_SHADOW_COLOR] = c4d.utils.HSVToRGB(CR)

            elif CV[0] >= 0.5:
                CR = c4d.Vector(CV[0] - 0.5 , op[d_ui.DL_SHADOW_HUE], op[d_ui.DL_SHADOW_BRIGHTNESS])
                op[d_ui.DL_SHADOW_COLOR] = c4d.utils.HSVToRGB(CR)

            elif CV[0] == 0.5:
                CR = c4d.Vector(0, op[d_ui.DL_SHADOW_HUE], op[d_ui.DL_SHADOW_BRIGHTNESS])
                op[d_ui.DL_SHADOW_COLOR] = c4d.utils.HSVToRGB(CR)


        if op[d_ui.DL_LOCK_FOG] == True:

            CV = c4d.utils.RGBToHSV(op[d_ui.DL_LIGHT_COLOR])

            if CV[0] <= 0.5:
                CRF = c4d.Vector(CV[0] + 0.5 , op[d_ui.DL_FOG_HUE], CV[2])
                op[d_ui.DL_FOG_COLOR] = c4d.utils.HSVToRGB(CRF)

            elif CV[0] >= 0.5:
                CRF = c4d.Vector(CV[0] - 0.5 , op[d_ui.DL_FOG_HUE], CV[2])
                op[d_ui.DL_FOG_COLOR] = c4d.utils.HSVToRGB(CRF)

            elif CV[0] == 0.5:
                CRF = c4d.Vector(0, op[d_ui.DL_FOG_HUE], CV[2])
                op[d_ui.DL_FOG_COLOR] = c4d.utils.HSVToRGB(CRF)

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
            op[d_ui.DL_RENDERER] = S.R_S

        elif rd[c4d.RDATA_RENDERENGINE] == S.Physical:
            op[d_ui.DL_RENDERER] = S.R_P

        elif rd[c4d.RDATA_RENDERENGINE] != S.Standard or rd[c4d.RDATA_RENDERENGINE] != S.Physical:
            op[d_ui.DL_RENDERER] = S.WARNING

        if rd[c4d.RDATA_RENDERENGINE] == S.Standard or rd[c4d.RDATA_RENDERENGINE] == S.Physical:

            if doc.SearchObject('Sky') != None:
                if doc.SearchObject('Sky').GetType() == s_ui.SKY:
                    if doc.SearchObject('Sky')[s_ui.S_SUN] == op:
                        if ID == d_ui.DL_ROT_X:
                            return False

                        if ID == d_ui.DL_ROT_Y:
                            return False
            else:
                if ID == d_ui.DL_ROT_X:
                    return True

                if ID == d_ui.DL_ROT_Y:
                    return True


            if op[d_ui.DL_LOCK] == True:
                if ID == d_ui.DL_SHADOW_COLOR:
                    return False

                if ID == d_ui.DL_SHADOW_HUE:
                    return True

                if ID == d_ui.DL_SHADOW_BRIGHTNESS:
                    return True

            elif op[d_ui.DL_LOCK] == False:
                if ID == d_ui.DL_SHADOW_COLOR:
                    return True

                if ID == d_ui.DL_SHADOW_HUE:
                    return False

                if ID == d_ui.DL_SHADOW_BRIGHTNESS:
                    return False

            if op[d_ui.DL_USED_FOG] == True:
                if ID == d_ui.DL_FOG_STR:
                    return True

                if ID == d_ui.DL_FOG_DISTANCE:
                    return True

                if ID == d_ui.DL_LOCK_FOG:
                    return True

                if ID == d_ui.DL_SHOW_FOG:
                    return True

                if ID == d_ui.DL_FOG_HUE:
                    return True

            elif op[d_ui.DL_USED_FOG] == False:
                if ID == d_ui.DL_FOG_STR:
                    return False

                if ID == d_ui.DL_FOG_DISTANCE:
                    return False

                if ID == d_ui.DL_LOCK_FOG:
                    return False

                if ID == d_ui.DL_SHOW_FOG:
                    return False

                if ID == d_ui.DL_FOG_HUE:
                    return False

            if op[d_ui.DL_LOCK_FOG] == True:
                if ID == d_ui.DL_FOG_COLOR:
                    return False

                if ID == d_ui.DL_FOG_HUE:
                    return True

            elif op[d_ui.DL_LOCK_FOG] == False:
                if ID == d_ui.DL_FOG_COLOR:
                    return True

                if ID == d_ui.DL_FOG_HUE:
                    return False

        elif rd[c4d.RDATA_RENDERENGINE] != S.Standard or rd[c4d.RDATA_RENDERENGINE] != S.Physical:

            if ID == d_ui.DL_ROT_X:
                return False

            if ID == d_ui.DL_ROT_Y:
                return False

            if ID == d_ui.DL_SHADOW_COLOR:
                return False

            if ID == d_ui.DL_SHADOW_HUE:
                return False

            if ID == d_ui.DL_SHADOW_BRIGHTNESS:
                return False

            if ID == d_ui.DL_SHADOW_COLOR:
                return False

            if ID == d_ui.DL_SHADOW_HUE:
                return False

            if ID == d_ui.DL_SHADOW_BRIGHTNESS:
                return False

            if ID == d_ui.DL_FOG_STR:
                return False

            if ID == d_ui.DL_FOG_DISTANCE:
                return False

            if ID == d_ui.DL_LOCK_FOG:
                return False

            if ID == d_ui.DL_SHOW_FOG:
                return False

            if ID == d_ui.DL_FOG_HUE:
                return False

            if ID == d_ui.DL_FOG_STR:
                return False

            if ID == d_ui.DL_FOG_DISTANCE:
                return False

            if ID == d_ui.DL_LOCK_FOG:
                return False

            if ID == d_ui.DL_SHOW_FOG:
                return False

            if ID == d_ui.DL_FOG_HUE:
                return False

            if ID == d_ui.DL_FOG_COLOR:
                return False

            if ID == d_ui.DL_FOG_HUE:
                return False

            if ID == d_ui.DL_FOG_COLOR:
                return False

            if ID == d_ui.DL_FOG_HUE:
                return False

            if ID == d_ui.DL_USED_FOG:
                return False

            if ID == d_ui.DL_SHOW_IN_VIEWPORT:
                return False

            if ID == d_ui.DL_LOCK:
                return False

            if ID == d_ui.DL_SHADOW_DENSITY:
                return False

            if ID == d_ui.DL_LIGHT_SHADOWTYPE:
                return False

            if ID == d_ui.DL_BRIGHTNESS:
                return False

            if ID == d_ui.DL_LIGHT_COLOR:
                return False

        return True
    #---------------------------------------------------------------------- КОНЕЦ  выкл/вкл интерфейса


#-------------------------------------------------------------------------------------- КОНЕЦ Daylight


# инициализация компонентов
if __name__ == '__main__':

    dir, file = os.path.split(__file__)

    # Daylight
    iconDL = c4d.bitmaps.BaseBitmap()
    iconDL.InitWith(os.path.join(dir, S.pathicons, S.daylightIcon))
    plugins.RegisterObjectPlugin(id = d_ui.DAYLIGHT, str = "Daylight", g = Daylight, description = "Daylight", info = c4d.OBJECT_GENERATOR, icon = iconDL )