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




#-------------------------------------------------------------------------------------------- SoftBox
class SoftBox(c4d.plugins.ObjectData):


    dialog = None
    HANDLECOUNT = 5


    #-------------------------------------------------------------------------------- Оптимизация кэша
    def __init__(self):

        self.SetOptimizeCache(True)
    #-------------------------------------------------------------------------------------------------


    #------------------------------------------------------------------- Значение поумолчанию настроек
    def Init(self, op):

        # инициализация настроек интерфейса
        self.InitAttr(op, long, [sb_ui.SB_MODE])
        self.InitAttr(op, long, [sb_ui.SB_LIGHT_PRO])

        self.InitAttr(op, float, [sb_ui.SB_WIDTH])
        self.InitAttr(op, float, [sb_ui.SB_HIDTH])
        self.InitAttr(op, float, [sb_ui.SB_DIST])

        self.InitAttr(op, bool, [sb_ui.SB_SHOW_FALLOFF])
        self.InitAttr(op, bool, [sb_ui.SB_INFINITE])
        self.InitAttr(op, bool, [sb_ui.SB_CAST])

        self.InitAttr(op, c4d.Vector, [sb_ui.SB_LIGHT_COLOR])
        self.InitAttr(op, float, [sb_ui.SB_BRIGHTNESS])
        self.InitAttr(op, int, [sb_ui.SB_SAMPLES])

        self.InitAttr(op, bool, [sb_ui.SB_USED_BRIGHTNESS_PLANE])
        self.InitAttr(op, float, [sb_ui.SB_BRIGHTNESS_PLANE])

        self.InitAttr(op, long, [sb_ui.SB_LIGHT_SHADOWTYPE])
        self.InitAttr(op, bool, [sb_ui.SB_LOCK])
        self.InitAttr(op, c4d.Vector, [sb_ui.SB_SHADOW_COLOR])
        self.InitAttr(op, float, [sb_ui.SB_SHADOW_DENSITY])
        self.InitAttr(op, float, [sb_ui.SB_SHADOW_VALUE])
        self.InitAttr(op, float, [sb_ui.SB_LIGHT_SHADOW_DENSITY])
        self.InitAttr(op, int, [sb_ui.SB_LIGHT_SHADOW_MAXSAMPLES])
        self.InitAttr(op, int, [sb_ui.SB_LIGHT_SHADOW_MAPSIZEX])

        self.InitAttr(op, bool, [sb_ui.SB_SB_CAMERA])
        self.InitAttr(op, bool, [sb_ui.SB_USED])
        self.InitAttr(op, bool, [sb_ui.SB_INVERT_COLOR])
        self.InitAttr(op, bool, [sb_ui.SB_ADDGAIN])
        self.InitAttr(op, bool, [sb_ui.SB_REFLECTION])
        self.InitAttr(op, bool, [sb_ui.SB_SPECULAR])
        self.InitAttr(op, bool, [sb_ui.SB_SB_TRANSPARENCY])
        self.InitAttr(op, bool, [sb_ui.SB_LIGHT_ON])
        self.InitAttr(op, bool, [sb_ui.SB_V_EDITOR])
        self.InitAttr(op, c4d.InExcludeData, [sb_ui.SB_LIGHT_OBJECT])

        # значения поумолчанию
        op[sb_ui.SB_MODE] = sb_ui.SB_SOFTBOX
        op[sb_ui.SB_LIGHT_PRO] = sb_ui.SB_EXCLUDE

        op[sb_ui.SB_WIDTH] = 100.0
        op[sb_ui.SB_HIDTH] = 100.0
        op[sb_ui.SB_DIST] = 300.0

        op[sb_ui.SB_USED] = False
        op[sb_ui.SB_INVERT_COLOR] = False
        op[sb_ui.SB_SHOW_FALLOFF] = False
        op[sb_ui.SB_INFINITE] = True

        op[sb_ui.SB_LIGHT_COLOR] = c4d.Vector(1, 0.91, 0.8)
        op[sb_ui.SB_BRIGHTNESS] = 1.0
        op[sb_ui.SB_SAMPLES] = 40

        op[sb_ui.SB_USED_BRIGHTNESS_PLANE] = False
        op[sb_ui.SB_BRIGHTNESS_PLANE] = 1.0

        op[sb_ui.SB_LIGHT_SHADOWTYPE] = sb_ui.SB_SH_AREA
        op[sb_ui.SB_LOCK] = True
        op[sb_ui.SB_SHADOW_COLOR] = c4d.Vector(0, 0, 0)
        op[sb_ui.SB_SHADOW_DENSITY] = 0.5
        op[sb_ui.SB_SHADOW_VALUE] = 0.2
        op[sb_ui.SB_LIGHT_SHADOW_DENSITY] = 1.0
        op[sb_ui.SB_LIGHT_SHADOW_MAXSAMPLES] = 300
        op[sb_ui.SB_LIGHT_SHADOW_MAPSIZEX] = 250

        op[sb_ui.SB_CAST] = True
        op[sb_ui.SB_SB_CAMERA] = False
        op[sb_ui.SB_ADDGAIN] = False
        op[sb_ui.SB_REFLECTION] = True
        op[sb_ui.SB_SPECULAR] = True
        op[sb_ui.SB_SB_TRANSPARENCY] = True
        op[sb_ui.SB_LIGHT_ON] = True
        op[sb_ui.SB_V_EDITOR] = True
        op[sb_ui.SB_LIGHT_OBJECT] = c4d.InExcludeData()

        return True
    #------------------------------------------------------------- КОНЕЦ Значение поумолчанию настроек


    #------------------------------------------------------------------------------------------- Ручки
    def GetHandleCount(self, op):

        return self.HANDLECOUNT

    def GetHandle(self, op, i, info):

        wight = op[sb_ui.SB_WIDTH]
        if wight is None: wight = 100

        hight = op[sb_ui.SB_HIDTH]
        if hight is None: hight = 100

        dist = op[sb_ui.SB_DIST]
        if dist is None: dist = 300.0

        doc = op.GetDocument()
        rd = doc.GetActiveRenderData()

        if rd[c4d.RDATA_RENDERENGINE] == S.Standard or rd[c4d.RDATA_RENDERENGINE] == S.Physical:
            if op[sb_ui.SB_MODE] == sb_ui.SB_SOFTBOX:
                if i is 0:
                    info.position = c4d.Vector(wight/2, 0.0, 0.0)
                    info.direction = c4d.Vector(1.0, 0.0, 0.0)
                elif i is 1:
                    info.position = c4d.Vector(0.0, hight/2, 0.0)
                    info.direction = c4d.Vector(0.0, 1.0, 0.0)
                elif i is 2:
                    info.position = c4d.Vector(0.0, -hight/2, 0.0)
                    info.direction = c4d.Vector(0.0, -1.0, 0.0)
                elif i is 3:
                    info.position = c4d.Vector(-wight/2, 0.0, 0.0)
                    info.direction = c4d.Vector(-1.0, 0.0, 0.0)
                elif i is 4:
                    info.position = c4d.Vector(0.0, 0.0, dist)
                    info.direction = c4d.Vector(0.0, 0.0, 1.0)

            elif op[sb_ui.SB_MODE] == sb_ui.SB_SPOT:
                if i is 0:
                    info.position = c4d.Vector(wight/2, 0.0, 0.0)
                    info.direction = c4d.Vector(1.0, 0.0, 0.0)
                elif i is 1:
                    info.position = c4d.Vector(0.0, wight/2, 0.0)
                    info.direction = c4d.Vector(0.0, 1.0, 0.0)
                elif i is 2:
                    info.position = c4d.Vector(0.0, -wight/2, 0.0)
                    info.direction = c4d.Vector(0.0, -1.0, 0.0)
                elif i is 3:
                    info.position = c4d.Vector(-wight/2, 0.0, 0.0)
                    info.direction = c4d.Vector(-1.0, 0.0, 0.0)
                elif i is 4:
                    info.position = c4d.Vector(0.0, 0.0, dist)
                    info.direction = c4d.Vector(0.0, 0.0, 1.0)

    def SetHandle(self, op, i, p, info):

        data = op.GetDataInstance()
        if data is None: return

        tmp = c4d.HandleInfo()
        self.GetHandle(op, i, tmp)

        val = (p-tmp.position)*info.direction

        if op[sb_ui.SB_MODE] == sb_ui.SB_SOFTBOX:
            if i is 0:
                op[sb_ui.SB_WIDTH] = c4d.utils.FCut(op[sb_ui.SB_WIDTH]+val, 0.0, sys.maxint)
            elif i is 1:
                op[sb_ui.SB_HIDTH] = c4d.utils.FCut(op[sb_ui.SB_HIDTH]+val, 0.0, sys.maxint)
            elif i is 2:
                op[sb_ui.SB_HIDTH] = c4d.utils.FCut(op[sb_ui.SB_HIDTH]+val, 0.0, sys.maxint)
            elif i is 3:
                op[sb_ui.SB_WIDTH] = c4d.utils.FCut(op[sb_ui.SB_WIDTH]+val, 0.0, sys.maxint)
            elif i is 4:
                op[sb_ui.SB_DIST] = c4d.utils.FCut(op[sb_ui.SB_DIST]+val, 0.0, sys.maxint)

        elif op[sb_ui.SB_MODE] == sb_ui.SB_SPOT:
            if i is 0:
                op[sb_ui.SB_WIDTH] = c4d.utils.FCut(op[sb_ui.SB_WIDTH]+val, 0.0, sys.maxint)
            elif i is 1:
                op[sb_ui.SB_WIDTH] = c4d.utils.FCut(op[sb_ui.SB_WIDTH]+val, 0.0, sys.maxint)
            elif i is 2:
                op[sb_ui.SB_WIDTH] = c4d.utils.FCut(op[sb_ui.SB_WIDTH]+val, 0.0, sys.maxint)
            elif i is 3:
                op[sb_ui.SB_WIDTH] = c4d.utils.FCut(op[sb_ui.SB_WIDTH]+val, 0.0, sys.maxint)
            elif i is 4:
                op[sb_ui.SB_DIST] = c4d.utils.FCut(op[sb_ui.SB_DIST]+val, 0.0, sys.maxint)

    #--------------------------------------------------------------------------- R17
    def DetectHandle(self, op, bd, x, y, qualifier):
        
        if qualifier&c4d.QUALIFIER_CTRL: return c4d.NOTOK

        mg = op.GetMg()
        ret = c4d.NOTOK

        for i in xrange(self.GetHandleCount(op)):
            info = c4d.HandleInfo()
            self.GetHandle(op, i, info)
            if bd.PointInRange(info.position*mg, x, y):
                ret = i
                if not qualifier&c4d.QUALIFIER_SHIFT: break

        return ret

    def MoveHandle(self, op, undo, mouse_pos, hit_id, qualifier, bd):
        mg = op.GetUpMg() * undo.GetMl()

        info = c4d.HandleInfo()
        self.GetHandle(op, hit_id, info)

        self.SetHandle(op, hit_id, info.CalculateNewPosition(bd, mg, mouse_pos), info)

        return True
    # --------------------------------------------------------------------------- R17
    #------------------------------------------------------------------------------------- КОНЕЦ Ручки


    #-------------------------------------------------------------------------------------- Прорисовка
    def Draw(self, op, drawpass, bd, bh):

        doc = op.GetDocument()
        rd = doc.GetActiveRenderData()

        if rd[c4d.RDATA_RENDERENGINE] == S.Standard or rd[c4d.RDATA_RENDERENGINE] == S.Physical:

            #------------------------------------------------------------------------------------------------- Ручки
            if drawpass!=c4d.DRAWPASS_HANDLES: return c4d.DRAWRESULT_SKIP

            bd.SetPen(c4d.GetViewColor(c4d.VIEWCOLOR_ACTIVEPOINT))

            hitid = op.GetHighlightHandle(bd)
            bd.SetMatrix_Matrix(op, bh.GetMg())

            for i in xrange(self.HANDLECOUNT):
                if i==hitid:
                    bd.SetPen(c4d.GetViewColor(c4d.VIEWCOLOR_SELECTION_PREVIEW))
                else:
                    bd.SetPen(c4d.GetViewColor(c4d.VIEWCOLOR_ACTIVEPOINT))

                info = c4d.HandleInfo()
                self.GetHandle(op, i, info)
                bd.DrawHandle(info.position, c4d.DRAWHANDLE_MIDDLE, 0)
                bd.SetPen(c4d.GetViewColor(c4d.VIEWCOLOR_ACTIVEPOINT))
                if i is 4:
                    bd.DrawLine(info.position, c4d.Vector(0), 0)

                bd.SetPen(c4d.GetViewColor(c4d.VIEWCOLOR_ACTIVEPOINT))
            #-------------------------------------------------------------------------------------------------

        return c4d.DRAWRESULT_OK
    #-------------------------------------------------------------------------------- КОНЕЦ Прорисовки


    #------------------------------------------------------------------------------- Генерация объекта
    def GetVirtualObjects(self, op, hierarchyhelp):

        doc = op.GetDocument()
        rd = doc.GetActiveRenderData()


        if rd[c4d.RDATA_RENDERENGINE] == S.Standard or rd[c4d.RDATA_RENDERENGINE] == S.Physical:

            op[c4d.ID_BASEOBJECT_USECOLOR] = 2
            op[c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(0.2, 0.2, 0.2)

            #------------------------------------------------------------------------------------------------- Базовый контейнер для рига
            self.base = c4d.BaseObject(c4d.Onull)
            self.base.SetName(op.GetName())
            self.base[c4d.ID_BASEOBJECT_REL_SCALE] = c4d.Vector(1, 1, 1)
            self.base[c4d.NULLOBJECT_DISPLAY] = 14

            if op[sb_ui.SB_V_EDITOR] == True:
                self.base[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 0

            elif op[sb_ui.SB_V_EDITOR] == False:
                self.base[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 1

            if op.GetTag(5676) != None:
                self.TargetTag = self.base.MakeTag(5676)
                self.TargetTag.SetName(self.base.GetName() + ' target')

                sourse = op.GetTag(5676)

                self.TargetTag[c4d.TARGETEXPRESSIONTAG_LINK] = sourse[c4d.TARGETEXPRESSIONTAG_LINK]


            #------------------------------------------------------------------------------------------------- SoftBox Лофт объект
            self.softbox = c4d.BaseObject(5107)
            self.softbox.SetName(op.GetName() + ' softbox itself')
            self.softbox.InsertUnder(self.base)
            self.softbox[c4d.ID_BASEOBJECT_USECOLOR] = 2
            self.softbox[c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(0, 0, 0)

            self.softbox[c4d.LOFTOBJECT_ADAPTIVEY] = 0
            self.softbox[c4d.CAP_START] = 1
            self.softbox[c4d.CAP_END] = 0

            if op[sb_ui.SB_REFLECTION] == True:
                self.softbox[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 0

            elif op[sb_ui.SB_REFLECTION] == False:
                self.softbox[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 1

            # tags
            self.tag_comp_softbox = self.softbox.MakeTag(5637)
            self.tag_comp_softbox[c4d.ID_BASELIST_NAME] = (self.softbox.GetName() + ' compositing')
            self.tag_comp_softbox[c4d.COMPOSITINGTAG_SEENBYCAMERA] = op[sb_ui.SB_SB_CAMERA]
            self.tag_comp_softbox[c4d.COMPOSITINGTAG_SEENBYRAYS] = 0
            self.tag_comp_softbox[c4d.COMPOSITINGTAG_SEENBYGI] = 0
            self.tag_comp_softbox[c4d.COMPOSITINGTAG_SEENBYTRANSPARENCY] = op[sb_ui.SB_SB_TRANSPARENCY]
            self.tag_comp_softbox[c4d.COMPOSITINGTAG_SEENBYREFRACTION] = op[sb_ui.SB_SB_TRANSPARENCY]
            self.tag_comp_softbox[c4d.COMPOSITINGTAG_SEENBYREFLECTION] = op[sb_ui.SB_REFLECTION]
            self.tag_comp_softbox[c4d.COMPOSITINGTAG_CASTSHADOW] = op[sb_ui.SB_CAST]
            #-------------------------------------------------------------------------------------------------


            #------------------------------------------------------------------------------------------------- Общие настройки света
            self.light = c4d.BaseObject(5102)
            self.light.SetName(op.GetName() + ' light')
            self.light.InsertUnder(self.base)
            self.light[c4d.LIGHT_SHADOWTYPE] = 3
            self.light[c4d.LIGHT_TYPE] = 8
            self.light[c4d.LIGHT_DETAILS_FALLOFF] = 10
            self.light[c4d.LIGHT_SHADOW_DENSITY] = op[sb_ui.SB_LIGHT_SHADOW_DENSITY]
            self.light[c4d.LIGHT_COLOR] = op[sb_ui.SB_LIGHT_COLOR]
            self.light[c4d.LIGHT_SHADOW_COLOR] = op[sb_ui.SB_SHADOW_COLOR]
            self.light[c4d.LIGHT_DETAILS_OUTERDISTANCE] = op[sb_ui.SB_DIST]
            
            if op[oh_ui.OH_CAST] == True:
                self.light[c4d.LIGHT_AREADETAILS_FALLOFF_ANGLE] = math.radians(150)
                self.light[c4d.LIGHT_DETAILS_ONLYZ] = True
            elif op[oh_ui.OH_CAST] == False:
                self.light[c4d.LIGHT_AREADETAILS_FALLOFF_ANGLE] = math.radians(180)
                self.light[c4d.LIGHT_DETAILS_ONLYZ] = False

            self.light[c4d.LIGHT_AREADETAILS_SHOWINRENDER] = op[sb_ui.SB_SB_CAMERA]
            self.light[c4d.LIGHT_AREADETAILS_SHOWINREFLECTION] = op[sb_ui.SB_REFLECTION]
            self.light[c4d.LIGHT_AREADETAILS_ADDGRAIN] = op[sb_ui.SB_ADDGAIN]
            self.light[c4d.LIGHT_AREADETAILS_SHOWINSPECULAR] = op[sb_ui.SB_SPECULAR]
            self.light[c4d.LIGHT_DETAILS_SPECULAR] = op[sb_ui.SB_SPECULAR]
            self.light[c4d.LIGHT_AREADETAILS_SAMPLES] = op[sb_ui.SB_SAMPLES]

            self.light[c4d.LIGHT_EXCLUSION_LIST] = op[sb_ui.SB_LIGHT_OBJECT]

            if op[sb_ui.SB_LIGHT_PRO] == sb_ui.SB_EXCLUDE:
                self.light[c4d.LIGHT_EXCLUSION_MODE] = 1

            elif op[sb_ui.SB_LIGHT_PRO] == sb_ui.SB_INCLUDE:
                self.light[c4d.LIGHT_EXCLUSION_MODE] = 0

            if op[sb_ui.SB_USED_BRIGHTNESS_PLANE] == True:
                self.light[c4d.LIGHT_BRIGHTNESS] = op[sb_ui.SB_BRIGHTNESS]
                self.light[c4d.LIGHT_AREADETAILS_BRIGHTNESS] = op[sb_ui.SB_BRIGHTNESS_PLANE]

            elif op[sb_ui.SB_USED_BRIGHTNESS_PLANE] == False:
                self.light[c4d.LIGHT_BRIGHTNESS] = op[sb_ui.SB_BRIGHTNESS]
                self.light[c4d.LIGHT_AREADETAILS_BRIGHTNESS] = op[sb_ui.SB_BRIGHTNESS] * 2

            if op[sb_ui.SB_LIGHT_ON] == True:
                self.light[c4d.ID_BASEOBJECT_GENERATOR_FLAG] = 1

            elif op[sb_ui.SB_LIGHT_ON] == False:
                self.light[c4d.ID_BASEOBJECT_GENERATOR_FLAG] = 0

            # формат тени
            if op[sb_ui.SB_LIGHT_SHADOWTYPE] == sb_ui.SB_SH_AREA:
                self.light[c4d.LIGHT_SHADOWTYPE_VIRTUAL] = 3

            elif op[sb_ui.SB_LIGHT_SHADOWTYPE] == sb_ui.SB_SH_NONE:
                self.light[c4d.LIGHT_SHADOWTYPE_VIRTUAL] = 0

            elif op[sb_ui.SB_LIGHT_SHADOWTYPE] == sb_ui.SB_SH_RAY:
                self.light[c4d.LIGHT_SHADOWTYPE_VIRTUAL] = 2

            elif op[sb_ui.SB_LIGHT_SHADOWTYPE] == sb_ui.SB_SH_SOFT:
                self.light[c4d.LIGHT_SHADOWTYPE_VIRTUAL] = 1

            # видемость во вьюпорте
            if op[sb_ui.SB_SHOW_FALLOFF] == False:
                self.light[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 1
            elif op[sb_ui.SB_SHOW_FALLOFF] == True:
                self.light[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 0
            #-------------------------------------------------------------------------------------------------

            #------------------------------------------------------------------------------------------------- Профиль софтбокса
            # если софт квадратный
            if op[sb_ui.SB_MODE] == sb_ui.SB_SOFTBOX:

                self.softbox_start = c4d.BaseObject(5186)
                self.softbox_start.SetName(op.GetName() + ' start')
                self.softbox_start.InsertUnder(self.softbox)
                self.softbox_start[c4d.PRIM_PLANE] = 0
                self.softbox_start[c4d.PRIM_RECTANGLE_WIDTH] = op[sb_ui.SB_WIDTH]
                self.softbox_start[c4d.PRIM_RECTANGLE_HEIGHT] = op[sb_ui.SB_HIDTH]

                self.softbox_end = c4d.BaseObject(5186)
                self.softbox_end.SetName(op.GetName() + ' end')
                self.softbox_end.InsertUnder(self.softbox)
                self.softbox_end[c4d.PRIM_PLANE] = 0
                self.softbox_end[c4d.PRIM_RECTANGLE_WIDTH] = op[sb_ui.SB_WIDTH] * 0.7
                self.softbox_end[c4d.PRIM_RECTANGLE_HEIGHT] = op[sb_ui.SB_HIDTH] * 0.7

                if self.softbox_start[c4d.PRIM_RECTANGLE_WIDTH] >= self.softbox_start[c4d.PRIM_RECTANGLE_HEIGHT]:
                    self.softbox_end[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Z] = -(self.softbox_start[c4d.PRIM_RECTANGLE_WIDTH] * 0.2)
                elif self.softbox_start[c4d.PRIM_RECTANGLE_WIDTH] <= self.softbox_start[c4d.PRIM_RECTANGLE_HEIGHT]:
                    self.softbox_end[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Z] = -(self.softbox_start[c4d.PRIM_RECTANGLE_HEIGHT] * 0.2)
                elif self.softbox_start[c4d.PRIM_RECTANGLE_WIDTH] == self.softbox_start[c4d.PRIM_RECTANGLE_HEIGHT]:
                    self.softbox_end[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Z] = -(self.softbox_start[c4d.PRIM_RECTANGLE_HEIGHT] * 0.2)

                self.light[c4d.LIGHT_AREADETAILS_SHAPE] = 1
                self.light[c4d.LIGHT_AREADETAILS_SIZEX] = self.softbox_start[c4d.PRIM_RECTANGLE_WIDTH]
                self.light[c4d.LIGHT_AREADETAILS_SIZEY] = self.softbox_start[c4d.PRIM_RECTANGLE_HEIGHT]

            # если софт круглый
            elif op[sb_ui.SB_MODE] == sb_ui.SB_SPOT:

                self.softbox_start = c4d.BaseObject(5181)
                self.softbox_start.SetName(op.GetName() + ' start')
                self.softbox_start.InsertUnder(self.softbox)
                self.softbox_start[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Y] = 0
                self.softbox_start[c4d.PRIM_PLANE] = 0
                self.softbox_start[c4d.PRIM_CIRCLE_RADIUS] = op[sb_ui.SB_WIDTH]/2

                self.softbox_end = c4d.BaseObject(5181)
                self.softbox_end.SetName(op.GetName() + ' end')
                self.softbox_end.InsertUnder(self.softbox)
                self.softbox_end[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Z] = -(op[sb_ui.SB_WIDTH] * 0.2)
                self.softbox_end[c4d.PRIM_PLANE] = 0
                self.softbox_end[c4d.PRIM_CIRCLE_RADIUS] = self.softbox_start[c4d.PRIM_CIRCLE_RADIUS] * 0.7

                self.light[c4d.LIGHT_AREADETAILS_SHAPE] = 0
                self.light[c4d.LIGHT_AREADETAILS_SIZEX] = self.softbox_start[c4d.PRIM_CIRCLE_RADIUS] * 2
                self.light[c4d.LIGHT_AREADETAILS_SIZEY] = self.softbox_start[c4d.PRIM_CIRCLE_RADIUS] * 2

            return self.base
            #-------------------------------------------------------------------------------------------------

        elif rd[c4d.RDATA_RENDERENGINE] != S.Standard or rd[c4d.RDATA_RENDERENGINE] != S.Physical:
            return None

        return self.base
    #------------------------------------------------------------------------- КОНЕЦ Генерации объекта


    #----------------------------------------------------------------------- Кнопки и сценарии нажатия
    def Message(self, op, type, data):

        #-------------------------------------------------------------------------------------------------
        if type == c4d.MSG_DESCRIPTION_COMMAND:

            # Helper
            if data["id"][0].id == sb_ui.SB_HELP:

                # if self.dialog is None:
                self.dialog = Helper()
                self.dialog.show(os.path.join(h.softbox_URL), S.STR_BROWSERDIALOG_TITLE, 200, 100, 700, 700)

            #-------------------------------------------------------------------------------------------------
            # Add target object tag
            if data["id"][0].id == sb_ui.SB_ADD_TARGET_TAG:

                if op.GetTag(5676) == None:

                    self.TargetTag = op.MakeTag(5676)
                    self.TargetTag.SetName(op.GetName() + ' target')
                    self.TargetTag.ChangeNBit(c4d.NBIT_OHIDE, c4d.NBITCONTROL_SET)

                elif op.GetTag(5676) != None:

                    self.TargetTag = op.GetTag(5676)
                    self.TargetTag.Remove()
        #-------------------------------------------------------------------------------------------------

        #------------------------------------------------------------------------------------------------- Настроийки цвета теней

        if op[sb_ui.SB_LOCK] == True:

            CV = c4d.utils.RGBToHSV(op[sb_ui.SB_LIGHT_COLOR])

            if CV[0] <= 0.5:
                CR = c4d.Vector(CV[0] + 0.5 , op[sb_ui.SB_SHADOW_DENSITY], op[sb_ui.SB_SHADOW_VALUE])
                op[sb_ui.SB_SHADOW_COLOR] = c4d.utils.HSVToRGB(CR)
            elif CV[0] >= 0.5:
                CR = c4d.Vector(CV[0] - 0.5 , op[sb_ui.SB_SHADOW_DENSITY], op[sb_ui.SB_SHADOW_VALUE])
                op[sb_ui.SB_SHADOW_COLOR] = c4d.utils.HSVToRGB(CR)
            elif CV[0] == 0.5:
                CR = c4d.Vector(0, op[sb_ui.SB_SHADOW_DENSITY], op[sb_ui.SB_SHADOW_VALUE])
                op[sb_ui.SB_SHADOW_COLOR] = c4d.utils.HSVToRGB(CR)
        #-------------------------------------------------------------------------------------------------

        #-------------------------------------------------------------------------------------------------
        # ведущий свет
        if op[sb_ui.SB_USED] == True:

            if op[sb_ui.SB_LINK] != None and op[sb_ui.SB_INVERT_COLOR] == True:

                if op[sb_ui.SB_LINK].GetType() == sb_ui.SBOX:
                    instLight = op[sb_ui.SB_LINK]

                    CV = c4d.utils.RGBToHSV(instLight[sb_ui.SB_LIGHT_COLOR])

                    if CV[0] <= 0.5:
                        CR = c4d.Vector(CV[0] + 0.5 , CV[1], CV[2])
                        op[sb_ui.SB_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] >= 0.5:
                        CR = c4d.Vector(CV[0] - 0.5 , CV[1], CV[2])
                        op[sb_ui.SB_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] == 0.5:
                        CR = c4d.Vector(0, CV[1], CV[2])
                        op[sb_ui.SB_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)

                elif op[sb_ui.SB_LINK].GetType() == bc_ui.BOUNCE:
                    instLight = op[sb_ui.SB_LINK]

                    CV = c4d.utils.RGBToHSV(instLight[bc_ui.BC_LIGHT_COLOR])

                    if CV[0] <= 0.5:
                        CR = c4d.Vector(CV[0] + 0.5 , CV[1], CV[2])
                        op[sb_ui.SB_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] >= 0.5:
                        CR = c4d.Vector(CV[0] - 0.5 , CV[1], CV[2])
                        op[sb_ui.SB_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] == 0.5:
                        CR = c4d.Vector(0, CV[1], CV[2])
                        op[sb_ui.SB_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)

                elif op[sb_ui.SB_LINK].GetType() == oh_ui.OVERHEAD:
                    instLight = op[sb_ui.SB_LINK]

                    CV = c4d.utils.RGBToHSV(instLight[oh_ui.OH_LIGHT_COLOR])

                    if CV[0] <= 0.5:
                        CR = c4d.Vector(CV[0] + 0.5 , CV[1], CV[2])
                        op[sb_ui.SB_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] >= 0.5:
                        CR = c4d.Vector(CV[0] - 0.5 , CV[1], CV[2])
                        op[sb_ui.SB_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] == 0.5:
                        CR = c4d.Vector(0, CV[1], CV[2])
                        op[sb_ui.SB_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)

                elif op[sb_ui.SB_LINK].GetType() == d_ui.DAYLIGHT:
                    instLight = op[sb_ui.SB_LINK]

                    CV = c4d.utils.RGBToHSV(instLight[d_ui.DL_LIGHT_COLOR])

                    if CV[0] <= 0.5:
                        CR = c4d.Vector(CV[0] + 0.5 , CV[1], CV[2])
                        op[sb_ui.SB_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] >= 0.5:
                        CR = c4d.Vector(CV[0] - 0.5 , CV[1], CV[2])
                        op[sb_ui.SB_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] == 0.5:
                        CR = c4d.Vector(0, CV[1], CV[2])
                        op[sb_ui.SB_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)

                elif op[sb_ui.SB_LINK].GetType() == gl_ui.GLOBALLIGHT:
                    instLight = op[sb_ui.SB_LINK]

                    CV = c4d.utils.RGBToHSV(instLight[gl_ui.GL_LIGHT_COLOR])

                    if CV[0] <= 0.5:
                        CR = c4d.Vector(CV[0] + 0.5 , CV[1], CV[2])
                        op[sb_ui.SB_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] >= 0.5:
                        CR = c4d.Vector(CV[0] - 0.5 , CV[1], CV[2])
                        op[sb_ui.SB_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] == 0.5:
                        CR = c4d.Vector(0, CV[1], CV[2])
                        op[sb_ui.SB_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)

                elif op[sb_ui.SB_LINK].GetType() == 5102:
                    instLight = op[sb_ui.SB_LINK]

                    CV = c4d.utils.RGBToHSV(instLight[c4d.LIGHT_COLOR])

                    if CV[0] <= 0.5:
                        CR = c4d.Vector(CV[0] + 0.5 , CV[1], CV[2])
                        op[sb_ui.SB_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] >= 0.5:
                        CR = c4d.Vector(CV[0] - 0.5 , CV[1], CV[2])
                        op[sb_ui.SB_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] == 0.5:
                        CR = c4d.Vector(0, CV[1], CV[2])
                        op[sb_ui.SB_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)

            elif op[sb_ui.SB_LINK] != None and op[sb_ui.SB_INVERT_COLOR] == False:

                if op[sb_ui.SB_LINK].GetType() == sb_ui.SBOX:
                    instLight = op[sb_ui.SB_LINK]

                    op[sb_ui.SB_LIGHT_COLOR] = instLight[sb_ui.SB_LIGHT_COLOR]

                elif op[sb_ui.SB_LINK].GetType() == bc_ui.BOUNCE:
                    instLight = op[sb_ui.SB_LINK]

                    op[sb_ui.SB_LIGHT_COLOR] = instLight[bc_ui.BC_LIGHT_COLOR]

                elif op[sb_ui.SB_LINK].GetType() == oh_ui.OVERHEAD:
                    instLight = op[sb_ui.SB_LINK]

                    op[sb_ui.SB_LIGHT_COLOR] = instLight[oh_ui.OH_LIGHT_COLOR]

                elif op[sb_ui.SB_LINK].GetType() == d_ui.DAYLIGHT:
                    instLight = op[sb_ui.SB_LINK]

                    op[sb_ui.SB_LIGHT_COLOR] = instLight[d_ui.DL_LIGHT_COLOR]

                elif op[sb_ui.SB_LINK].GetType() == gl_ui.GLOBALLIGHT:
                    instLight = op[sb_ui.SB_LINK]

                    op[sb_ui.SB_LIGHT_COLOR] = instLight[gl_ui.GL_LIGHT_COLOR]

                elif op[sb_ui.SB_LINK].GetType() == 5102:
                    instLight = op[sb_ui.SB_LINK]

                    op[sb_ui.SB_LIGHT_COLOR] = instLight[c4d.LIGHT_COLOR]

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

        #------------------------------------------------------------------------------------------------- Интерфейс
        if rd[c4d.RDATA_RENDERENGINE] == S.Standard:
            op[sb_ui.SB_RENDERER] = S.R_S

        elif rd[c4d.RDATA_RENDERENGINE] == S.Physical:
            op[sb_ui.SB_RENDERER] = S.R_P

        elif rd[c4d.RDATA_RENDERENGINE] != S.Standard or rd[c4d.RDATA_RENDERENGINE] != S.Physical:
            op[sb_ui.SB_RENDERER] = S.WARNING

        if rd[c4d.RDATA_RENDERENGINE] == S.Standard or rd[c4d.RDATA_RENDERENGINE] == S.Physical:
            
            if op[sb_ui.SB_USED] == True:
                if ID == sb_ui.SB_LIGHT_COLOR:
                    return False

                if ID == sb_ui.SB_LINK:
                    return True

                if ID == sb_ui.SB_INVERT_COLOR:
                    return True

            elif op[sb_ui.SB_USED] == False:
                if ID == sb_ui.SB_LIGHT_COLOR:
                    return True

                if ID == sb_ui.SB_LINK:
                    return False

                if ID == sb_ui.SB_INVERT_COLOR:
                    return False

            if op[sb_ui.SB_LOCK] == True:
                if ID == sb_ui.SB_SHADOW_COLOR:
                    return False

                if ID == sb_ui.SB_SHADOW_DENSITY:
                    return True

                if ID == sb_ui.SB_SHADOW_VALUE:
                    return True

            elif op[sb_ui.SB_LOCK] == False:
                if ID == sb_ui.SB_SHADOW_COLOR:
                    return True

                if ID == sb_ui.SB_SHADOW_DENSITY:
                    return False

                if ID == sb_ui.SB_SHADOW_VALUE:
                    return False

            if op[sb_ui.SB_USED_BRIGHTNESS_PLANE] == True:
                if ID == sb_ui.SB_BRIGHTNESS_PLANE:
                    return True

            elif ID == sb_ui.SB_BRIGHTNESS_PLANE:
                return False

            if rd[c4d.RDATA_RENDERENGINE] == 0:
                if ID == sb_ui.SB_LIGHT_SHADOW_MAXSAMPLES:
                    return True

            elif rd[c4d.RDATA_RENDERENGINE] == 1023342:
                if ID == sb_ui.SB_LIGHT_SHADOW_MAXSAMPLES:
                    return False

            elif rd[c4d.RDATA_RENDERENGINE] == 1019782:
                if ID == sb_ui.SB_LIGHT_SHADOW_MAXSAMPLES:
                    return False

            elif rd[c4d.RDATA_RENDERENGINE] == 1029988:
                if ID == sb_ui.SB_LIGHT_SHADOW_MAXSAMPLES:
                    return False

            if op[sb_ui.SB_MODE] == sb_ui.SB_SOFTBOX:
                if ID == sb_ui.SB_HIDTH:
                    return True

            elif ID == sb_ui.SB_HIDTH:
                return False

            if op[sb_ui.SB_LIGHT_SHADOWTYPE] == sb_ui.SB_SH_NONE:
                if ID == sb_ui.SB_LIGHT_SHADOW_DENSITY:
                    return False
                if ID == sb_ui.SB_LIGHT_SHADOW_MAXSAMPLES:
                    return False
                if ID == sb_ui.SB_LIGHT_SHADOW_MAPSIZEX:
                    return False

            elif op[sb_ui.SB_LIGHT_SHADOWTYPE] == sb_ui.SB_SH_AREA:
                if ID == sb_ui.SB_LIGHT_SHADOW_DENSITY:
                    return True
                if ID == sb_ui.SB_LIGHT_SHADOW_MAXSAMPLES:
                    return True
                if ID == sb_ui.SB_LIGHT_SHADOW_MAPSIZEX:
                    return False

            elif op[sb_ui.SB_LIGHT_SHADOWTYPE] == sb_ui.SB_SH_RAY:
                if ID == sb_ui.SB_LIGHT_SHADOW_DENSITY:
                    return True
                if ID == sb_ui.SB_LIGHT_SHADOW_MAXSAMPLES:
                    return False
                if ID == sb_ui.SB_LIGHT_SHADOW_MAPSIZEX:
                    return False

            elif op[sb_ui.SB_LIGHT_SHADOWTYPE] == sb_ui.SB_SH_SOFT:
                if ID == sb_ui.SB_LIGHT_SHADOW_DENSITY:
                    return True
                if ID == sb_ui.SB_LIGHT_SHADOW_MAXSAMPLES:
                    return False
                if ID == sb_ui.SB_LIGHT_SHADOW_MAPSIZEX:
                    return True

        elif rd[c4d.RDATA_RENDERENGINE] != S.Standard or rd[c4d.RDATA_RENDERENGINE] != S.Physical:

            if ID == sb_ui.SB_CAST:
                return False

            if ID == sb_ui.SB_USED:
                return False

            if ID == sb_ui.SB_LINK:
                return False

            if ID == sb_ui.SB_INVERT_COLOR:
                return False

            if ID == sb_ui.SB_ADD_TARGET_TAG:
                return False

            if ID == sb_ui.SB_MODE:
                return False
            
            if ID == sb_ui.SB_WIDTH:
                return False

            if ID == sb_ui.SB_HIDTH:
                return False

            if ID == sb_ui.SB_DIST:
                return False

            if ID == sb_ui.SB_LIGHT_COLOR:
                return False
            
            if ID == sb_ui.SB_BRIGHTNESS:
                return False

            if ID == sb_ui.SB_SAMPLES:
                return False

            if ID == sb_ui.SB_USED_BRIGHTNESS_PLANE:
                return False

            if ID == sb_ui.SB_BRIGHTNESS_PLANE:
                return False
            
            if ID == sb_ui.SB_LIGHT_SHADOWTYPE:
                return False

            if ID == sb_ui.SB_LOCK:
                return False

            if ID == sb_ui.SB_SHADOW_COLOR:
                return False

            if ID == sb_ui.SB_SHADOW_DENSITY:
                return False
            
            if ID == sb_ui.SB_SHADOW_VALUE:
                return False

            if ID == sb_ui.SB_LIGHT_SHADOW_DENSITY:
                return False

            if ID == sb_ui.SB_LIGHT_SHADOW_MAXSAMPLES:
                return False

            if ID == sb_ui.SB_LIGHT_SHADOW_MAPSIZEX:
                return False

            if ID == sb_ui.SB_SB_CAMERA:
                return False
            
            if ID == sb_ui.SB_REFLECTION:
                return False

            if ID == sb_ui.SB_SPECULAR:
                return False

            if ID == sb_ui.SB_SB_TRANSPARENCY:
                return False

            if ID == sb_ui.SB_LIGHT_ON:
                return False
            
            if ID == sb_ui.SB_V_EDITOR:
                return False

            if ID == sb_ui.SB_ADDGAIN:
                return False

            if ID == sb_ui.SB_SHOW_FALLOFF:
                return False

        return True
    #---------------------------------------------------------------------- КОНЕЦ  выкл/вкл интерфейса


#--------------------------------------------------------------------------------------- КОНЕЦ SoftBox


# инициализация компонентов
if __name__ == '__main__':

    dir, file = os.path.split(__file__)

    # SoftBox
    iconSB = c4d.bitmaps.BaseBitmap()
    iconSB.InitWith(os.path.join(dir, S.pathicons, S.softboxIcon))
    plugins.RegisterObjectPlugin(id = sb_ui.SBOX, str = "SoftBox", g = SoftBox, description = "SoftBox", info = c4d.OBJECT_GENERATOR, icon = iconSB )
