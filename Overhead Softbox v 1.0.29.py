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




#------------------------------------------------------------------------------------- OverheadSoftBox
class OverheadSoftBox(c4d.plugins.ObjectData):


    dialog = None
    HANDLECOUNT = 5


    #-------------------------------------------------------------------------------- Оптимизация кэша
    def __init__(self):

        self.SetOptimizeCache(True)
    #-------------------------------------------------------------------------------------------------


    #------------------------------------------------------------------- Значение поумолчанию настроек
    def Init(self, op):

        # инициализация настроек интерфейса
        self.InitAttr(op, float, [oh_ui.OH_WIDTH])
        self.InitAttr(op, float, [oh_ui.OH_HIDTH])
        self.InitAttr(op, float, [oh_ui.OH_RADIUS_SPLINE])
        self.InitAttr(op, float, [oh_ui.OH_DIST])

        self.InitAttr(op, c4d.Vector, [oh_ui.OH_COLOR_BOX])
        self.InitAttr(op, bool, [oh_ui.OH_SHOW_BOX])
        self.InitAttr(op, bool, [oh_ui.OH_SHOW_FALLOFF])
        self.InitAttr(op, bool, [oh_ui.OH_INFINITE])

        self.InitAttr(op, c4d.Vector, [oh_ui.OH_LIGHT_COLOR])
        self.InitAttr(op, float, [oh_ui.OH_BRIGHTNESS])
        self.InitAttr(op, float, [oh_ui.OH_BRIGHTNESS_PLANE])
        self.InitAttr(op, bool, [oh_ui.OH_USED_BRIGHTNESS_PLANE])

        self.InitAttr(op, long, [oh_ui.OH_LIGHT_SHADOWTYPE])
        self.InitAttr(op, bool, [oh_ui.OH_LOCK])
        self.InitAttr(op, c4d.Vector, [oh_ui.OH_SHADOW_COLOR])
        self.InitAttr(op, float, [oh_ui.OH_SHADOW_DENSITY])
        self.InitAttr(op, float, [oh_ui.OH_SHADOW_VALUE])
        self.InitAttr(op, long, [oh_ui.OH_SHADOW_FALLOFF])
        self.InitAttr(op, float, [oh_ui.OH_LIGHT_SHADOW_DENSITY])
        self.InitAttr(op, float, [oh_ui.OH_LIGHT_SHADOW_MAXSAMPLES])
        self.InitAttr(op, float, [oh_ui.OH_LIGHT_SHADOW_MAPSIZEX])

        self.InitAttr(op, bool, [oh_ui.OH_CAST])
        self.InitAttr(op, bool, [oh_ui.OH_OH_CAMERA])
        self.InitAttr(op, bool, [oh_ui.OH_OH_TRANSPARENCY])
        self.InitAttr(op, bool, [oh_ui.OH_LIGHT_ON])
        self.InitAttr(op, bool, [oh_ui.OH_REFLECTION])
        self.InitAttr(op, bool, [oh_ui.OH_SPECULAR])

        self.InitAttr(op, bool, [oh_ui.OH_V_EDITOR])
        self.InitAttr(op, bool, [oh_ui.OH_VIEWPORT_FLOATVIEW])
        self.InitAttr(op, bool, [oh_ui.OH_ADDGAIN])
        self.InitAttr(op, long, [oh_ui.OH_MODE])
        self.InitAttr(op, int, [oh_ui.OH_SAMPLES])
        self.InitAttr(op, c4d.InExcludeData, [oh_ui.OH_LIGHT_OBJECT])
        self.InitAttr(op, bool, [oh_ui.OH_USED])
        self.InitAttr(op, bool, [oh_ui.OH_INVERT_COLOR])


        # значения поумолчанию
        op[oh_ui.OH_WIDTH] = 900.0
        op[oh_ui.OH_HIDTH] = 450.0
        op[oh_ui.OH_RADIUS_SPLINE] = 0
        op[oh_ui.OH_DIST] = 350.0
        op[oh_ui.OH_COLOR_BOX] = c4d.Vector(0, 0, 0)
        op[oh_ui.OH_SHOW_BOX] = True
        op[oh_ui.OH_SHOW_FALLOFF] = False
        op[oh_ui.OH_INFINITE] = True

        op[oh_ui.OH_LIGHT_COLOR] = c4d.Vector(0.91, 0.982, 1)
        op[oh_ui.OH_BRIGHTNESS] = 1.0
        op[oh_ui.OH_BRIGHTNESS_PLANE] = 1.0
        op[oh_ui.OH_USED_BRIGHTNESS_PLANE] = False

        op[oh_ui.OH_LIGHT_SHADOWTYPE] = oh_ui.OH_SH_AREA
        op[oh_ui.OH_LOCK] = True
        op[oh_ui.OH_SHADOW_COLOR] = c4d.Vector(0, 0, 0)
        op[oh_ui.OH_SHADOW_DENSITY] = 0.5
        op[oh_ui.OH_SHADOW_VALUE] = 0.2
        op[oh_ui.OH_SHADOW_FALLOFF] = oh_ui.OH_SHADOW_FALLOFF_INVERS
        op[oh_ui.OH_LIGHT_SHADOW_MAXSAMPLES] = 300
        op[oh_ui.OH_LIGHT_SHADOW_DENSITY] = 1.0
        op[oh_ui.OH_LIGHT_SHADOW_MAPSIZEX] = 250.0

        op[oh_ui.OH_USED] = False
        op[oh_ui.OH_INVERT_COLOR] = False

        op[oh_ui.OH_CAST] = True
        op[oh_ui.OH_OH_CAMERA] = False
        op[oh_ui.OH_ADDGAIN] = False
        op[oh_ui.OH_OH_TRANSPARENCY] = True
        op[oh_ui.OH_LIGHT_ON] = True
        op[oh_ui.OH_REFLECTION] = True
        op[oh_ui.OH_SPECULAR] = True

        op[oh_ui.OH_V_EDITOR] = True
        op[oh_ui.OH_VIEWPORT_FLOATVIEW] = True

        op[oh_ui.OH_MODE] = oh_ui.OH_SOFTBOX

        op[oh_ui.OH_SAMPLES] = 40
        op[oh_ui.OH_LIGHT_OBJECT] = c4d.InExcludeData()

        return True
    #-------------------------------------------------------------------------------------------------


    #------------------------------------------------------------------------------------------- Ручки
    def GetHandleCount(self, op):

        return self.HANDLECOUNT

    def GetHandle(self, op, i, info):

        wight = op[oh_ui.OH_WIDTH]
        if wight is None: wight = 900

        hight = op[oh_ui.OH_HIDTH]
        if hight is None: hight = 450

        dist = op[oh_ui.OH_DIST]
        if dist is None: dist = 350.0

        doc = op.GetDocument()
        rd = doc.GetActiveRenderData()

        if rd[c4d.RDATA_RENDERENGINE] == S.Standard or rd[c4d.RDATA_RENDERENGINE] == S.Physical:

            if op[oh_ui.OH_MODE] == oh_ui.OH_SOFTBOX:
                if i is 0:
                    info.position = c4d.Vector(wight/2, 0.0, 0.0)
                    info.direction = c4d.Vector(1.0, 0.0, 0.0)
                elif i is 1:
                    info.position = c4d.Vector(0.0, 0.0, hight/2)
                    info.direction = c4d.Vector(0.0, 0.0, 1.0)
                elif i is 2:
                    info.position = c4d.Vector(0.0, 0.0, -hight/2)
                    info.direction = c4d.Vector(0.0, 0.0, -1.0)
                elif i is 3:
                    info.position = c4d.Vector(-wight/2, 0.0, 0.0)
                    info.direction = c4d.Vector(-1.0, 0.0, 0.0)
                if op[oh_ui.OH_SHADOW_FALLOFF] == oh_ui.OH_SHADOW_FALLOFF_INVERS or op[oh_ui.OH_SHADOW_FALLOFF] == oh_ui.OH_SHADOW_FALLOFF_LINER:
                    if i is 4:
                        info.position = c4d.Vector(0.0, -dist, 0.0)
                        info.direction = c4d.Vector(0.0, -1.0, 0.0)

            elif op[oh_ui.OH_MODE] == oh_ui.OH_SPOT :
                if i is 0:
                    info.position = c4d.Vector(wight/2, 0.0, 0.0)
                    info.direction = c4d.Vector(1.0, 0.0, 0.0)
                elif i is 1:
                    info.position = c4d.Vector(0.0, 0.0, wight/2)
                    info.direction = c4d.Vector(0.0, 0.0, 1.0)
                elif i is 2:
                    info.position = c4d.Vector(0.0, 0.0, -wight/2)
                    info.direction = c4d.Vector(0.0, 0.0, -1.0)
                elif i is 3:
                    info.position = c4d.Vector(-wight/2, 0.0, 0.0)
                    info.direction = c4d.Vector(-1.0, 0.0, 0.0)
                if op[oh_ui.OH_SHADOW_FALLOFF] == oh_ui.OH_SHADOW_FALLOFF_INVERS or op[oh_ui.OH_SHADOW_FALLOFF] == oh_ui.OH_SHADOW_FALLOFF_LINER:
                    if i is 4:
                        info.position = c4d.Vector(0.0, -dist, 0.0)
                        info.direction = c4d.Vector(0.0, -1.0, 0.0)

    def SetHandle(self, op, i, p, info):

        data = op.GetDataInstance()
        if data is None: return

        tmp = c4d.HandleInfo()
        self.GetHandle(op, i, tmp)

        val = (p-tmp.position)*info.direction

        if op[oh_ui.OH_MODE] == oh_ui.OH_SOFTBOX:
            if i is 0:
                op[oh_ui.OH_WIDTH] = c4d.utils.FCut(op[oh_ui.OH_WIDTH]+val, 0.0, sys.maxint)
            elif i is 1:
                op[oh_ui.OH_HIDTH] = c4d.utils.FCut(op[oh_ui.OH_HIDTH]+val, 0.0, sys.maxint)
            elif i is 2:
                op[oh_ui.OH_HIDTH] = c4d.utils.FCut(op[oh_ui.OH_HIDTH]+val, 0.0, sys.maxint)
            elif i is 3:
                op[oh_ui.OH_WIDTH] = c4d.utils.FCut(op[oh_ui.OH_WIDTH]+val, 0.0, sys.maxint)

            if op[oh_ui.OH_SHADOW_FALLOFF] == oh_ui.OH_SHADOW_FALLOFF_INVERS or op[oh_ui.OH_SHADOW_FALLOFF] == oh_ui.OH_SHADOW_FALLOFF_LINER:
                if i is 4:
                    op[oh_ui.OH_DIST] = c4d.utils.FCut(op[oh_ui.OH_DIST]+val, 0.0, sys.maxint)

        elif op[oh_ui.OH_MODE] == oh_ui.OH_SPOT:
            if i is 0:
                op[oh_ui.OH_WIDTH] = c4d.utils.FCut(op[oh_ui.OH_WIDTH]+val, 0.0, sys.maxint)
            elif i is 1:
                op[oh_ui.OH_WIDTH] = c4d.utils.FCut(op[oh_ui.OH_WIDTH]+val, 0.0, sys.maxint)
            elif i is 2:
                op[oh_ui.OH_WIDTH] = c4d.utils.FCut(op[oh_ui.OH_WIDTH]+val, 0.0, sys.maxint)
            elif i is 3:
                op[oh_ui.OH_WIDTH] = c4d.utils.FCut(op[oh_ui.OH_WIDTH]+val, 0.0, sys.maxint)

            if op[oh_ui.OH_SHADOW_FALLOFF] == oh_ui.OH_SHADOW_FALLOFF_INVERS or op[oh_ui.OH_SHADOW_FALLOFF] == oh_ui.OH_SHADOW_FALLOFF_LINER:
                if i is 4:
                    op[oh_ui.OH_DIST] = c4d.utils.FCut(op[oh_ui.OH_DIST]+val, 0.0, sys.maxint)

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
                    # цвет точки
                    bd.SetPen(c4d.GetViewColor(c4d.VIEWCOLOR_ACTIVEPOINT))

                info = c4d.HandleInfo()
                self.GetHandle(op, i, info)
                bd.DrawHandle(info.position, c4d.DRAWHANDLE_MIDDLE, 0)

                # цвет линии
                bd.SetPen(c4d.GetViewColor(c4d.VIEWCOLOR_ACTIVEPOINT))
                
                if i is 4:
                    bd.DrawLine(info.position, c4d.Vector(0), 0)
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

            # выключение в эдиторе
            if op[oh_ui.OH_V_EDITOR] == True:
                self.base[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 0

            elif op[oh_ui.OH_V_EDITOR] == False:
                self.base[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 1

            #------------------------------------------------------------------------------------------------- SoftBox Лофт объект
            self.overhead = c4d.BaseObject(5107)
            self.overhead.SetName(op.GetName() + ' softbox itself')
            self.overhead.InsertUnder(self.base)
            self.overhead[c4d.LOFTOBJECT_ADAPTIVEY] = 0
            self.overhead[c4d.CAP_START] = 1
            self.overhead[c4d.CAP_END] = 0

            if op[oh_ui.OH_REFLECTION] == True:
                self.overhead[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 0

            elif op[oh_ui.OH_REFLECTION] == False:
                self.overhead[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 1

            # tags
            self.tag_comp_softbox = self.overhead.MakeTag(5637)
            self.tag_comp_softbox[c4d.ID_BASELIST_NAME] = (self.overhead.GetName() + ' compositing')
            self.tag_comp_softbox[c4d.COMPOSITINGTAG_SEENBYCAMERA] = op[oh_ui.OH_OH_CAMERA]
            self.tag_comp_softbox[c4d.COMPOSITINGTAG_SEENBYRAYS] = 0
            self.tag_comp_softbox[c4d.COMPOSITINGTAG_SEENBYGI] = 0
            self.tag_comp_softbox[c4d.COMPOSITINGTAG_SEENBYTRANSPARENCY] = op[oh_ui.OH_OH_TRANSPARENCY]
            self.tag_comp_softbox[c4d.COMPOSITINGTAG_SEENBYREFRACTION] = op[oh_ui.OH_OH_TRANSPARENCY]
            self.tag_comp_softbox[c4d.COMPOSITINGTAG_SEENBYREFLECTION] = op[oh_ui.OH_REFLECTION]
            self.tag_comp_softbox[c4d.COMPOSITINGTAG_CASTSHADOW] = op[oh_ui.OH_CAST]
            # для бесконечного пола
            if op[oh_ui.OH_INFINITE] == False:
                self.tag_comp_softbox[c4d.COMPOSITINGTAG_CASTSHADOW] = 0
            elif op[oh_ui.OH_INFINITE] == True:
                self.tag_comp_softbox[c4d.COMPOSITINGTAG_CASTSHADOW] = 1
            #-------------------------------------------------------------------------------------------------

            #------------------------------------------------------------------------------------------------- Общие настройки света
            self.light = c4d.BaseObject(5102)
            self.light.SetName(op.GetName() + ' light')
            self.light.InsertUnder(self.base)
            self.light[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Y] = math.radians(-90)
            self.light[c4d.LIGHT_SHADOWTYPE] = 3
            self.light[c4d.LIGHT_TYPE] = 8
            self.light[c4d.LIGHT_SHADOW_DENSITY] = op[oh_ui.OH_LIGHT_SHADOW_DENSITY]
            self.light[c4d.LIGHT_COLOR] = op[oh_ui.OH_LIGHT_COLOR]
            self.light[c4d.LIGHT_SHADOW_COLOR] = op[oh_ui.OH_SHADOW_COLOR]
            self.light[c4d.LIGHT_DETAILS_OUTERDISTANCE] = op[oh_ui.OH_DIST]
            
            if op[oh_ui.OH_CAST] == True:
                self.light[c4d.LIGHT_AREADETAILS_FALLOFF_ANGLE] = math.radians(150)
                self.light[c4d.LIGHT_DETAILS_ONLYZ] = True
            elif op[oh_ui.OH_CAST] == False:
                self.light[c4d.LIGHT_AREADETAILS_FALLOFF_ANGLE] = math.radians(180)
                self.light[c4d.LIGHT_DETAILS_ONLYZ] = False
            
            self.light[c4d.LIGHT_AREADETAILS_SHOWINRENDER] = op[oh_ui.OH_OH_CAMERA]
            self.light[c4d.LIGHT_AREADETAILS_SHOWINREFLECTION] = op[oh_ui.OH_REFLECTION]
            self.light[c4d.LIGHT_AREADETAILS_SHOWINSPECULAR] = op[oh_ui.OH_SPECULAR]
            self.light[c4d.LIGHT_DETAILS_SPECULAR] = op[oh_ui.OH_SPECULAR]
            self.light[c4d.LIGHT_AREADETAILS_SAMPLES] = op[oh_ui.OH_SAMPLES]
            self.light[c4d.LIGHT_AREADETAILS_ADDGRAIN] = op[oh_ui.OH_ADDGAIN]

            self.light[c4d.LIGHT_EXCLUSION_LIST] = op[oh_ui.OH_LIGHT_OBJECT]

            if op[oh_ui.OH_LIGHT_PRO] == oh_ui.OH_EXCLUDE:
                self.light[c4d.LIGHT_EXCLUSION_MODE] = 1

            elif op[oh_ui.OH_LIGHT_PRO] == oh_ui.OH_INCLUDE:
                self.light[c4d.LIGHT_EXCLUSION_MODE] = 0

            if op[oh_ui.OH_USED_BRIGHTNESS_PLANE] == True:
                self.light[c4d.LIGHT_BRIGHTNESS] = op[oh_ui.OH_BRIGHTNESS]
                self.light[c4d.LIGHT_AREADETAILS_BRIGHTNESS] = op[oh_ui.OH_BRIGHTNESS_PLANE]

            elif op[oh_ui.OH_USED_BRIGHTNESS_PLANE] == False:
                self.light[c4d.LIGHT_BRIGHTNESS] = op[oh_ui.OH_BRIGHTNESS]
                self.light[c4d.LIGHT_AREADETAILS_BRIGHTNESS] = op[oh_ui.OH_BRIGHTNESS] * 2

            if op[oh_ui.OH_SHADOW_FALLOFF] == oh_ui.OH_SHADOW_FALLOFF_INVERS:
                self.light[c4d.LIGHT_DETAILS_FALLOFF] = 10

            elif op[oh_ui.OH_SHADOW_FALLOFF] == oh_ui.OH_SHADOW_FALLOFF_LINER:
                self.light[c4d.LIGHT_DETAILS_FALLOFF] = 8

            elif op[oh_ui.OH_SHADOW_FALLOFF] == oh_ui.OH_SHADOW_FALLOFF_NONE:
                self.light[c4d.LIGHT_DETAILS_FALLOFF] = 0

            if op[oh_ui.OH_LIGHT_ON] == True:
                self.light[c4d.ID_BASEOBJECT_GENERATOR_FLAG] = 1

            elif op[oh_ui.OH_LIGHT_ON] == False:
                self.light[c4d.ID_BASEOBJECT_GENERATOR_FLAG] = 0

            # формат тени
            if op[oh_ui.OH_LIGHT_SHADOWTYPE] == oh_ui.OH_SH_AREA:
                self.light[c4d.LIGHT_SHADOWTYPE_VIRTUAL] = 3

            elif op[oh_ui.OH_LIGHT_SHADOWTYPE] == oh_ui.OH_SH_NONE:
                self.light[c4d.LIGHT_SHADOWTYPE_VIRTUAL] = 0

            elif op[oh_ui.OH_LIGHT_SHADOWTYPE] == oh_ui.OH_SH_RAY:
                self.light[c4d.LIGHT_SHADOWTYPE_VIRTUAL] = 2

            elif op[oh_ui.OH_LIGHT_SHADOWTYPE] == oh_ui.OH_SH_SOFT:
                self.light[c4d.LIGHT_SHADOWTYPE_VIRTUAL] = 1

            # видемость во вьюпорте
            if op[oh_ui.OH_SHOW_FALLOFF] == False:
                self.light[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 1
            elif op[oh_ui.OH_SHOW_FALLOFF] == True:
                self.light[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 0
            #-------------------------------------------------------------------------------------------------

            #------------------------------------------------------------------------------------------------- Профиль софтбокса
            # если софт квадратный
            if op[oh_ui.OH_MODE] == oh_ui.OH_SOFTBOX:

                self.overhead_start = c4d.BaseObject(5186)
                self.overhead_start.SetName(op.GetName() + ' start')
                self.overhead_start.InsertUnder(self.overhead)
                self.overhead_start[c4d.PRIM_PLANE] = 2
                self.overhead_start[c4d.PRIM_RECTANGLE_WIDTH] = op[oh_ui.OH_WIDTH]
                self.overhead_start[c4d.PRIM_RECTANGLE_HEIGHT] = op[oh_ui.OH_HIDTH]

                self.overhead_end = c4d.BaseObject(5186)
                self.overhead_end.SetName(op.GetName() + ' end')
                self.overhead_end.InsertUnder(self.overhead)
                self.overhead_end[c4d.PRIM_PLANE] = 2
                self.overhead_end[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Y] = 100
                self.overhead_end[c4d.PRIM_RECTANGLE_WIDTH] = op[oh_ui.OH_WIDTH] * 0.8
                self.overhead_end[c4d.PRIM_RECTANGLE_HEIGHT] = op[oh_ui.OH_HIDTH] * 0.8

                if self.overhead_start[c4d.PRIM_RECTANGLE_WIDTH] >= self.overhead_start[c4d.PRIM_RECTANGLE_HEIGHT]:
                    self.overhead_end[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Y] = self.overhead_start[c4d.PRIM_RECTANGLE_WIDTH] * 0.1
                elif self.overhead_start[c4d.PRIM_RECTANGLE_WIDTH] <= self.overhead_start[c4d.PRIM_RECTANGLE_HEIGHT]:
                    self.overhead_end[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Y] = self.overhead_start[c4d.PRIM_RECTANGLE_HEIGHT] * 0.1
                elif self.overhead_start[c4d.PRIM_RECTANGLE_WIDTH] == self.overhead_start[c4d.PRIM_RECTANGLE_HEIGHT]:
                    self.overhead_end[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Y] = self.overhead_start[c4d.PRIM_RECTANGLE_HEIGHT] * 0.1

                self.light[c4d.LIGHT_AREADETAILS_SHAPE] = 1
                self.light[c4d.LIGHT_AREADETAILS_SIZEX] = self.overhead_start[c4d.PRIM_RECTANGLE_WIDTH]
                self.light[c4d.LIGHT_AREADETAILS_SIZEY] = self.overhead_start[c4d.PRIM_RECTANGLE_HEIGHT]

            # если софт круглый
            elif op[oh_ui.OH_MODE] == oh_ui.OH_SPOT:

                self.overhead_start = c4d.BaseObject(5181)
                self.overhead_start.SetName(op.GetName() + ' start')
                self.overhead_start.InsertUnder(self.overhead)
                self.overhead_start[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Y] = 0
                self.overhead_start[c4d.PRIM_PLANE] = 2
                self.overhead_start[c4d.PRIM_CIRCLE_RADIUS] = op[oh_ui.OH_WIDTH]/2

                self.overhead_end = c4d.BaseObject(5181)
                self.overhead_end.SetName(op.GetName() + ' end')
                self.overhead_end.InsertUnder(self.overhead)
                self.overhead_end[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Y] = op[oh_ui.OH_WIDTH] * 0.1
                self.overhead_end[c4d.PRIM_PLANE] = 2
                self.overhead_end[c4d.PRIM_CIRCLE_RADIUS] = self.overhead_start[c4d.PRIM_CIRCLE_RADIUS] * 0.8

                self.light[c4d.LIGHT_AREADETAILS_SHAPE] = 0
                self.light[c4d.LIGHT_AREADETAILS_SIZEX] = self.overhead_start[c4d.PRIM_CIRCLE_RADIUS] * 2
                self.light[c4d.LIGHT_AREADETAILS_SIZEY] = self.overhead_start[c4d.PRIM_CIRCLE_RADIUS] * 2
            #-------------------------------------------------------------------------------------------------

        elif rd[c4d.RDATA_RENDERENGINE] != S.Standard or rd[c4d.RDATA_RENDERENGINE] != S.Physical:
            return None

        return self.base
    #------------------------------------------------------------------------- КОНЕЦ Генерации объекта


    #----------------------------------------------------------------------- Кнопки и сценарии нажатия
    def Message(self, op, type, data):

        if type == c4d.MSG_DESCRIPTION_COMMAND:

            # Helper
            if data["id"][0].id == oh_ui.OH_HELP:

                self.dialog = Helper()
                self.dialog.show(os.path.join(h.overhead_URL), S.STR_BROWSERDIALOG_TITLE, 200, 100, 700, 700)

        #------------------------------------------------------------------------------------------------- Настроийки цвета теней
        if op[oh_ui.OH_LOCK] == True:

            CV = c4d.utils.RGBToHSV(op[oh_ui.OH_LIGHT_COLOR])

            if CV[0] <= 0.5:
                CR = c4d.Vector(CV[0] + 0.5 , op[oh_ui.OH_SHADOW_DENSITY], op[oh_ui.OH_SHADOW_VALUE])
                op[oh_ui.OH_SHADOW_COLOR] = c4d.utils.HSVToRGB(CR)
            elif CV[0] >= 0.5:
                CR = c4d.Vector(CV[0] - 0.5 , op[oh_ui.OH_SHADOW_DENSITY], op[oh_ui.OH_SHADOW_VALUE])
                op[oh_ui.OH_SHADOW_COLOR] = c4d.utils.HSVToRGB(CR)
            elif CV[0] == 0.5:
                CR = c4d.Vector(0, op[oh_ui.OH_SHADOW_DENSITY], op[oh_ui.OH_SHADOW_VALUE])
                op[oh_ui.OH_SHADOW_COLOR] = c4d.utils.HSVToRGB(CR)
        #-------------------------------------------------------------------------------------------------

        #-------------------------------------------------------------------------------------------------
        # ведущий свет
        if op[oh_ui.OH_USED] == True:

            if op[oh_ui.OH_LINK] != None and op[oh_ui.OH_INVERT_COLOR] == True:

                if op[oh_ui.OH_LINK].GetType() == sb_ui.SBOX:
                    instLight = op[oh_ui.OH_LINK]

                    CV = c4d.utils.RGBToHSV(instLight[sb_ui.SB_LIGHT_COLOR])

                    if CV[0] <= 0.5:
                        CR = c4d.Vector(CV[0] + 0.5 , CV[1], CV[2])
                        op[oh_ui.OH_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] >= 0.5:
                        CR = c4d.Vector(CV[0] - 0.5 , CV[1], CV[2])
                        op[oh_ui.OH_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] == 0.5:
                        CR = c4d.Vector(0, CV[1], CV[2])
                        op[oh_ui.OH_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)

                elif op[oh_ui.OH_LINK].GetType() == bc_ui.BOUNCE:
                    instLight = op[oh_ui.OH_LINK]

                    CV = c4d.utils.RGBToHSV(instLight[bc_ui.BC_LIGHT_COLOR])

                    if CV[0] <= 0.5:
                        CR = c4d.Vector(CV[0] + 0.5 , CV[1], CV[2])
                        op[oh_ui.OH_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] >= 0.5:
                        CR = c4d.Vector(CV[0] - 0.5 , CV[1], CV[2])
                        op[oh_ui.OH_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] == 0.5:
                        CR = c4d.Vector(0, CV[1], CV[2])
                        op[oh_ui.OH_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)

                elif op[oh_ui.OH_LINK].GetType() == oh_ui.OVERHEAD:
                    instLight = op[oh_ui.OH_LINK]

                    CV = c4d.utils.RGBToHSV(instLight[oh_ui.OH_LIGHT_COLOR])

                    if CV[0] <= 0.5:
                        CR = c4d.Vector(CV[0] + 0.5 , CV[1], CV[2])
                        op[oh_ui.OH_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] >= 0.5:
                        CR = c4d.Vector(CV[0] - 0.5 , CV[1], CV[2])
                        op[oh_ui.OH_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] == 0.5:
                        CR = c4d.Vector(0, CV[1], CV[2])
                        op[oh_ui.OH_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)

                elif op[oh_ui.OH_LINK].GetType() == d_ui.DAYLIGHT:
                    instLight = op[oh_ui.OH_LINK]

                    CV = c4d.utils.RGBToHSV(instLight[d_ui.DL_LIGHT_COLOR])

                    if CV[0] <= 0.5:
                        CR = c4d.Vector(CV[0] + 0.5 , CV[1], CV[2])
                        op[oh_ui.OH_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] >= 0.5:
                        CR = c4d.Vector(CV[0] - 0.5 , CV[1], CV[2])
                        op[oh_ui.OH_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] == 0.5:
                        CR = c4d.Vector(0, CV[1], CV[2])
                        op[oh_ui.OH_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)

                elif op[oh_ui.OH_LINK].GetType() == gl_ui.GLOBALLIGHT:
                    instLight = op[oh_ui.OH_LINK]

                    CV = c4d.utils.RGBToHSV(instLight[gl_ui.GL_LIGHT_COLOR])

                    if CV[0] <= 0.5:
                        CR = c4d.Vector(CV[0] + 0.5 , CV[1], CV[2])
                        op[oh_ui.OH_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] >= 0.5:
                        CR = c4d.Vector(CV[0] - 0.5 , CV[1], CV[2])
                        op[oh_ui.OH_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] == 0.5:
                        CR = c4d.Vector(0, CV[1], CV[2])
                        op[oh_ui.OH_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)

                elif op[oh_ui.OH_LINK].GetType() == 5102:
                    instLight = op[oh_ui.OH_LINK]

                    CV = c4d.utils.RGBToHSV(instLight[c4d.LIGHT_COLOR])

                    if CV[0] <= 0.5:
                        CR = c4d.Vector(CV[0] + 0.5 , CV[1], CV[2])
                        op[oh_ui.OH_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] >= 0.5:
                        CR = c4d.Vector(CV[0] - 0.5 , CV[1], CV[2])
                        op[oh_ui.OH_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] == 0.5:
                        CR = c4d.Vector(0, CV[1], CV[2])
                        op[oh_ui.OH_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)

            elif op[oh_ui.OH_LINK] != None and op[oh_ui.OH_INVERT_COLOR] == False:

                if op[oh_ui.OH_LINK].GetType() == sb_ui.SBOX:
                    instLight = op[oh_ui.OH_LINK]

                    op[oh_ui.OH_LIGHT_COLOR] = instLight[sb_ui.SB_LIGHT_COLOR]

                elif op[oh_ui.OH_LINK].GetType() == bc_ui.BOUNCE:
                    instLight = op[oh_ui.OH_LINK]

                    op[oh_ui.OH_LIGHT_COLOR] = instLight[bc_ui.BC_LIGHT_COLOR]

                elif op[oh_ui.OH_LINK].GetType() == oh_ui.OVERHEAD:
                    instLight = op[oh_ui.OH_LINK]

                    op[oh_ui.OH_LIGHT_COLOR] = instLight[oh_ui.OH_LIGHT_COLOR]

                elif op[oh_ui.OH_LINK].GetType() == d_ui.DAYLIGHT:
                    instLight = op[oh_ui.OH_LINK]

                    op[oh_ui.OH_LIGHT_COLOR] = instLight[d_ui.DL_LIGHT_COLOR]

                elif op[oh_ui.OH_LINK].GetType() == gl_ui.GLOBALLIGHT:
                    instLight = op[oh_ui.OH_LINK]

                    op[oh_ui.OH_LIGHT_COLOR] = instLight[gl_ui.GL_LIGHT_COLOR]

                elif op[oh_ui.OH_LINK].GetType() == 5102:
                    instLight = op[oh_ui.OH_LINK]

                    op[oh_ui.OH_LIGHT_COLOR] = instLight[c4d.LIGHT_COLOR]

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

        #------------------------------------------------------------------------------------------------- Итерфейс
        if rd[c4d.RDATA_RENDERENGINE] == S.Standard:
            op[oh_ui.OH_RENDERER] = S.R_S

        elif rd[c4d.RDATA_RENDERENGINE] == S.Physical:
            op[oh_ui.OH_RENDERER] = S.R_P

        elif rd[c4d.RDATA_RENDERENGINE] != S.Standard and rd[c4d.RDATA_RENDERENGINE] != S.Physical:
            op[oh_ui.OH_RENDERER] = S.WARNING

        if rd[c4d.RDATA_RENDERENGINE] == S.Standard or rd[c4d.RDATA_RENDERENGINE] == S.Physical:

            if op[oh_ui.OH_USED] == True:
                if ID == oh_ui.OH_LIGHT_COLOR:
                    return False

                if ID == oh_ui.OH_LINK:
                    return True

                if ID == oh_ui.OH_INVERT_COLOR:
                    return True

            elif op[oh_ui.OH_USED] == False:
                if ID == oh_ui.OH_LIGHT_COLOR:
                    return True

                if ID == oh_ui.OH_LINK:
                    return False

                if ID == oh_ui.OH_INVERT_COLOR:
                    return False

            if op[oh_ui.OH_SHADOW_FALLOFF] == oh_ui.OH_SHADOW_FALLOFF_INVERS:
                if ID == oh_ui.OH_DIST:
                    return True

            elif op[oh_ui.OH_SHADOW_FALLOFF] == oh_ui.OH_SHADOW_FALLOFF_LINER:
                if ID == oh_ui.OH_DIST:
                    return True

            elif op[oh_ui.OH_SHADOW_FALLOFF] == oh_ui.OH_SHADOW_FALLOFF_NONE:
                if ID == oh_ui.OH_DIST:
                    return False

            if rd[c4d.RDATA_RENDERENGINE] == 0:
                if ID == oh_ui.OH_LIGHT_SHADOW_MAXSAMPLES:
                    return True

            elif rd[c4d.RDATA_RENDERENGINE] == 1023342:
                if ID == oh_ui.OH_LIGHT_SHADOW_MAXSAMPLES:
                    return False

            elif rd[c4d.RDATA_RENDERENGINE] == 1019782:
                if ID == oh_ui.OH_LIGHT_SHADOW_MAXSAMPLES:
                    return False

            elif rd[c4d.RDATA_RENDERENGINE] == 1029988:
                if ID == oh_ui.OH_LIGHT_SHADOW_MAXSAMPLES:
                    return False

            if op[oh_ui.OH_LOCK] == True:
                if ID == oh_ui.OH_SHADOW_COLOR:
                    return False

                if ID == oh_ui.OH_SHADOW_DENSITY:
                    return True

                if ID == oh_ui.OH_SHADOW_VALUE:
                    return True

            elif op[oh_ui.OH_LOCK] == False:
                if ID == oh_ui.OH_SHADOW_COLOR:
                    return True

                if ID == oh_ui.OH_SHADOW_DENSITY:
                    return False

                if ID == oh_ui.OH_SHADOW_VALUE:
                    return False

            if op[oh_ui.OH_USED_BRIGHTNESS_PLANE] == True:
                if ID == oh_ui.OH_BRIGHTNESS_PLANE:
                    return True

            elif ID == oh_ui.OH_BRIGHTNESS_PLANE:
                return False

            if op[oh_ui.OH_MODE] == oh_ui.OH_SOFTBOX:
                if ID == oh_ui.OH_HIDTH:
                    return True

            elif ID == oh_ui.OH_HIDTH:
                return False

            if op[oh_ui.OH_LIGHT_SHADOWTYPE] == oh_ui.OH_SH_NONE:
                if ID == oh_ui.OH_LIGHT_SHADOW_DENSITY:
                    return False
                if ID == oh_ui.OH_LIGHT_SHADOW_MAXSAMPLES:
                    return False
                if ID == oh_ui.OH_LIGHT_SHADOW_MAPSIZEX:
                    return False

            elif op[oh_ui.OH_LIGHT_SHADOWTYPE] == oh_ui.OH_SH_AREA:
                if ID == oh_ui.OH_LIGHT_SHADOW_DENSITY:
                    return True
                if ID == oh_ui.OH_LIGHT_SHADOW_MAXSAMPLES:
                    return True
                if ID == oh_ui.OH_LIGHT_SHADOW_MAPSIZEX:
                    return False

            elif op[oh_ui.OH_LIGHT_SHADOWTYPE] == oh_ui.OH_SH_RAY:
                if ID == oh_ui.OH_LIGHT_SHADOW_DENSITY:
                    return True
                if ID == oh_ui.OH_LIGHT_SHADOW_MAXSAMPLES:
                    return False
                if ID == oh_ui.OH_LIGHT_SHADOW_MAPSIZEX:
                    return False

            elif op[oh_ui.OH_LIGHT_SHADOWTYPE] == oh_ui.OH_SH_SOFT:
                if ID == oh_ui.OH_LIGHT_SHADOW_DENSITY:
                    return True
                if ID == oh_ui.OH_LIGHT_SHADOW_MAXSAMPLES:
                    return False
                if ID == oh_ui.OH_LIGHT_SHADOW_MAPSIZEX:
                    return True

        elif rd[c4d.RDATA_RENDERENGINE] != S.Standard and rd[c4d.RDATA_RENDERENGINE] != S.Physical:

            if ID == oh_ui.OH_CAST:
                return False

            if ID == oh_ui.OH_USED:
                return False

            if ID == oh_ui.OH_LINK:
                return False

            if ID == oh_ui.OH_INVERT_COLOR:
                return False

            if ID == oh_ui.OH_MODE:
                return False
            
            if ID == oh_ui.OH_WIDTH:
                return False

            if ID == oh_ui.OH_HIDTH:
                return False

            if ID == oh_ui.OH_DIST:
                return False

            if ID == oh_ui.OH_LIGHT_COLOR:
                return False
            
            if ID == oh_ui.OH_BRIGHTNESS:
                return False

            if ID == oh_ui.OH_SAMPLES:
                return False

            if ID == oh_ui.OH_USED_BRIGHTNESS_PLANE:
                return False

            if ID == oh_ui.OH_BRIGHTNESS_PLANE:
                return False
            
            if ID == oh_ui.OH_LIGHT_SHADOWTYPE:
                return False

            if ID == oh_ui.OH_LOCK:
                return False

            if ID == oh_ui.OH_SHADOW_COLOR:
                return False

            if ID == oh_ui.OH_SHADOW_DENSITY:
                return False
            
            if ID == oh_ui.OH_SHADOW_VALUE:
                return False

            if ID == oh_ui.OH_LIGHT_SHADOW_DENSITY:
                return False

            if ID == oh_ui.OH_LIGHT_SHADOW_MAXSAMPLES:
                return False

            if ID == oh_ui.OH_LIGHT_SHADOW_MAPSIZEX:
                return False

            if ID == oh_ui.OH_OH_CAMERA:
                return False
            
            if ID == oh_ui.OH_REFLECTION:
                return False

            if ID == oh_ui.OH_SPECULAR:
                return False

            if ID == oh_ui.OH_OH_TRANSPARENCY:
                return False

            if ID == oh_ui.OH_LIGHT_ON:
                return False
            
            if ID == oh_ui.OH_V_EDITOR:
                return False

            if ID == oh_ui.OH_ADDGAIN:
                return False

            if ID == oh_ui.OH_SHOW_FALLOFF:
                return False

            if ID == oh_ui.OH_SHADOW_FALLOFF:
                return False
        #-------------------------------------------------------------------------------------------------

        return True
    #---------------------------------------------------------------------- КОНЕЦ  выкл/вкл интерфейса


#------------------------------------------------------------------------------- КОНЕЦ OverheadSoftBox


# инициализация компонентов
if __name__ == '__main__':

    dir, file = os.path.split(__file__)

    # OverheadSoftBox
    iconOH = c4d.bitmaps.BaseBitmap()
    iconOH.InitWith(os.path.join(dir, S.pathicons, S.overheadIcon))
    plugins.RegisterObjectPlugin(id = oh_ui.OVERHEAD, str = "Overhead SoftBox", g = OverheadSoftBox, description = "OverheadSoftBox", info = c4d.OBJECT_GENERATOR, icon = iconOH )
