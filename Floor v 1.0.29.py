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


from module.engine import if_ui
from module.engine import S
from module.engine import h
from module.engine import m
from module.engine.layer import *
from module.engine.helper import *




#-------------------------------------------------------------------------------------------- Floor
class Floor(c4d.plugins.ObjectData):


    dialog = None
    HANDLECOUNT = 4


    #-------------------------------------------------------------------------------- оптимизация кэша
    def __init__(self):

        self.SetOptimizeCache(True)
    #-------------------------------------------------------------------------------------------------


    #------------------------------------------------------------------- значение поумолчанию настроек
    def Init(self, op):

        # инициализация настроек интерфейса
        self.InitAttr(op, long, [if_ui.IF_MODE])
        self.InitAttr(op, c4d.Gradient, [if_ui.IF_GRADIENT])

        self.InitAttr(op, bool, [if_ui.IF_ONOFF])
        self.InitAttr(op, long, [if_ui.IF_REF_MODE])
        self.InitAttr(op, long, [if_ui.IF_FLOOR_MODE])
        self.InitAttr(op, float, [if_ui.IF_STRENGTH])
        self.InitAttr(op, float, [if_ui.IF_RUOGHNESS])
        self.InitAttr(op, float, [if_ui.IF_FRESNEL_STRENGTH])
        self.InitAttr(op, float, [if_ui.IF_IOR])
        self.InitAttr(op, float, [if_ui.IF_SAMPLING])

        self.InitAttr(op, bool, [if_ui.IF_DIM])
        self.InitAttr(op, float, [if_ui.IF_DIST])
        self.InitAttr(op, float, [if_ui.IF_FALLOFF])

        self.InitAttr(op, bool, [if_ui.IF_ONOFF_FLOOR])
        self.InitAttr(op, bool, [if_ui.IF_ONOFF_BG])
        self.InitAttr(op, float, [if_ui.IF_SIZE_F_STUDIO])

        self.grad = c4d.Gradient()
        self.grad.InsertKnot(col = c4d.Vector(0.95, 0.95, 0.95), brightness = 1.0, pos = 0.0, bias = 0.5, index = 0)
        self.grad.InsertKnot(col = c4d.Vector(0.75, 0.75, 0.75), brightness = 1.0, pos = 1.0, bias = 0.5, index = 1)
        self.grad.SetData(c4d.GRADIENT_INTERPOLATION, c4d.GRADIENT_INTERPOLATION_SMOOTHKNOT)

        # значения поумолчанию
        op[if_ui.IF_MODE] = if_ui.IF_CIRCULAR
        op[if_ui.IF_GRADIENT] = self.grad

        op[if_ui.IF_ONOFF] = False
        op[if_ui.IF_REF_MODE] = if_ui.IF_DIEL
        op[if_ui.IF_FLOOR_MODE] = if_ui.IF_F_INFINITE
        op[if_ui.IF_STRENGTH] = 1
        op[if_ui.IF_RUOGHNESS] = 0.0
        op[if_ui.IF_FRESNEL_STRENGTH] = 1.0
        op[if_ui.IF_IOR] = 1.537
        op[if_ui.IF_SAMPLING] = 8.0

        op[if_ui.IF_DIM] = False
        op[if_ui.IF_DIST] = 300.0
        op[if_ui.IF_FALLOFF] = 0.0

        op[if_ui.IF_ONOFF_FLOOR] = False
        op[if_ui.IF_ONOFF_BG] = False
        op[if_ui.IF_SIZE_F_STUDIO] = 500.0

        return True
    #-------------------------------------------------------------------------------------------------


    #------------------------------------------------------------------------------------------- Ручки
    def GetHandleCount(self, op):

        return self.HANDLECOUNT

    def GetHandle(self, op, i, info):

        wight = op[if_ui.IF_SIZE_F_STUDIO]
        if wight is None: wight = 500

        doc = op.GetDocument()
        rd = doc.GetActiveRenderData()

        #----------------------------------------------------------------------------------------------------- ручки

        if rd[c4d.RDATA_RENDERENGINE] == S.Standard or rd[c4d.RDATA_RENDERENGINE] == S.Physical:

            if op[if_ui.IF_FLOOR_MODE] == if_ui.IF_F_STUDIO:
                if i is 0:
                    info.position = c4d.Vector(wight, 0.0, 0.0)
                    info.direction = c4d.Vector(1.0, 0.0, 0.0)
                elif i is 1:
                    info.position = c4d.Vector(0.0, 0.0, wight)
                    info.direction = c4d.Vector(0.0, 0.0, 1.0)
                elif i is 2:
                    info.position = c4d.Vector(0.0, 0.0, -wight)
                    info.direction = c4d.Vector(0.0, 0.0, -1.0)
                elif i is 3:
                    info.position = c4d.Vector(-wight, 0.0, 0.0)
                    info.direction = c4d.Vector(-1.0, 0.0, 0.0)


    def SetHandle(self, op, i, p, info):

        data = op.GetDataInstance()
        if data is None: return

        tmp = c4d.HandleInfo()
        self.GetHandle(op, i, tmp)

        val = (p-tmp.position)*info.direction

        if op[if_ui.IF_FLOOR_MODE] == if_ui.IF_F_STUDIO:
            if i is 0:
                op[if_ui.IF_SIZE_F_STUDIO] = c4d.utils.FCut(op[if_ui.IF_SIZE_F_STUDIO]+val, 0.0, sys.maxint)
            elif i is 1:
                op[if_ui.IF_SIZE_F_STUDIO] = c4d.utils.FCut(op[if_ui.IF_SIZE_F_STUDIO]+val, 0.0, sys.maxint)
            elif i is 2:
                op[if_ui.IF_SIZE_F_STUDIO] = c4d.utils.FCut(op[if_ui.IF_SIZE_F_STUDIO]+val, 0.0, sys.maxint)
            elif i is 3:
                op[if_ui.IF_SIZE_F_STUDIO] = c4d.utils.FCut(op[if_ui.IF_SIZE_F_STUDIO]+val, 0.0, sys.maxint)

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
    #-------------------------------------------------------------------------------------------------


    #----------------------------------------------------------------------------------- Автоматизация
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
            #-------------------------------------------------------------------------------------------------

        return c4d.DRAWRESULT_OK
    #-------------------------------------------------------------------------------------------------


    #------------------------------------------------------------------------------- генерация объекта
    def GetVirtualObjects(self, op, hierarchyhelp):

        doc = op.GetDocument()
        rd = doc.GetActiveRenderData()

        if rd[c4d.RDATA_RENDERENGINE] == S.Standard or rd[c4d.RDATA_RENDERENGINE] == S.Physical:

            matlayer()

            #------------------------------------------------------------------------------------------------- базовый объект
            self.base = c4d.BaseObject(c4d.Onull)
            self.base.SetName(op.GetName())
            self.base[c4d.ID_BASEOBJECT_REL_SCALE] = c4d.Vector(1, 1, 1)

            root = doc.GetLayerObjectRoot()

            #------------------------------------------------------------------------------------------------- материалы
            if doc.SearchMaterial(op.GetName() + ' floor material') == None:
                # материал для пола
                self.matIn = c4d.documents.MergeDocument(doc, m.floorMat, c4d.SCENEFILTER_MATERIALS)
                self.MatTemp = doc.SearchMaterial('floor material')
                self.MatTemp.SetName(op.GetName() + ' floor material')
                doc.InsertMaterial(self.MatTemp)

                self.MatTemp.SetLayerObject(root.GetDown())

                c4d.EventAdd()
            #------------------------------------------------------------------------------------------------- конец материалы


            #------------------------------------------------------------------------------------------------- пол
            self.mat_floor = doc.SearchMaterial(op.GetName() + ' floor material')

            # материал для пола ------------------------------------------------------------------------
            # назначение градиента в канал цвета ---------------------------------------------------
            self.gtrad_mat = self.mat_floor[c4d.MATERIAL_COLOR_SHADER]
            self.gtrad_mat[c4d.SLA_GRADIENT_GRADIENT] = op[if_ui.IF_GRADIENT]

            if op[if_ui.IF_MODE] == if_ui.IF_CIRCULAR:
                self.gtrad_mat[c4d.SLA_GRADIENT_TYPE] = 2004
            elif op[if_ui.IF_MODE] == if_ui.IF_V:
                self.gtrad_mat[c4d.SLA_GRADIENT_TYPE] = 2001

            self.mat_floor[c4d.MATERIAL_USE_REFLECTION] = op[if_ui.IF_ONOFF]

            mainid = 526336

            if op[if_ui.IF_REF_MODE] == if_ui.IF_DIEL:
                self.mat_floor[mainid + c4d.REFLECTION_LAYER_FRESNEL_MODE] = 1

            elif op[if_ui.IF_REF_MODE] == if_ui.IF_COND:
                self.mat_floor[mainid + c4d.REFLECTION_LAYER_FRESNEL_MODE] = 2

            self.mat_floor[mainid + c4d.REFLECTION_LAYER_SAMPLING_DIM] = op[if_ui.IF_DIM]
            self.mat_floor[mainid + c4d.REFLECTION_LAYER_SAMPLING_DIM_DISTANCE] = op[if_ui.IF_DIST]
            self.mat_floor[mainid + c4d.REFLECTION_LAYER_SAMPLING_DIM_FALLOFF] = op[if_ui.IF_FALLOFF]
            self.mat_floor[mainid + c4d.REFLECTION_LAYER_SAMPLING_CLAMP] = op[if_ui.IF_SAMPLING]

            self.mat_floor[mainid + c4d.REFLECTION_LAYER_MAIN_VALUE_ROUGHNESS] = op[if_ui.IF_RUOGHNESS]
            self.mat_floor[mainid + c4d.REFLECTION_LAYER_MAIN_VALUE_REFLECTION] = op[if_ui.IF_STRENGTH]
            self.mat_floor[mainid + c4d.REFLECTION_LAYER_FRESNEL_VALUE_STRENGTH] = op[if_ui.IF_FRESNEL_STRENGTH]
            self.mat_floor[mainid + c4d.REFLECTION_LAYER_FRESNEL_VALUE_IOR] = op[if_ui.IF_IOR]
            self.mat_floor.Update(True, True)
            #-------------------------------------------------------------------------------------------------

            if op[if_ui.IF_FLOOR_MODE] == if_ui.IF_F_INFINITE:
                self.floor_preview = c4d.BaseObject(5168)
                self.floor_preview.SetName(op.GetName() + ' infinite floor preview')
                self.floor_preview.InsertUnder(self.base)
                self.floor_preview[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 1
                self.floor_preview[c4d.PRIM_PLANE_WIDTH] = 1000
                self.floor_preview[c4d.PRIM_PLANE_HEIGHT] = 1000
                self.floor_preview[c4d.PRIM_PLANE_SUBW] = 6
                self.floor_preview[c4d.PRIM_PLANE_SUBH] = 6

                # тэг текстуры preview ---------------------------------------------------------------------------
                self.tag_mat_floor_preview = self.floor_preview.MakeTag(5616)
                self.tag_mat_floor_preview[c4d.ID_BASELIST_NAME] = 'floor material tag'
                self.tag_mat_floor_preview[c4d.TEXTURETAG_MATERIAL] = self.mat_floor
                self.tag_mat_floor_preview[c4d.TEXTURETAG_PROJECTION] = 4

                self.tag_dis_floor_preview = self.floor_preview.MakeTag(5613)
                self.tag_dis_floor_preview[c4d.ID_BASELIST_NAME] = 'floor display tag'
                self.tag_dis_floor_preview[c4d.DISPLAYTAG_AFFECT_DISPLAYMODE] = 1
                self.tag_dis_floor_preview[c4d.DISPLAYTAG_SDISPLAYMODE] = 4

                # пол ---------------------------------------------------------------------------
                self.floor = c4d.BaseObject(5104)
                self.floor.SetName(op.GetName() + ' infinite floor')
                self.floor.InsertUnder(self.base)
                self.floor[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 1

                if op[if_ui.IF_ONOFF_FLOOR] == True:
                    self.floor_preview[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 1
                    self.floor[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 1

                elif op[if_ui.IF_ONOFF_FLOOR] == False:
                    self.floor_preview[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 0
                    self.floor[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 0

                # тэг текстуры ---------------------------------------------------------------------------
                self.tag_mat_floor = self.floor.MakeTag(5616)
                self.tag_mat_floor[c4d.ID_BASELIST_NAME] = 'floor material tag'
                self.tag_mat_floor[c4d.TEXTURETAG_MATERIAL] = self.mat_floor
                self.tag_mat_floor[c4d.TEXTURETAG_PROJECTION] = 4

                # тэг композиции -----------------------------------------------------------------------
                self.floor_comp_tag = self.floor.MakeTag(5637)
                self.floor_comp_tag[c4d.ID_BASELIST_NAME] = 'floor compositing tag'
                self.floor_comp_tag[c4d.COMPOSITINGTAG_BACKGROUND] = 1
                self.floor_comp_tag[c4d.COMPOSITINGTAG_BACKGROUND_GI] = 0
                self.floor_comp_tag[c4d.COMPOSITINGTAG_SEENBYGI] = 0
                self.floor_comp_tag[c4d.COMPOSITINGTAG_CASTSHADOW] = 0
                #-------------------------------------------------------------------------------------------------

            elif op[if_ui.IF_FLOOR_MODE] == if_ui.IF_F_STUDIO:
                self.floor = c4d.BaseObject(5164)
                self.floor.SetName(op.GetName() + ' circular floor')
                self.floor.InsertUnder(self.base)
                self.floor[c4d.PRIM_DISC_ORAD] = op[if_ui.IF_SIZE_F_STUDIO]
                self.floor[c4d.PRIM_DISC_CSUB] = 2

                if op[if_ui.IF_ONOFF_FLOOR] == True:
                    self.floor[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 1
                    self.floor[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 1

                elif op[if_ui.IF_ONOFF_FLOOR] == False:
                    self.floor[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 0
                    self.floor[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 0

                # тэг текстуры ---------------------------------------------------------------------------
                self.tag_mat_floor = self.floor.MakeTag(5616)
                self.tag_mat_floor[c4d.ID_BASELIST_NAME] = 'floor material tag'
                self.tag_mat_floor[c4d.TEXTURETAG_MATERIAL] = self.mat_floor
                self.tag_mat_floor[c4d.TEXTURETAG_PROJECTION] = 4

                self.tag_dis_floor_preview = self.floor.MakeTag(5613)
                self.tag_dis_floor_preview[c4d.ID_BASELIST_NAME] = 'floor display tag'
                self.tag_dis_floor_preview[c4d.DISPLAYTAG_AFFECT_DISPLAYMODE] = 1
                self.tag_dis_floor_preview[c4d.DISPLAYTAG_SDISPLAYMODE] = 4

                # тэг композиции -----------------------------------------------------------------------
                self.floor_comp_tag = self.floor.MakeTag(5637)
                self.floor_comp_tag[c4d.ID_BASELIST_NAME] = 'floor compositing tag'
                self.floor_comp_tag[c4d.COMPOSITINGTAG_BACKGROUND] = 1
                self.floor_comp_tag[c4d.COMPOSITINGTAG_BACKGROUND_GI] = 0
                self.floor_comp_tag[c4d.COMPOSITINGTAG_SEENBYGI] = 1
                self.floor_comp_tag[c4d.COMPOSITINGTAG_CASTSHADOW] = 0
                #-------------------------------------------------------------------------------------------------

            #------------------------------------------------------------------------------------------------- фон
            self.bg = c4d.BaseObject(5122)
            self.bg.SetName(op.GetName() + ' background')
            self.bg.InsertUnder(self.base)

            if op[if_ui.IF_ONOFF_BG] == True:
                self.bg[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 1
                self.bg[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 1

            elif op[if_ui.IF_ONOFF_BG] == False:
                self.bg[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 0
                self.bg[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 0

            self.tag_mat_bg = self.bg.MakeTag(5616)
            self.tag_mat_bg[c4d.ID_BASELIST_NAME] = (op.GetName() + ' plane material tag')
            self.tag_mat_bg[c4d.TEXTURETAG_MATERIAL] = self.mat_floor
            self.tag_mat_bg[c4d.TEXTURETAG_PROJECTION] = 4

            #------------------------------------------------------------------------------------------------- фон в окне просмотра
            self.bg_viewport = c4d.BaseObject(5105)
            self.bg_viewport.SetName(op.GetName() + ' background in viewport')
            self.bg_viewport.InsertUnder(self.base)
            self.bg_viewport[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 1

            self.tag_mat_bg_viewport = self.bg_viewport.MakeTag(5616)
            self.tag_mat_bg_viewport[c4d.ID_BASELIST_NAME] = (op.GetName() + ' plane material tag')
            self.tag_mat_bg_viewport[c4d.TEXTURETAG_MATERIAL] = self.mat_floor
            self.tag_mat_bg_viewport[c4d.TEXTURETAG_PROJECTION] = 4
            #-------------------------------------------------------------------------------------------------

        elif rd[c4d.RDATA_RENDERENGINE] != S.Standard or rd[c4d.RDATA_RENDERENGINE] != S.Physical:
            return None

        return self.base
    #-------------------------------------------------------------------------------------------------


    #----------------------------------------------------------------------- Кнопки и сценарии нажатия
    def Message(self, op, type, data):

        #--------------------------------------------------------------------------------------------- кнопки создания таргет объекта
        if type == c4d.MSG_DESCRIPTION_COMMAND:

            # Helper
            if data["id"][0].id == if_ui.IF_HELP:

                self.dialog = Helper()
                self.dialog.show(os.path.join(h.floor_URL), S.STR_BROWSERDIALOG_TITLE, 200, 100, 700, 700)
        #-----------------------------------------------------------------------------------------------------

        return True
    #-------------------------------------------------------------------------------------------------


    #----------------------------------------------------------------------------- выкл/вкл интерфейса
    def GetDEnabling(self, op, id, t_data, flags, itemdesc):

        data = op.GetDataInstance()
        if data is None: return
        ID = id[0].id

        doc = op.GetDocument()
        rd = doc.GetActiveRenderData()

        #------------------------------------------------------------------------------------------------- Тело и колеса
        if rd[c4d.RDATA_RENDERENGINE] == S.Standard:
            op[if_ui.IF_RENDERER] = S.R_S

        elif rd[c4d.RDATA_RENDERENGINE] == S.Physical:
            op[if_ui.IF_RENDERER] = S.R_P

        elif rd[c4d.RDATA_RENDERENGINE] != S.Standard or rd[c4d.RDATA_RENDERENGINE] != S.Physical:
            op[if_ui.IF_RENDERER] = S.WARNING

        if rd[c4d.RDATA_RENDERENGINE] == S.Standard or rd[c4d.RDATA_RENDERENGINE] == S.Physical:

            if op[if_ui.IF_FLOOR_MODE] == if_ui.IF_F_INFINITE:
                if ID == if_ui.IF_SIZE_F_STUDIO:
                    return False

            elif op[if_ui.IF_FLOOR_MODE] == if_ui.IF_F_STUDIO:
                if ID == if_ui.IF_SIZE_F_STUDIO:
                    return True

            if op[if_ui.IF_ONOFF] == False:
                if ID == if_ui.IF_REF_MODE:
                    return False

                if ID == if_ui.IF_STRENGTH:
                    return False

                if ID == if_ui.IF_RUOGHNESS:
                    return False

                if ID == if_ui.IF_IOR:
                    return False

                if ID == if_ui.IF_SAMPLING:
                    return False

                if ID == if_ui.IF_DIM:
                    return False

                if ID == if_ui.IF_FRESNEL_STRENGTH:
                    return False

            elif op[if_ui.IF_ONOFF] == True:
                if ID == if_ui.IF_REF_MODE:
                    return True

                if ID == if_ui.IF_STRENGTH:
                    return True

                if ID == if_ui.IF_RUOGHNESS:
                    return True

                if ID == if_ui.IF_IOR:
                    return True

                if ID == if_ui.IF_SAMPLING:
                    return True

                if ID == if_ui.IF_DIM:
                    return True

                if ID == if_ui.IF_FRESNEL_STRENGTH:
                    return True

            if op[if_ui.IF_DIM] == False:
                if ID == if_ui.IF_DIST:
                    return False

                if ID == if_ui.IF_FALLOFF:
                    return False

            elif op[if_ui.IF_DIM] == True:
                if ID == if_ui.IF_DIST:
                    return True

                if ID == if_ui.IF_FALLOFF:
                    return True

        elif rd[c4d.RDATA_RENDERENGINE] != S.Standard or rd[c4d.RDATA_RENDERENGINE] != S.Physical:

            if ID == if_ui.IF_FLOOR_MODE:
                return False

            if ID == if_ui.IF_SIZE_F_STUDIO:
                return False

            if ID == if_ui.IF_MODE:
                return False

            if ID == if_ui.IF_GRADIENT:
                return False

            if ID == if_ui.IF_ONOFF:
                return False

            if ID == if_ui.IF_REF_MODE:
                return False

            if ID == if_ui.IF_STRENGTH:
                return False

            if ID == if_ui.IF_RUOGHNESS:
                return False

            if ID == if_ui.IF_FRESNEL_STRENGTH:
                return False

            if ID == if_ui.IF_IOR:
                return False

            if ID == if_ui.IF_SAMPLING:
                return False

            if ID == if_ui.IF_DIM:
                return False

            if ID == if_ui.IF_DIST:
                return False

            if ID == if_ui.IF_FALLOFF:
                return False

            if ID == if_ui.IF_ONOFF_FLOOR:
                return False

            if ID == if_ui.IF_ONOFF_BG:
                return False


        return True
    #-------------------------------------------------------------------------------------------------


#-------------------------------------------------------------------------------------------- end Floor


# инициализация компонентов
if __name__ == '__main__':

    dir, file = os.path.split(__file__)

    # Floor
    iconIF = c4d.bitmaps.BaseBitmap()
    iconIF.InitWith(os.path.join(dir, S.pathicons, S.infinitIcon))
    plugins.RegisterObjectPlugin(id = if_ui.INFINIT, str = "Floor", g = Floor, description = "Floor", info = c4d.OBJECT_GENERATOR, icon = iconIF )