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


from module.engine import st_ui
from module.engine import S
from module.engine import h
from module.engine import m
from module.engine.layer import *
from module.engine.helper import *




#-------------------------------------------------------------------------------------------- Studio
class Studio(c4d.plugins.ObjectData):


    dialog = None
    HANDLECOUNT = 10


    #-------------------------------------------------------------------------------- Оптимизация кэша
    def __init__(self):

        self.SetOptimizeCache(True)
    #-------------------------------------------------------------------------------------------------


    #------------------------------------------------------------------- Значение поумолчанию настроек
    def Init(self, op):

        # инициализация настроек интерфейса
        self.InitAttr(op, c4d.Vector, [st_ui.ST_STUDIO_COLOR])
        self.InitAttr(op, long, [st_ui.ST_MODE])
        self.InitAttr(op, long, [st_ui.ST_RENDER_COLOR])
        self.InitAttr(op, float, [st_ui.ST_WIDTH])
        self.InitAttr(op, float, [st_ui.ST_HIDTH])
        self.InitAttr(op, float, [st_ui.ST_DEFTH])
        self.InitAttr(op, float, [st_ui.ST_ROUNDING])
        self.InitAttr(op, int, [st_ui.ST_SUB_VIEWER])
        self.InitAttr(op, int, [st_ui.ST_SUB_RENDER])

        # # значения поумолчанию
        op[st_ui.ST_STUDIO_COLOR] = c4d.Vector(1, 1, 1)

        op[st_ui.ST_MODE] = st_ui.ST_C
        op[st_ui.ST_RENDER_COLOR] = st_ui.ST_COLOR
        op[st_ui.ST_WIDTH] = 300
        op[st_ui.ST_HIDTH] = 300
        op[st_ui.ST_DEFTH] = 300
        op[st_ui.ST_ROUNDING] = 60
        op[st_ui.ST_SUB_VIEWER] = 1
        op[st_ui.ST_SUB_RENDER] = 2

        return True
    #-------------------------------------------------------------------------------------------------


    #------------------------------------------------------------------------------------------- Ручки
    def GetHandleCount(self, op):

        return self.HANDLECOUNT

    def GetHandle(self, op, i, info):

        wight = op[st_ui.ST_WIDTH]
        if wight is None: wight = 300

        hight = op[st_ui.ST_HIDTH]
        if hight is None: hight = 300

        depht = op[st_ui.ST_DEFTH]
        if depht is None: depht = 300

        rad = op[st_ui.ST_ROUNDING]
        if rad is None: rad = 20

        #----------------------------------------------------------------------------------------------------- ручки
        if i is 0:
            info.position = c4d.Vector(wight, 0.0, 0.0)
            info.direction = c4d.Vector(1.0, 0.0, 0.0)

        elif i is 1:
            info.position = c4d.Vector(-wight, 0.0, 0.0)
            info.direction = c4d.Vector(-1.0, 0.0, 0.0)

        elif i is 2:
            if op[st_ui.ST_MODE] == st_ui.ST_C:
                info.position = c4d.Vector(0.0, hight, 0.0)
                info.direction = c4d.Vector(0.0, 1.0, 0.0)

            elif op[st_ui.ST_MODE] == st_ui.ST_S:
                info.position = c4d.Vector(0.0, hight, depht)
                info.direction = c4d.Vector(0.0, 1.0, 1.0)

            elif op[st_ui.ST_MODE] == st_ui.ST_U:
                info.position = c4d.Vector(wight, hight, 0.0)
                info.direction = c4d.Vector(1.0, 1.0, 1.0)

            elif op[st_ui.ST_MODE] == st_ui.ST_L:
                info.position = c4d.Vector(0.0, hight, depht)
                info.direction = c4d.Vector(0.0, 1.0, 1.0)

        elif i is 3:
            info.position = c4d.Vector(0.0, 0.0, depht)
            info.direction = c4d.Vector(0.0, 0.0, 1.0)

        elif i is 4:
            info.position = c4d.Vector(0.0, 0.0, -depht)
            info.direction = c4d.Vector(0.0, 0.0, -1.0)

        elif i is 5:
            if op[st_ui.ST_MODE] == st_ui.ST_C:
                info.position = c4d.Vector(wight, rad, depht-rad)
                info.direction = c4d.Vector(0.0, 1.0, 0.0)

            elif op[st_ui.ST_MODE] == st_ui.ST_S:
                info.position = c4d.Vector(wight, rad, depht-rad)
                info.direction = c4d.Vector(0.0, 1.0, 0.0)

            elif op[st_ui.ST_MODE] == st_ui.ST_U:
                info.position = c4d.Vector(wight-rad, rad, -depht)
                info.direction = c4d.Vector(0.0, 1.0, 0.0)

            elif op[st_ui.ST_MODE] == st_ui.ST_L:
                info.position = c4d.Vector(wight, rad, depht-rad)
                info.direction = c4d.Vector(0.0, 1.0, 0.0)

        elif i is 6:
            if op[st_ui.ST_MODE] == st_ui.ST_C:
                info.position = c4d.Vector(-wight, rad, depht-rad)
                info.direction = c4d.Vector(0.0, 1.0, 0.0)

            elif op[st_ui.ST_MODE] == st_ui.ST_S:
                info.position = c4d.Vector(-wight, rad, depht-rad)
                info.direction = c4d.Vector(0.0, 1.0, 0.0)

            elif op[st_ui.ST_MODE] == st_ui.ST_U:
                info.position = c4d.Vector(wight-rad, rad, depht)
                info.direction = c4d.Vector(0.0, 1.0, 0.0)

            elif op[st_ui.ST_MODE] == st_ui.ST_L:
                info.position = c4d.Vector(-wight, rad, depht-rad)
                info.direction = c4d.Vector(0.0, 1.0, 0.0)

        elif i is 7:
            if op[st_ui.ST_MODE] == st_ui.ST_C:
                info.position = c4d.Vector(-wight, hight-rad, depht-rad)
                info.direction = c4d.Vector(0.0, -1.0, 0.0)

            elif op[st_ui.ST_MODE] == st_ui.ST_S:
                info.position = c4d.Vector(-wight, -rad, -depht+rad)
                info.direction = c4d.Vector(0.0, -1.0, 0.0)

            elif op[st_ui.ST_MODE] == st_ui.ST_U:
                info.position = c4d.Vector(-wight+rad, rad, -depht)
                info.direction = c4d.Vector(0.0, 1.0, 0.0)

            elif op[st_ui.ST_MODE] == st_ui.ST_L:
                info.position = c4d.Vector(0.0, 0.0, 0.0)
                info.direction = c4d.Vector(0.0, 0.0, 0.0)

        elif i is 8:
            if op[st_ui.ST_MODE] == st_ui.ST_C:
                info.position = c4d.Vector(wight, hight-rad, depht-rad)
                info.direction = c4d.Vector(0.0, -1.0, 0.0)

            elif op[st_ui.ST_MODE] == st_ui.ST_S:
                info.position = c4d.Vector(wight, -rad, -depht+rad)
                info.direction = c4d.Vector(0.0, -1.0, 0.0)

            elif op[st_ui.ST_MODE] == st_ui.ST_U:
                info.position = c4d.Vector(-wight+rad, rad, depht)
                info.direction = c4d.Vector(0.0, 1.0, 0.0)

            elif op[st_ui.ST_MODE] == st_ui.ST_L:
                info.position = c4d.Vector(0.0, 0.0, 0.0)
                info.direction = c4d.Vector(0.0, 0.0, 0.0)

    def SetHandle(self, op, i, p, info):

        data = op.GetDataInstance()
        if data is None: return

        tmp = c4d.HandleInfo()
        self.GetHandle(op, i, tmp)

        val = (p-tmp.position)*info.direction

        if i is 0:
            op[st_ui.ST_WIDTH] = c4d.utils.FCut(op[st_ui.ST_WIDTH]+val, op[st_ui.ST_ROUNDING]*2, sys.maxint)
        elif i is 1:
            op[st_ui.ST_WIDTH] = c4d.utils.FCut(op[st_ui.ST_WIDTH]+val, op[st_ui.ST_ROUNDING]*2, sys.maxint)
        elif i is 2:
            op[st_ui.ST_HIDTH] = c4d.utils.FCut(op[st_ui.ST_HIDTH]+val, op[st_ui.ST_ROUNDING]*2, sys.maxint)
        elif i is 3:
            op[st_ui.ST_DEFTH] = c4d.utils.FCut(op[st_ui.ST_DEFTH]+val, op[st_ui.ST_ROUNDING]*2, sys.maxint)
        elif i is 4:
            op[st_ui.ST_DEFTH] = c4d.utils.FCut(op[st_ui.ST_DEFTH]+val, op[st_ui.ST_ROUNDING]*2, sys.maxint)

        elif i is 5 or i is 6 or i is 7 or i is 8:
            op[st_ui.ST_ROUNDING] = c4d.utils.FCut(op[st_ui.ST_ROUNDING]+val, 0.0, op[st_ui.ST_HIDTH]/2)

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

        #----------------------------------------------------------------------------------------------------- Ручки
        if drawpass!=c4d.DRAWPASS_HANDLES: return c4d.DRAWRESULT_SKIP

        bd.SetPen(c4d.GetViewColor(c4d.VIEWCOLOR_ACTIVEPOINT))

        hitid = op.GetHighlightHandle(bd)
        bd.SetMatrix_Matrix(op, bh.GetMg())

        for i in xrange(self.HANDLECOUNT):
            if i==hitid:
                bd.SetPen(c4d.GetViewColor(c4d.VIEWCOLOR_SELECTION_PREVIEW))
            else:
                bd.SetPen(c4d.GetViewColor(c4d.VIEWCOLOR_ACTIVEPOINT))

            if op[st_ui.ST_MODE] == st_ui.ST_C:
                if i is 6:
                    bd.DrawLine(info.position, c4d.Vector(op[st_ui.ST_WIDTH], 0.0, op[st_ui.ST_DEFTH]-op[st_ui.ST_ROUNDING]), 0)
                    bd.DrawLine(info.position, c4d.Vector(op[st_ui.ST_WIDTH], op[st_ui.ST_ROUNDING], op[st_ui.ST_DEFTH]), 0)
                if i is 7:
                    bd.DrawLine(info.position, c4d.Vector(-op[st_ui.ST_WIDTH], 0.0, op[st_ui.ST_DEFTH]-op[st_ui.ST_ROUNDING]), 0)
                    bd.DrawLine(info.position, c4d.Vector(-op[st_ui.ST_WIDTH], op[st_ui.ST_ROUNDING], op[st_ui.ST_DEFTH]), 0)

                if i is 8:
                    bd.DrawLine(info.position, c4d.Vector(-op[st_ui.ST_WIDTH], op[st_ui.ST_HIDTH], op[st_ui.ST_DEFTH]-op[st_ui.ST_ROUNDING]), 0)
                    bd.DrawLine(info.position, c4d.Vector(-op[st_ui.ST_WIDTH], op[st_ui.ST_HIDTH]-op[st_ui.ST_ROUNDING], op[st_ui.ST_DEFTH]), 0)
                if i is 9:
                    bd.DrawLine(info.position, c4d.Vector(op[st_ui.ST_WIDTH], op[st_ui.ST_HIDTH], op[st_ui.ST_DEFTH]-op[st_ui.ST_ROUNDING]), 0)
                    bd.DrawLine(info.position, c4d.Vector(op[st_ui.ST_WIDTH], op[st_ui.ST_HIDTH]-op[st_ui.ST_ROUNDING], op[st_ui.ST_DEFTH]), 0)

            elif op[st_ui.ST_MODE] == st_ui.ST_S:
                if i is 6:
                    bd.DrawLine(info.position, c4d.Vector(op[st_ui.ST_WIDTH], 0.0, op[st_ui.ST_DEFTH]-op[st_ui.ST_ROUNDING]), 0)
                    bd.DrawLine(info.position, c4d.Vector(op[st_ui.ST_WIDTH], op[st_ui.ST_ROUNDING], op[st_ui.ST_DEFTH]), 0)
                if i is 7:
                    bd.DrawLine(info.position, c4d.Vector(-op[st_ui.ST_WIDTH], 0.0, op[st_ui.ST_DEFTH]-op[st_ui.ST_ROUNDING]), 0)
                    bd.DrawLine(info.position, c4d.Vector(-op[st_ui.ST_WIDTH], op[st_ui.ST_ROUNDING], op[st_ui.ST_DEFTH]), 0)

                if i is 8:
                    bd.DrawLine(info.position, c4d.Vector(-op[st_ui.ST_WIDTH], 0.0, -op[st_ui.ST_DEFTH]+op[st_ui.ST_ROUNDING]), 0)
                    bd.DrawLine(info.position, c4d.Vector(-op[st_ui.ST_WIDTH], -op[st_ui.ST_ROUNDING], -op[st_ui.ST_DEFTH]), 0)
                if i is 9:
                    bd.DrawLine(info.position, c4d.Vector(op[st_ui.ST_WIDTH], 0.0, -op[st_ui.ST_DEFTH]+op[st_ui.ST_ROUNDING]), 0)
                    bd.DrawLine(info.position, c4d.Vector(op[st_ui.ST_WIDTH], -op[st_ui.ST_ROUNDING], -op[st_ui.ST_DEFTH]), 0)

            elif op[st_ui.ST_MODE] == st_ui.ST_U:
                if i is 6:
                    bd.DrawLine(info.position, c4d.Vector(op[st_ui.ST_WIDTH]-op[st_ui.ST_ROUNDING], 0.0, -op[st_ui.ST_DEFTH]), 0)
                    bd.DrawLine(info.position, c4d.Vector(op[st_ui.ST_WIDTH], op[st_ui.ST_ROUNDING], -op[st_ui.ST_DEFTH]), 0)
                if i is 7:
                    bd.DrawLine(info.position, c4d.Vector(op[st_ui.ST_WIDTH]-op[st_ui.ST_ROUNDING], 0.0, op[st_ui.ST_DEFTH]), 0)
                    bd.DrawLine(info.position, c4d.Vector(op[st_ui.ST_WIDTH], op[st_ui.ST_ROUNDING], op[st_ui.ST_DEFTH]), 0)

                if i is 8:
                    bd.DrawLine(info.position, c4d.Vector(-op[st_ui.ST_WIDTH]+op[st_ui.ST_ROUNDING], 0.0, -op[st_ui.ST_DEFTH]), 0)
                    bd.DrawLine(info.position, c4d.Vector(-op[st_ui.ST_WIDTH], op[st_ui.ST_ROUNDING], -op[st_ui.ST_DEFTH]), 0)
                if i is 9:
                    bd.DrawLine(info.position, c4d.Vector(-op[st_ui.ST_WIDTH]+op[st_ui.ST_ROUNDING], 0.0, op[st_ui.ST_DEFTH]), 0)
                    bd.DrawLine(info.position, c4d.Vector(-op[st_ui.ST_WIDTH], op[st_ui.ST_ROUNDING], op[st_ui.ST_DEFTH]), 0)

            elif op[st_ui.ST_MODE] == st_ui.ST_L:
                if i is 6:
                    bd.DrawLine(info.position, c4d.Vector(op[st_ui.ST_WIDTH], 0.0, op[st_ui.ST_DEFTH]-op[st_ui.ST_ROUNDING]), 0)
                    bd.DrawLine(info.position, c4d.Vector(op[st_ui.ST_WIDTH], op[st_ui.ST_ROUNDING], op[st_ui.ST_DEFTH]), 0)
                if i is 7:
                    bd.DrawLine(info.position, c4d.Vector(-op[st_ui.ST_WIDTH], 0.0, op[st_ui.ST_DEFTH]-op[st_ui.ST_ROUNDING]), 0)
                    bd.DrawLine(info.position, c4d.Vector(-op[st_ui.ST_WIDTH], op[st_ui.ST_ROUNDING], op[st_ui.ST_DEFTH]), 0)


            info = c4d.HandleInfo()
            self.GetHandle(op, i, info)
            bd.DrawHandle(info.position, c4d.DRAWHANDLE_BIG, 0)
            bd.SetPen(c4d.GetViewColor(c4d.VIEWCOLOR_ACTIVEPOINT))
        #-----------------------------------------------------------------------------------------------------

        return c4d.DRAWRESULT_OK
    #-------------------------------------------------------------------------------- КОНЕЦ Прорисовки


    #------------------------------------------------------------------------------- Генерация объекта
    def GetVirtualObjects(self, op, hierarchyhelp):

        matlayer()

        doc = op.GetDocument()
        rd = doc.GetActiveRenderData()

        root = doc.GetLayerObjectRoot()

        #-------------------------------------------------------------------------------------------------
        # базовый контейнер
        self.base = c4d.BaseObject(c4d.Onull)
        self.base.SetName(op.GetName())

        # сабдив объект для студии
        self.basesub = c4d.BaseObject(1007455)
        self.basesub.SetName('Subdivision Surface ' + op.GetName())
        self.basesub.InsertUnder(self.base)
        self.basesub[c4d.SDSOBJECT_SUBEDITOR_CM] = int(op[st_ui.ST_SUB_VIEWER])
        self.basesub[c4d.SDSOBJECT_SUBRAY_CM] = int(op[st_ui.ST_SUB_RENDER])

        if rd[c4d.RDATA_RENDERENGINE] == S.Standard or rd[c4d.RDATA_RENDERENGINE] == S.Physical:
            # ----------------------------------------------------------------------------------------  текстура на студии
            # если на оп есть текстурТаг
            if op.GetTag(5616) != None:
                # если на оп есть материал, то удалить тэг материала на бэйсе и материал
                if self.basesub.GetTag(5616) != None:
                        self.basesub.GetTag(5616).KillTag()

            # если на оп нет текстурТаг
            elif op.GetTag(5616) == None:

                # если на оп нет материала и не создан сам материал
                if doc.SearchMaterial(op.GetName() + ' studio') == None:
                    
                    self.matIn_ST = c4d.documents.MergeDocument(doc, m.studio_mat, c4d.SCENEFILTER_MATERIALS)
                    self.MatTemp_ST = doc.SearchMaterial('studio')
                    self.MatTemp_ST.SetName(op.GetName() + ' studio')
                    self.MatTemp_ST.SetLayerObject(root.GetDown())

                    tag_mat_base = self.basesub.MakeTag(5616)
                    tag_mat_base[c4d.ID_BASELIST_NAME] = (op.GetName() + ' texture tag studio')
                    tag_mat_base[c4d.TEXTURETAG_MATERIAL] = self.MatTemp_ST

                    self.MatTemp_ST.Update(True, True)

                # если на оп нет материала и создан сам материал
                elif doc.SearchMaterial(op.GetName() + ' studio') != None:

                    self.mat_studio = doc.SearchMaterial(op.GetName() + ' studio')

                    tag_mat_base = self.basesub.MakeTag(5616)
                    tag_mat_base[c4d.ID_BASELIST_NAME] = (op.GetName() + ' texture tag studio')
                    tag_mat_base[c4d.TEXTURETAG_MATERIAL] = self.mat_studio

                    if op[st_ui.ST_RENDER_COLOR] == st_ui.ST_COLOR:
                        self.mat_studio[c4d.MATERIAL_USE_COLOR] = 1
                        self.mat_studio[c4d.MATERIAL_USE_REFLECTION] = 0
                        self.mat_studio[c4d.MATERIAL_COLOR_COLOR] = op[st_ui.ST_STUDIO_COLOR]
                        self.mat_studio.Update(True, True)

                    elif op[st_ui.ST_RENDER_COLOR] == st_ui.ST_REFLECTANCE:
                        self.mat_studio[c4d.MATERIAL_USE_COLOR] = 0
                        self.mat_studio[c4d.MATERIAL_USE_REFLECTION] = 1

                        mainid = 526336
                        self.mat_studio[mainid + c4d.REFLECTION_LAYER_COLOR_COLOR] = op[st_ui.ST_STUDIO_COLOR]
                        self.mat_studio.Update(True, True)
            #------------------------------------------------------------------------------------------- текстура на студии

        self.mat_studio = doc.SearchMaterial(op.GetName() + ' studio')

        # полигон из которого строится студия
        self.mypoly = c4d.BaseObject(c4d.Opolygon)
        self.mypoly.InsertUnder(self.basesub)

        xs = op[st_ui.ST_WIDTH]
        ys = op[st_ui.ST_HIDTH]
        zs = op[st_ui.ST_DEFTH]
        rd = op[st_ui.ST_ROUNDING]
        s = 10

        # студии
        if op[st_ui.ST_MODE] == st_ui.ST_C:

            # создание полигона
            self.mypoly.ResizeObject(40, 27)

            phong = self.mypoly.MakeTag(5612)
            phong[c4d.PHONGTAG_PHONG_ANGLELIMIT] = 1

            #------------------------------------------------------------------------ точки полигона
            #
            self.mypoly.SetPoint(0,c4d.Vector( -xs, 0, -zs))
            self.mypoly.SetPoint(1,c4d.Vector( -xs+s, 0, -zs))
            #
            self.mypoly.SetPoint(2,c4d.Vector( xs-s, 0, -zs))
            self.mypoly.SetPoint(3,c4d.Vector( xs, 0, -zs))

            #
            self.mypoly.SetPoint(4,c4d.Vector( -xs, 0, -zs+s))
            self.mypoly.SetPoint(5,c4d.Vector( -xs+s, 0, -zs+s))
            #
            self.mypoly.SetPoint(6,c4d.Vector( xs-s, 0, -zs+s))
            self.mypoly.SetPoint(7,c4d.Vector( xs, 0, -zs+s))

            #
            self.mypoly.SetPoint(8,c4d.Vector( -xs, 0, zs-rd))
            self.mypoly.SetPoint(9,c4d.Vector( -xs+s, 0, zs-rd))
            #
            self.mypoly.SetPoint(10,c4d.Vector( xs-s, 0, zs-rd))
            self.mypoly.SetPoint(11,c4d.Vector( xs, 0, zs-rd))

            #
            self.mypoly.SetPoint(12,c4d.Vector( -xs, 0, zs))
            self.mypoly.SetPoint(13,c4d.Vector( -xs+s, 0, zs))
            #
            self.mypoly.SetPoint(14,c4d.Vector( xs-s, 0, zs))
            self.mypoly.SetPoint(15,c4d.Vector( xs, 0, zs))

            #
            self.mypoly.SetPoint(16,c4d.Vector( -xs, rd, zs))
            self.mypoly.SetPoint(17,c4d.Vector( -xs+s, rd, zs))
            #
            self.mypoly.SetPoint(18,c4d.Vector( xs-s, rd, zs))
            self.mypoly.SetPoint(19,c4d.Vector( xs, rd, zs))
            
            #
            self.mypoly.SetPoint(20,c4d.Vector( -xs, ys-rd, zs))
            self.mypoly.SetPoint(21,c4d.Vector( -xs+s, ys-rd, zs))
            #
            self.mypoly.SetPoint(22,c4d.Vector( xs-s, ys-rd, zs))
            self.mypoly.SetPoint(23,c4d.Vector( xs, ys-rd, zs))

            #
            self.mypoly.SetPoint(24,c4d.Vector( -xs, ys, zs))
            self.mypoly.SetPoint(25,c4d.Vector( -xs+s, ys, zs))
            #
            self.mypoly.SetPoint(26,c4d.Vector( xs-s, ys, zs))
            self.mypoly.SetPoint(27,c4d.Vector( xs, ys, zs))

            #
            self.mypoly.SetPoint(28,c4d.Vector( -xs, ys, zs-rd))
            self.mypoly.SetPoint(29,c4d.Vector( -xs+s, ys, zs-rd))
            #
            self.mypoly.SetPoint(30,c4d.Vector( xs-s, ys, zs-rd))
            self.mypoly.SetPoint(31,c4d.Vector( xs, ys, zs-rd))

            #
            self.mypoly.SetPoint(32,c4d.Vector( -xs, ys, -zs+s))
            self.mypoly.SetPoint(33,c4d.Vector( -xs+s, ys, -zs+s))
            #
            self.mypoly.SetPoint(34,c4d.Vector( xs-s, ys, -zs+s))
            self.mypoly.SetPoint(35,c4d.Vector( xs, ys, -zs+s))

            #
            self.mypoly.SetPoint(36,c4d.Vector( -xs, ys, -zs))
            self.mypoly.SetPoint(37,c4d.Vector( -xs+s, ys,-zs))
            #
            self.mypoly.SetPoint(38,c4d.Vector( xs-s, ys, -zs))
            self.mypoly.SetPoint(39,c4d.Vector( xs, ys, -zs))
            #------------------------------------------------------------------------


            #------------------------------------------------------------------------ полигоны
            self.mypoly.SetPolygon(0, c4d.CPolygon(0, 1, 5, 4) )
            self.mypoly.SetPolygon(1, c4d.CPolygon(1, 2, 6, 5) )
            self.mypoly.SetPolygon(2, c4d.CPolygon(2, 3, 7, 6) )
            
            self.mypoly.SetPolygon(3, c4d.CPolygon(4, 5, 9, 8) )
            self.mypoly.SetPolygon(4, c4d.CPolygon(5, 6, 10, 9) )
            self.mypoly.SetPolygon(5, c4d.CPolygon(6, 7, 11, 10) )
            
            self.mypoly.SetPolygon(6, c4d.CPolygon(8, 9, 13, 12) )
            self.mypoly.SetPolygon(7, c4d.CPolygon(9, 10, 14, 13) )
            self.mypoly.SetPolygon(8, c4d.CPolygon(10, 11, 15, 14) )
            
            self.mypoly.SetPolygon(9, c4d.CPolygon(12, 13, 17, 16) )
            self.mypoly.SetPolygon(10, c4d.CPolygon(13, 14, 18, 17) )
            self.mypoly.SetPolygon(11, c4d.CPolygon(14, 15, 19, 18) )
            
            self.mypoly.SetPolygon(12, c4d.CPolygon(16, 17, 21, 20) )
            self.mypoly.SetPolygon(13, c4d.CPolygon(17, 18, 22, 21) )
            self.mypoly.SetPolygon(14, c4d.CPolygon(18, 19, 23, 22) )
            
            self.mypoly.SetPolygon(15, c4d.CPolygon(20, 21, 25, 24) )
            self.mypoly.SetPolygon(16, c4d.CPolygon(21, 22, 26, 25) )
            self.mypoly.SetPolygon(17, c4d.CPolygon(22, 23, 27, 26) )
            
            self.mypoly.SetPolygon(18, c4d.CPolygon(24, 25, 29, 28) )
            self.mypoly.SetPolygon(19, c4d.CPolygon(25, 26, 30, 29) )
            self.mypoly.SetPolygon(20, c4d.CPolygon(26, 27, 31, 30) )
            
            self.mypoly.SetPolygon(21, c4d.CPolygon(28, 29, 33, 32) )
            self.mypoly.SetPolygon(22, c4d.CPolygon(29, 30, 34, 33) )
            self.mypoly.SetPolygon(23, c4d.CPolygon(30, 31, 35, 34) )
            
            self.mypoly.SetPolygon(24, c4d.CPolygon(32, 33, 37, 36) )
            self.mypoly.SetPolygon(25, c4d.CPolygon(33, 34, 38, 37) )
            self.mypoly.SetPolygon(26, c4d.CPolygon(34, 35, 39, 38) )
            #------------------------------------------------------------------------

            self.mypoly.Message(c4d.MSG_UPDATE)

        elif op[st_ui.ST_MODE] == st_ui.ST_S:

            # создание полигона
            self.mypoly.ResizeObject(36,24)

            phong = self.mypoly.MakeTag(5612)
            phong[c4d.PHONGTAG_PHONG_ANGLELIMIT] = 1

            #------------------------------------------------------------------------ точки полигона
            #
            self.mypoly.SetPoint(0,c4d.Vector( -xs, -(ys * 0.3), -zs))
            self.mypoly.SetPoint(1,c4d.Vector( -xs+s, -(ys * 0.3), -zs))
            #
            self.mypoly.SetPoint(2,c4d.Vector( xs-s, -(ys * 0.3), -zs))
            self.mypoly.SetPoint(3,c4d.Vector( xs, -(ys * 0.3), -zs))
            
            #
            self.mypoly.SetPoint(4,c4d.Vector( -xs, -rd, -zs))
            self.mypoly.SetPoint(5,c4d.Vector( -xs+s, -rd, -zs))
            #
            self.mypoly.SetPoint(6,c4d.Vector( xs-s, -rd, -zs))
            self.mypoly.SetPoint(7,c4d.Vector( xs, -rd, -zs))

            #
            self.mypoly.SetPoint(8,c4d.Vector( -xs, 0, -zs))
            self.mypoly.SetPoint(9,c4d.Vector( -xs+s, 0, -zs))
            #
            self.mypoly.SetPoint(10,c4d.Vector( xs-s, 0, -zs))
            self.mypoly.SetPoint(11,c4d.Vector( xs, 0, -zs))

            #
            self.mypoly.SetPoint(12,c4d.Vector( -xs, 0, -zs+rd))
            self.mypoly.SetPoint(13,c4d.Vector( -xs+s, 0, -zs+rd))
            #
            self.mypoly.SetPoint(14,c4d.Vector( xs-s, 0, -zs+rd))
            self.mypoly.SetPoint(15,c4d.Vector( xs, 0, -zs+rd))

            #
            self.mypoly.SetPoint(16,c4d.Vector( -xs, 0, zs-rd))
            self.mypoly.SetPoint(17,c4d.Vector( -xs+s, 0, zs-rd))
            #
            self.mypoly.SetPoint(18,c4d.Vector( xs-s, 0, zs-rd))
            self.mypoly.SetPoint(19,c4d.Vector( xs, 0, zs-rd))

            #
            self.mypoly.SetPoint(20,c4d.Vector( -xs, 0, zs))
            self.mypoly.SetPoint(21,c4d.Vector( -xs+s, 0, zs))
            #
            self.mypoly.SetPoint(22,c4d.Vector( xs-s, 0, zs))
            self.mypoly.SetPoint(23,c4d.Vector( xs, 0, zs))

            #
            self.mypoly.SetPoint(24,c4d.Vector( -xs, rd, zs))
            self.mypoly.SetPoint(25,c4d.Vector( -xs+s, rd, zs))
            #
            self.mypoly.SetPoint(26,c4d.Vector( xs-s, rd, zs))
            self.mypoly.SetPoint(27,c4d.Vector( xs, rd, zs))

            #
            self.mypoly.SetPoint(28,c4d.Vector( -xs, ys-s, zs))
            self.mypoly.SetPoint(29,c4d.Vector( -xs+s, ys-s, zs))
            #
            self.mypoly.SetPoint(30,c4d.Vector( xs-s, ys-s, zs))
            self.mypoly.SetPoint(31,c4d.Vector( xs, ys-s, zs))

            #
            self.mypoly.SetPoint(32,c4d.Vector( -xs, ys, zs))
            self.mypoly.SetPoint(33,c4d.Vector( -xs+s, ys, zs))
            # 
            self.mypoly.SetPoint(34,c4d.Vector( xs-s, ys, zs))
            self.mypoly.SetPoint(35,c4d.Vector( xs, ys, zs))
            #----------------------------------------------------------------------------------------------------------

            #------------------------------------------------------------------------ полигоны
            self.mypoly.SetPolygon(0, c4d.CPolygon(0, 1, 5, 4) )
            self.mypoly.SetPolygon(1, c4d.CPolygon(1, 2, 6, 5) )
            self.mypoly.SetPolygon(2, c4d.CPolygon(2, 3, 7, 6) )
            
            self.mypoly.SetPolygon(3, c4d.CPolygon(4, 5, 9, 8) )
            self.mypoly.SetPolygon(4, c4d.CPolygon(5, 6, 10, 9) )
            self.mypoly.SetPolygon(5, c4d.CPolygon(6, 7, 11, 10) )
            
            self.mypoly.SetPolygon(6, c4d.CPolygon(8, 9, 13, 12) )
            self.mypoly.SetPolygon(7, c4d.CPolygon(9, 10, 14, 13) )
            self.mypoly.SetPolygon(8, c4d.CPolygon(10, 11, 15, 14) )
            
            self.mypoly.SetPolygon(9, c4d.CPolygon(12, 13, 17, 16) )
            self.mypoly.SetPolygon(10, c4d.CPolygon(13, 14, 18, 17) )
            self.mypoly.SetPolygon(11, c4d.CPolygon(14, 15, 19, 18) )
            
            self.mypoly.SetPolygon(12, c4d.CPolygon(16, 17, 21, 20) )
            self.mypoly.SetPolygon(13, c4d.CPolygon(17, 18, 22, 21) )
            self.mypoly.SetPolygon(14, c4d.CPolygon(18, 19, 23, 22) )
            
            self.mypoly.SetPolygon(15, c4d.CPolygon(20, 21, 25, 24) )
            self.mypoly.SetPolygon(16, c4d.CPolygon(21, 22, 26, 25) )
            self.mypoly.SetPolygon(17, c4d.CPolygon(22, 23, 27, 26) )
            
            self.mypoly.SetPolygon(18, c4d.CPolygon(24, 25, 29, 28) )
            self.mypoly.SetPolygon(19, c4d.CPolygon(25, 26, 30, 29) )
            self.mypoly.SetPolygon(20, c4d.CPolygon(26, 27, 31, 30) )
            
            self.mypoly.SetPolygon(21, c4d.CPolygon(28, 29, 33, 32) )
            self.mypoly.SetPolygon(22, c4d.CPolygon(29, 30, 34, 33) )
            self.mypoly.SetPolygon(23, c4d.CPolygon(30, 31, 35, 34) )
            #------------------------------------------------------------------------

            self.mypoly.Message(c4d.MSG_UPDATE)

        elif op[st_ui.ST_MODE] == st_ui.ST_U:

            # создание полигона
            self.mypoly.ResizeObject(40, 27)

            phong = self.mypoly.MakeTag(5612)
            phong[c4d.PHONGTAG_PHONG_ANGLELIMIT] = 1

            #------------------------------------------------------------------------ точки полигона
            #
            self.mypoly.SetPoint(0,c4d.Vector( -xs, 0, -zs))
            self.mypoly.SetPoint(1,c4d.Vector( -xs+rd, 0, -zs))
            #
            self.mypoly.SetPoint(2,c4d.Vector( xs-rd, 0, -zs))
            self.mypoly.SetPoint(3,c4d.Vector( xs, 0, -zs))

            #
            self.mypoly.SetPoint(4,c4d.Vector( -xs, 0, -zs+s))
            self.mypoly.SetPoint(5,c4d.Vector( -xs+rd, 0, -zs+s))
            #
            self.mypoly.SetPoint(6,c4d.Vector( xs-rd, 0, -zs+s))
            self.mypoly.SetPoint(7,c4d.Vector( xs, 0, -zs+s))

            #
            self.mypoly.SetPoint(8,c4d.Vector( -xs, 0, zs-s))
            self.mypoly.SetPoint(9,c4d.Vector( -xs+rd, 0, zs-s))
            #
            self.mypoly.SetPoint(10,c4d.Vector( xs-rd, 0, zs-s))
            self.mypoly.SetPoint(11,c4d.Vector( xs, 0, zs-s))

            #
            self.mypoly.SetPoint(12,c4d.Vector( -xs, 0, zs))
            self.mypoly.SetPoint(13,c4d.Vector( -xs+rd, 0, zs))
            #
            self.mypoly.SetPoint(14,c4d.Vector( xs-rd, 0, zs))
            self.mypoly.SetPoint(15,c4d.Vector( xs, 0, zs))

            #
            self.mypoly.SetPoint(16,c4d.Vector( xs, rd, -zs))
            self.mypoly.SetPoint(17,c4d.Vector( xs, rd, -zs+s))
            #
            self.mypoly.SetPoint(18,c4d.Vector( xs, rd, zs-s))
            self.mypoly.SetPoint(19,c4d.Vector( xs, rd, zs))
            
            #
            self.mypoly.SetPoint(20,c4d.Vector( xs, ys-s, -zs))
            self.mypoly.SetPoint(21,c4d.Vector( xs, ys-s, -zs+s))
            #
            self.mypoly.SetPoint(22,c4d.Vector( xs, ys-s, zs-s))
            self.mypoly.SetPoint(23,c4d.Vector( xs, ys-s, zs))
            
            #
            self.mypoly.SetPoint(24,c4d.Vector( xs, ys, -zs))
            self.mypoly.SetPoint(25,c4d.Vector( xs, ys, -zs+s))
            #
            self.mypoly.SetPoint(26,c4d.Vector( xs, ys, zs-s))
            self.mypoly.SetPoint(27,c4d.Vector( xs, ys, zs))

            #
            self.mypoly.SetPoint(28,c4d.Vector( -xs, rd, -zs))
            self.mypoly.SetPoint(29,c4d.Vector( -xs, rd, -zs+s))
            #
            self.mypoly.SetPoint(30,c4d.Vector( -xs, rd, zs-s))
            self.mypoly.SetPoint(31,c4d.Vector( -xs, rd, zs))
            
            #
            self.mypoly.SetPoint(32,c4d.Vector( -xs, ys-s, -zs))
            self.mypoly.SetPoint(33,c4d.Vector( -xs, ys-s, -zs+s))
            #
            self.mypoly.SetPoint(34,c4d.Vector( -xs, ys-s, zs-s))
            self.mypoly.SetPoint(35,c4d.Vector( -xs, ys-s, zs))
            
            #
            self.mypoly.SetPoint(36,c4d.Vector( -xs, ys, -zs))
            self.mypoly.SetPoint(37,c4d.Vector( -xs, ys, -zs+s))
            #
            self.mypoly.SetPoint(38,c4d.Vector( -xs, ys, zs-s))
            self.mypoly.SetPoint(39,c4d.Vector( -xs, ys, zs))
            #------------------------------------------------------------------------

            #------------------------------------------------------------------------ полигоны
            self.mypoly.SetPolygon(0, c4d.CPolygon(0, 1, 5, 4) )
            self.mypoly.SetPolygon(1, c4d.CPolygon(1, 2, 6, 5) )
            self.mypoly.SetPolygon(2, c4d.CPolygon(2, 3, 7, 6) )
            
            self.mypoly.SetPolygon(3, c4d.CPolygon(4, 5, 9, 8) )
            self.mypoly.SetPolygon(4, c4d.CPolygon(5, 6, 10, 9) )
            self.mypoly.SetPolygon(5, c4d.CPolygon(6, 7, 11, 10) )
            
            self.mypoly.SetPolygon(6, c4d.CPolygon(8, 9, 13, 12) )
            self.mypoly.SetPolygon(7, c4d.CPolygon(9, 10, 14, 13) )
            self.mypoly.SetPolygon(8, c4d.CPolygon(10, 11, 15, 14) )
            
            self.mypoly.SetPolygon(9, c4d.CPolygon(16, 17, 7, 3) )
            self.mypoly.SetPolygon(10, c4d.CPolygon(17, 18, 11, 7) )
            self.mypoly.SetPolygon(11, c4d.CPolygon(18, 19, 15, 11) )
            
            self.mypoly.SetPolygon(12, c4d.CPolygon(20, 21, 17, 16) )
            self.mypoly.SetPolygon(13, c4d.CPolygon(21, 22, 18, 17) )
            self.mypoly.SetPolygon(14, c4d.CPolygon(22, 23, 19, 18) )
            
            self.mypoly.SetPolygon(15, c4d.CPolygon(20, 21, 25, 24) )
            self.mypoly.SetPolygon(16, c4d.CPolygon(21, 22, 26, 25) )
            self.mypoly.SetPolygon(17, c4d.CPolygon(22, 23, 27, 26) )
            
            self.mypoly.SetPolygon(18, c4d.CPolygon(28, 29, 4, 0) )
            self.mypoly.SetPolygon(19, c4d.CPolygon(29, 30, 8, 4) )
            self.mypoly.SetPolygon(20, c4d.CPolygon(30, 31, 12, 8) )
            
            self.mypoly.SetPolygon(21, c4d.CPolygon(32, 33, 29, 28) )
            self.mypoly.SetPolygon(22, c4d.CPolygon(33, 34, 30, 29) )
            self.mypoly.SetPolygon(23, c4d.CPolygon(34, 35, 31, 30) )
            #------------------------------------------------------------------------

            self.mypoly.Message(c4d.MSG_UPDATE)

        elif op[st_ui.ST_MODE] == st_ui.ST_L:

            # создание полигона
            self.mypoly.ResizeObject(28, 18)

            phong = self.mypoly.MakeTag(5612)
            phong[c4d.PHONGTAG_PHONG_ANGLELIMIT] = 1

            #------------------------------------------------------------------------ точки полигона
            #
            self.mypoly.SetPoint(0,c4d.Vector( -xs, 0, -zs))
            self.mypoly.SetPoint(1,c4d.Vector( -xs+s, 0, -zs))
            #
            self.mypoly.SetPoint(2,c4d.Vector( xs-s, 0, -zs))
            self.mypoly.SetPoint(3,c4d.Vector( xs, 0, -zs))

            #
            self.mypoly.SetPoint(4,c4d.Vector( -xs, 0, -zs+s))
            self.mypoly.SetPoint(5,c4d.Vector( -xs+s, 0, -zs+s))
            #
            self.mypoly.SetPoint(6,c4d.Vector( xs-s, 0, -zs+s))
            self.mypoly.SetPoint(7,c4d.Vector( xs, 0, -zs+s))

            #
            self.mypoly.SetPoint(8,c4d.Vector( -xs, 0, zs-rd))
            self.mypoly.SetPoint(9,c4d.Vector( -xs+s, 0, zs-rd))
            #
            self.mypoly.SetPoint(10,c4d.Vector( xs-s, 0, zs-rd))
            self.mypoly.SetPoint(11,c4d.Vector( xs, 0, zs-rd))

            #
            self.mypoly.SetPoint(12,c4d.Vector( -xs, 0, zs))
            self.mypoly.SetPoint(13,c4d.Vector( -xs+s, 0, zs))
            #
            self.mypoly.SetPoint(14,c4d.Vector( xs-s, 0, zs))
            self.mypoly.SetPoint(15,c4d.Vector( xs, 0, zs))

            #
            self.mypoly.SetPoint(16,c4d.Vector( -xs, rd, zs))
            self.mypoly.SetPoint(17,c4d.Vector( -xs+s, rd, zs))
            #
            self.mypoly.SetPoint(18,c4d.Vector( xs-s, rd, zs))
            self.mypoly.SetPoint(19,c4d.Vector( xs, rd, zs))

            #
            self.mypoly.SetPoint(20,c4d.Vector( -xs, ys-s, zs))
            self.mypoly.SetPoint(21,c4d.Vector( -xs+s, ys-s, zs))
            #
            self.mypoly.SetPoint(22,c4d.Vector( xs-s, ys-s, zs))
            self.mypoly.SetPoint(23,c4d.Vector( xs, ys-s, zs))

            #
            self.mypoly.SetPoint(24,c4d.Vector( -xs, ys, zs))
            self.mypoly.SetPoint(25,c4d.Vector( -xs+s, ys, zs))
            #
            self.mypoly.SetPoint(26,c4d.Vector( xs-s, ys, zs))
            self.mypoly.SetPoint(27,c4d.Vector( xs, ys, zs))
            #------------------------------------------------------------------------------------------

            #------------------------------------------------------------------------ полигоны
            self.mypoly.SetPolygon(0, c4d.CPolygon(0, 1, 5, 4) )
            self.mypoly.SetPolygon(1, c4d.CPolygon(1, 2, 6, 5) )
            self.mypoly.SetPolygon(2, c4d.CPolygon(2, 3, 7, 6) )
            
            self.mypoly.SetPolygon(3, c4d.CPolygon(4, 5, 9, 8) )
            self.mypoly.SetPolygon(4, c4d.CPolygon(5, 6, 10, 9) )
            self.mypoly.SetPolygon(5, c4d.CPolygon(6, 7, 11, 10) )
            
            self.mypoly.SetPolygon(6, c4d.CPolygon(8, 9, 13, 12) )
            self.mypoly.SetPolygon(7, c4d.CPolygon(9, 10, 14, 13) )
            self.mypoly.SetPolygon(8, c4d.CPolygon(10, 11, 15, 14) )
            
            self.mypoly.SetPolygon(9, c4d.CPolygon(12, 13, 17, 16) )
            self.mypoly.SetPolygon(10, c4d.CPolygon(13, 14, 18, 17) )
            self.mypoly.SetPolygon(11, c4d.CPolygon(14, 15, 19, 18) )
            
            self.mypoly.SetPolygon(12, c4d.CPolygon(16, 17, 21, 20) )
            self.mypoly.SetPolygon(13, c4d.CPolygon(17, 18, 22, 21) )
            self.mypoly.SetPolygon(14, c4d.CPolygon(18, 19, 23, 22) )
            
            self.mypoly.SetPolygon(15, c4d.CPolygon(20, 21, 25, 24) )
            self.mypoly.SetPolygon(16, c4d.CPolygon(21, 22, 26, 25) )
            self.mypoly.SetPolygon(17, c4d.CPolygon(22, 23, 27, 26) )
            #------------------------------------------------------------------------

            self.mypoly.Message(c4d.MSG_UPDATE)
        #-------------------------------------------------------------------------------------------------


        return self.base
    #------------------------------------------------------------------------- КОНЕЦ Генерации объекта


    #----------------------------------------------------------------------- Кнопки и сценарии нажатия
    def Message(self, op, type, data):
        
        if type == c4d.MSG_DESCRIPTION_COMMAND:

            # Helper
            if data["id"][0].id ==  st_ui.ST_HELP:

                self.dialog = Helper()
                self.dialog.show(os.path.join(h.studio_URL), S.STR_BROWSERDIALOG_TITLE, 200, 100, 700, 700)

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
            op[st_ui.ST_RENDERER] = S.R_S

        elif rd[c4d.RDATA_RENDERENGINE] == S.Physical:
            op[st_ui.ST_RENDERER] = S.R_P

        elif rd[c4d.RDATA_RENDERENGINE] != S.Standard or rd[c4d.RDATA_RENDERENGINE] != S.Physical:
            op[st_ui.ST_RENDERER] = S.WARNING

        if rd[c4d.RDATA_RENDERENGINE] == S.Standard or rd[c4d.RDATA_RENDERENGINE] == S.Physical:
            
            if  op.GetTag(5616) != None:
                if ID == st_ui.ST_RENDER_COLOR:
                    return False

                if ID == st_ui.ST_STUDIO_COLOR:
                    return False

            else:
                if ID == st_ui.ST_RENDER_COLOR:
                    return True

                if ID == st_ui.ST_STUDIO_COLOR:
                    return True

        elif rd[c4d.RDATA_RENDERENGINE] != S.Standard and rd[c4d.RDATA_RENDERENGINE] != S.Physical:
            
            if ID == st_ui.ST_RENDER_COLOR:
                return False

            if ID == st_ui.ST_STUDIO_COLOR:
                return False
        #-------------------------------------------------------------------------------------------------

        return True
    #---------------------------------------------------------------------- КОНЕЦ  выкл/вкл интерфейса


#---------------------------------------------------------------------------------------- КОНЕЦ Studio


# инициализация компонентов
if __name__ == '__main__':

    dir, file = os.path.split(__file__)

    # Studio
    iconST = c4d.bitmaps.BaseBitmap()
    iconST.InitWith(os.path.join(dir, S.pathicons, S.studioIcon))
    plugins.RegisterObjectPlugin(id = st_ui.STUDIO, str = "Studio", g = Studio, description = "Studio", info = c4d.OBJECT_GENERATOR, icon = iconST )