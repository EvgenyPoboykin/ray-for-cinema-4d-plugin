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
from module.engine import bc_ui
from module.engine import d_ui
from module.engine import sb_ui
from module.engine import gl_ui
from module.engine import oh_ui
from module.engine import h
from module.engine import m
from module.engine.layer import *
from module.engine.helper import *




#------------------------------------------------------------------------------------------ BounceCard
class BounceCard(c4d.plugins.ObjectData):


    dialog = None
    HANDLECOUNT = 8


    #-------------------------------------------------------------------------------- Оптимизация кэша
    def __init__(self):

        self.SetOptimizeCache(True)
    #-------------------------------------------------------------------------------------------------


    #------------------------------------------------------------------- Значение поумолчанию настроек
    def Init(self, op):

        # инициализация настроек интерфейса
        self.InitAttr(op, float, [bc_ui.BC_WIDTH])
        self.InitAttr(op, float, [bc_ui.BC_HIDTH])
        self.InitAttr(op, float, [bc_ui.BC_RADIUS])

        self.InitAttr(op, c4d.Vector, [bc_ui.BC_LIGHT_COLOR])
        self.InitAttr(op, float, [bc_ui.BC_POWER])

        self.InitAttr(op, bool, [bc_ui.BC_SB_CAMERA])
        self.InitAttr(op, bool, [bc_ui.BC_SB_TRANSPARENCY])
        self.InitAttr(op, bool, [bc_ui.BC_V_EDITOR])
        self.InitAttr(op, bool, [bc_ui.BC_LIGHT_RAY])
        self.InitAttr(op, bool, [bc_ui.BC_LIGHT_GI])
        self.InitAttr(op, bool, [bc_ui.BC_USED])
        self.InitAttr(op, bool, [bc_ui.BC_INVERT_COLOR])

        # значения поумолчанию

        op[bc_ui.BC_WIDTH] = 200
        op[bc_ui.BC_HIDTH] = 100
        op[bc_ui.BC_RADIUS] = 0.0

        op[bc_ui.BC_LIGHT_COLOR] = c4d.Vector(0.97, 0.97, 0.97)
        op[bc_ui.BC_POWER] = 1.0

        op[bc_ui.BC_SB_CAMERA] = False
        op[bc_ui.BC_USED] = False
        op[bc_ui.BC_INVERT_COLOR] = False
        op[bc_ui.BC_SB_TRANSPARENCY] = True
        op[bc_ui.BC_V_EDITOR] = True
        op[bc_ui.BC_LIGHT_RAY] = True
        op[bc_ui.BC_LIGHT_GI] = True

        return True
    #-------------------------------------------------------------------------------------------------


    #------------------------------------------------------------------------------------------- Ручки
    def GetHandleCount(self, op):

        return self.HANDLECOUNT

    def GetHandle(self, op, i, info):

        wight = op[bc_ui.BC_WIDTH]
        if wight is None: wight = 200

        hight = op[bc_ui.BC_HIDTH]
        if hight is None: hight = 100

        rad = op[bc_ui.BC_RADIUS]
        if rad is None: rad = 0

        doc = op.GetDocument()
        rd = doc.GetActiveRenderData()

        if rd[c4d.RDATA_RENDERENGINE] == S.Standard or rd[c4d.RDATA_RENDERENGINE] == S.Physical:

            #----------------------------------------------------------------------------------------------------- ручки
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
                info.position = c4d.Vector(wight/2 - rad, hight/2 - rad, 0.0)
                info.direction = c4d.Vector(0.0, -1.0, 0.0)
            elif i is 5:
                info.position = c4d.Vector(-(wight/2 - rad), hight/2 - rad, 0.0)
                info.direction = c4d.Vector(0.0, -1.0, 0.0)
            elif i is 6:
                info.position = c4d.Vector(-(wight/2 - rad), -(hight/2 - rad), 0.0)
                info.direction = c4d.Vector(0.0, 1.0, 0.0)
            elif i is 7:
                info.position = c4d.Vector(wight/2 - rad, -(hight/2 - rad), 0.0)
                info.direction = c4d.Vector(0.0, 1.0, 0.0)

    def SetHandle(self, op, i, p, info):

        data = op.GetDataInstance()
        if data is None: return

        tmp = c4d.HandleInfo()
        self.GetHandle(op, i, tmp)

        val = (p-tmp.position)*info.direction

        if op[bc_ui.BC_WIDTH] >= op[bc_ui.BC_HIDTH]:
            if i is 0:
                op[bc_ui.BC_WIDTH] = c4d.utils.FCut(op[bc_ui.BC_WIDTH]+val, op[bc_ui.BC_RADIUS]*2, sys.maxint)
            elif i is 1:
                op[bc_ui.BC_HIDTH] = c4d.utils.FCut(op[bc_ui.BC_HIDTH]+val, op[bc_ui.BC_RADIUS]*2, sys.maxint)
            elif i is 2:
                op[bc_ui.BC_HIDTH] = c4d.utils.FCut(op[bc_ui.BC_HIDTH]+val, op[bc_ui.BC_RADIUS]*2, sys.maxint)
            elif i is 3:
                op[bc_ui.BC_WIDTH] = c4d.utils.FCut(op[bc_ui.BC_WIDTH]+val, op[bc_ui.BC_RADIUS]*2, sys.maxint)
            elif i is 4 or i is 5 or i is 6 or i is 7:
                op[bc_ui.BC_RADIUS] = c4d.utils.FCut(op[bc_ui.BC_RADIUS]+val, 0.0, op[bc_ui.BC_HIDTH]/2)

        elif op[bc_ui.BC_WIDTH] <= op[bc_ui.BC_HIDTH]:
            if i is 0:
                op[bc_ui.BC_WIDTH] = c4d.utils.FCut(op[bc_ui.BC_WIDTH]+val, op[bc_ui.BC_RADIUS]*2, sys.maxint)
            elif i is 1:
                op[bc_ui.BC_HIDTH] = c4d.utils.FCut(op[bc_ui.BC_HIDTH]+val, op[bc_ui.BC_RADIUS]*2, sys.maxint)
            elif i is 2:
                op[bc_ui.BC_HIDTH] = c4d.utils.FCut(op[bc_ui.BC_HIDTH]+val, op[bc_ui.BC_RADIUS]*2, sys.maxint)
            elif i is 3:
                op[bc_ui.BC_WIDTH] = c4d.utils.FCut(op[bc_ui.BC_WIDTH]+val, op[bc_ui.BC_RADIUS]*2, sys.maxint)
            elif i is 4 or i is 5 or i is 6 or i is 7:
                op[bc_ui.BC_RADIUS] = c4d.utils.FCut(op[bc_ui.BC_RADIUS]+val, 0.0, op[bc_ui.BC_WIDTH]/2)

        elif op[bc_ui.BC_WIDTH] == op[bc_ui.BC_HIDTH]:
            if i is 0:
                op[bc_ui.BC_WIDTH] = c4d.utils.FCut(op[bc_ui.BC_WIDTH]+val, op[bc_ui.BC_RADIUS]*2, sys.maxint)
            elif i is 1:
                op[bc_ui.BC_HIDTH] = c4d.utils.FCut(op[bc_ui.BC_HIDTH]+val, op[bc_ui.BC_RADIUS]*2, sys.maxint)
            elif i is 2:
                op[bc_ui.BC_HIDTH] = c4d.utils.FCut(op[bc_ui.BC_HIDTH]+val, op[bc_ui.BC_RADIUS]*2, sys.maxint)
            elif i is 3:
                op[bc_ui.BC_WIDTH] = c4d.utils.FCut(op[bc_ui.BC_WIDTH]+val, op[bc_ui.BC_RADIUS]*2, sys.maxint)
            elif i is 4 or i is 5 or i is 6 or i is 7:
                op[bc_ui.BC_RADIUS] = c4d.utils.FCut(op[bc_ui.BC_RADIUS]+val, 0.0, op[bc_ui.BC_WIDTH]/2)

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

                info = c4d.HandleInfo()
                self.GetHandle(op, i, info)
                bd.DrawHandle(info.position, c4d.DRAWHANDLE_MIDDLE, 0)

                bd.SetPen(c4d.GetViewColor(c4d.VIEWCOLOR_ACTIVEPOINT))
            #-----------------------------------------------------------------------------------------------------

        elif rd[c4d.RDATA_RENDERENGINE] != S.Standard or rd[c4d.RDATA_RENDERENGINE] != S.Physical:

            if drawpass!=c4d.DRAWPASS_OBJECT: return c4d.DRAWRESULT_SKIP

        return c4d.DRAWRESULT_OK
    #-------------------------------------------------------------------------------- КОНЕЦ Прорисовки


    #------------------------------------------------------------------------------- Генерация объекта
    def GetVirtualObjects(self, op, hierarchyhelp):

        doc = op.GetDocument()
        rd = doc.GetActiveRenderData()



        # если стандартный или физический рендер тогда создать объект
        if rd[c4d.RDATA_RENDERENGINE] == S.Standard or rd[c4d.RDATA_RENDERENGINE] == S.Physical:

            matlayer()

            #------------------------------------------------------------------------------------------------- базовый объект
            self.base = c4d.BaseObject(c4d.Onull)
            self.base.SetName(op.GetName())
            self.base[c4d.ID_BASEOBJECT_REL_SCALE] = c4d.Vector(1, 1, 1)

            #------------------------------------------------------------------------------------------- выключение в эдиторе
            if op[bc_ui.BC_V_EDITOR] == True:
                self.base[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 0

            elif op[bc_ui.BC_V_EDITOR] == False:
                self.base[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 1

            if op.GetTag(5676) != None:
                self.TargetTag = self.base.MakeTag(5676)
                self.TargetTag.SetName(self.base.GetName() + ' target')

                sourse = op.GetTag(5676)

                self.TargetTag[c4d.TARGETEXPRESSIONTAG_LINK] = sourse[c4d.TARGETEXPRESSIONTAG_LINK]
            #---------------------------------------------------------------------------------------------------------------

            root = doc.GetLayerObjectRoot()

            #----------------------------------------------------------------------------------------------------- материалы
            if doc.SearchMaterial(op.GetName() + ' plane material') == None:
                # материал для рефлектора
                self.matIn = c4d.documents.MergeDocument(doc, m.cardMat, c4d.SCENEFILTER_MATERIALS)
                self.MatTemp = doc.SearchMaterial('plane material')
                self.MatTemp.SetName(op.GetName() + ' plane material')

                self.MatTemp.SetLayerObject(root.GetDown())
            #-----------------------------------------------------------------------------------------------------


            #----------------------------------------------------------------------------------------------------- рефлектор с материалом
            self.material = doc.SearchMaterial(op.GetName() + ' plane material')

            self.reflection = c4d.BaseObject(5107)
            self.reflection.SetName(op.GetName() + ' card itself')
            self.reflection.InsertUnder(self.base)
            self.reflection[c4d.LOFTOBJECT_ADAPTIVEY] = 0
            self.reflection[c4d.CAP_START] = 1
            self.reflection[c4d.CAP_END] = 0

            self.tag_comp = self.reflection.MakeTag(5637)
            self.tag_comp[c4d.ID_BASELIST_NAME] = (op.GetName() + ' compositing')
            self.tag_comp[c4d.COMPOSITINGTAG_CASTSHADOW] = 0
            self.tag_comp[c4d.COMPOSITINGTAG_RECEIVESHADOW] = 0
            self.tag_comp[c4d.COMPOSITINGTAG_SEENBYTRANSPARENCY] = op[bc_ui.BC_SB_TRANSPARENCY]
            self.tag_comp[c4d.COMPOSITINGTAG_SEENBYAO] = 0
            self.tag_comp[c4d.COMPOSITINGTAG_SEENBYCAMERA] = op[bc_ui.BC_SB_CAMERA]
            self.tag_comp[c4d.COMPOSITINGTAG_SEENBYRAYS] = op[bc_ui.BC_LIGHT_RAY]
            self.tag_comp[c4d.COMPOSITINGTAG_SEENBYGI] = op[bc_ui.BC_LIGHT_GI]

            self.tag_mat_soft = self.reflection.MakeTag(5616)
            self.tag_mat_soft[c4d.ID_BASELIST_NAME] = (op.GetName() + ' reflection plane tag')
            self.tag_mat_soft[c4d.TEXTURETAG_MATERIAL] = self.material
            self.material[c4d.MATERIAL_LUMINANCE_COLOR] = op[bc_ui.BC_LIGHT_COLOR]
            self.material[c4d.MATERIAL_LUMINANCE_BRIGHTNESS] = op[bc_ui.BC_POWER]
            self.material[c4d.MATERIAL_GLOBALILLUM_GENERATE_STRENGTH] = 1.0
            #-----------------------------------------------------------------------------------------------------


            #----------------------------------------------------------------------------------------------------- Профиль рефлектора
            self.softbox_start = c4d.BaseObject(5186)
            self.softbox_start.SetName(op.GetName() + ' start')
            self.softbox_start.InsertUnder(self.reflection)
            self.softbox_start[c4d.PRIM_PLANE] = 0
            self.softbox_start[c4d.PRIM_RECTANGLE_ROUNDING] = 1
            self.softbox_start[c4d.PRIM_RECTANGLE_WIDTH] = op[bc_ui.BC_WIDTH]
            self.softbox_start[c4d.PRIM_RECTANGLE_HEIGHT] = op[bc_ui.BC_HIDTH]
            self.softbox_start[c4d.PRIM_RECTANGLE_RADIUS] = op[bc_ui.BC_RADIUS]
            #-------------------------------------------------------------------------------------------------

        elif rd[c4d.RDATA_RENDERENGINE] != S.Standard or rd[c4d.RDATA_RENDERENGINE] != S.Physical:
            return None

        return self.base
    #------------------------------------------------------------------------- КОНЕЦ Генерации объекта


    #----------------------------------------------------------------------- Кнопки и сценарии нажатия
    def Message(self, op, type, data):

        #--------------------------------------------------------------------------------------------- кнопки создания таргет объекта
        if type == c4d.MSG_DESCRIPTION_COMMAND:

            # Helper
            if data["id"][0].id == bc_ui.BC_HELP:

                self.dialog = Helper()
                self.dialog.show(os.path.join(h.bounce_URL), S.STR_BROWSERDIALOG_TITLE, 200, 100, 700, 700)

            # Add target object
            if data["id"][0].id == bc_ui.BC_ADD_TARGET_TAG:

                if op.GetTag(5676) == None:

                    self.TargetTag = op.MakeTag(5676)
                    self.TargetTag.SetName(op.GetName() + ' target')
                    self.TargetTag.ChangeNBit(c4d.NBIT_OHIDE, c4d.NBITCONTROL_SET)

                elif op.GetTag(5676) != None:

                    self.TargetTag = op.GetTag(5676)
                    self.TargetTag.Remove()
        #-----------------------------------------------------------------------------------------------------

        #-------------------------------------------------------------------------------------------------
        # ведущий свет
        if op[bc_ui.BC_USED] == True:

            if op[bc_ui.BC_LINK] != None and op[bc_ui.BC_INVERT_COLOR] == True:

                if op[bc_ui.BC_LINK].GetType() == sb_ui.SBOX:
                    instLight = op[bc_ui.BC_LINK]

                    CV = c4d.utils.RGBToHSV(instLight[sb_ui.SB_LIGHT_COLOR])

                    if CV[0] <= 0.5:
                        CR = c4d.Vector(CV[0] + 0.5 , CV[1], CV[2])
                        op[bc_ui.BC_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] >= 0.5:
                        CR = c4d.Vector(CV[0] - 0.5 , CV[1], CV[2])
                        op[bc_ui.BC_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] == 0.5:
                        CR = c4d.Vector(0, CV[1], CV[2])
                        op[bc_ui.BC_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)

                elif op[bc_ui.BC_LINK].GetType() == bc_ui.BOUNCE:
                    instLight = op[bc_ui.BC_LINK]

                    CV = c4d.utils.RGBToHSV(instLight[bc_ui.BC_LIGHT_COLOR])

                    if CV[0] <= 0.5:
                        CR = c4d.Vector(CV[0] + 0.5 , CV[1], CV[2])
                        op[bc_ui.BC_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] >= 0.5:
                        CR = c4d.Vector(CV[0] - 0.5 , CV[1], CV[2])
                        op[bc_ui.BC_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] == 0.5:
                        CR = c4d.Vector(0, CV[1], CV[2])
                        op[bc_ui.BC_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)

                elif op[bc_ui.BC_LINK].GetType() == oh_ui.OVERHEAD:
                    instLight = op[bc_ui.BC_LINK]

                    CV = c4d.utils.RGBToHSV(instLight[oh_ui.OH_LIGHT_COLOR])

                    if CV[0] <= 0.5:
                        CR = c4d.Vector(CV[0] + 0.5 , CV[1], CV[2])
                        op[bc_ui.BC_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] >= 0.5:
                        CR = c4d.Vector(CV[0] - 0.5 , CV[1], CV[2])
                        op[bc_ui.BC_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] == 0.5:
                        CR = c4d.Vector(0, CV[1], CV[2])
                        op[bc_ui.BC_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)

                elif op[bc_ui.BC_LINK].GetType() == d_ui.DAYLIGHT:
                    instLight = op[bc_ui.BC_LINK]

                    CV = c4d.utils.RGBToHSV(instLight[d_ui.DL_LIGHT_COLOR])

                    if CV[0] <= 0.5:
                        CR = c4d.Vector(CV[0] + 0.5 , CV[1], CV[2])
                        op[bc_ui.BC_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] >= 0.5:
                        CR = c4d.Vector(CV[0] - 0.5 , CV[1], CV[2])
                        op[bc_ui.BC_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] == 0.5:
                        CR = c4d.Vector(0, CV[1], CV[2])
                        op[bc_ui.BC_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)

                elif op[bc_ui.BC_LINK].GetType() == 5102:
                    instLight = op[bc_ui.BC_LINK]

                    CV = c4d.utils.RGBToHSV(instLight[c4d.LIGHT_COLOR])

                    if CV[0] <= 0.5:
                        CR = c4d.Vector(CV[0] + 0.5 , CV[1], CV[2])
                        op[bc_ui.BC_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] >= 0.5:
                        CR = c4d.Vector(CV[0] - 0.5 , CV[1], CV[2])
                        op[bc_ui.BC_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] == 0.5:
                        CR = c4d.Vector(0, CV[1], CV[2])
                        op[bc_ui.BC_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)

                elif op[bc_ui.BC_LINK].GetType() == gl_ui.GLOBALLIGHT:
                    instLight = op[bc_ui.BC_LINK]

                    CV = c4d.utils.RGBToHSV(instLight[gl_ui.GL_LIGHT_COLOR])

                    if CV[0] <= 0.5:
                        CR = c4d.Vector(CV[0] + 0.5 , CV[1], CV[2])
                        op[bc_ui.BC_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] >= 0.5:
                        CR = c4d.Vector(CV[0] - 0.5 , CV[1], CV[2])
                        op[bc_ui.BC_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)
                    elif CV[0] == 0.5:
                        CR = c4d.Vector(0, CV[1], CV[2])
                        op[bc_ui.BC_LIGHT_COLOR] = c4d.utils.HSVToRGB(CR)

            elif op[bc_ui.BC_LINK] != None and op[bc_ui.BC_INVERT_COLOR] == False:

                if op[bc_ui.BC_LINK].GetType() == sb_ui.SBOX:
                    instLight = op[bc_ui.BC_LINK]

                    op[bc_ui.BC_LIGHT_COLOR] = instLight[sb_ui.SB_LIGHT_COLOR]

                elif op[bc_ui.BC_LINK].GetType() == bc_ui.BOUNCE:
                    instLight = op[bc_ui.BC_LINK]

                    op[bc_ui.BC_LIGHT_COLOR] = instLight[bc_ui.BC_LIGHT_COLOR]

                elif op[bc_ui.BC_LINK].GetType() == oh_ui.OVERHEAD:
                    instLight = op[bc_ui.BC_LINK]

                    op[bc_ui.BC_LIGHT_COLOR] = instLight[oh_ui.OH_LIGHT_COLOR]

                elif op[bc_ui.BC_LINK].GetType() == d_ui.DAYLIGHT:
                    instLight = op[bc_ui.BC_LINK]

                    op[bc_ui.BC_LIGHT_COLOR] = instLight[d_ui.DL_LIGHT_COLOR]

                elif op[bc_ui.BC_LINK].GetType() == gl_ui.GLOBALLIGHT:
                    instLight = op[bc_ui.BC_LINK]

                    op[bc_ui.BC_LIGHT_COLOR] = instLight[gl_ui.GL_LIGHT_COLOR]
                
                elif op[bc_ui.BC_LINK].GetType() == 5102:
                    instLight = op[bc_ui.BC_LINK]

                    op[bc_ui.BC_LIGHT_COLOR] = instLight[c4d.LIGHT_COLOR]

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
            op[bc_ui.BC_RENDERER] = S.R_S

        elif rd[c4d.RDATA_RENDERENGINE] == S.Physical:
            op[bc_ui.BC_RENDERER] = S.R_P

        elif rd[c4d.RDATA_RENDERENGINE] != S.Standard or rd[c4d.RDATA_RENDERENGINE] != S.Physical:
            op[bc_ui.BC_RENDERER] = S.WARNING

        if rd[c4d.RDATA_RENDERENGINE] == S.Standard or rd[c4d.RDATA_RENDERENGINE] == S.Physical:

            if op[bc_ui.BC_USED] == True:
                if ID == bc_ui.BC_LIGHT_COLOR:
                    return False

                if ID == bc_ui.BC_LINK:
                    return True

                if ID == bc_ui.BC_INVERT_COLOR:
                    return True

            elif op[bc_ui.BC_USED] == False:
                if ID == bc_ui.BC_LIGHT_COLOR:
                    return True

                if ID == bc_ui.BC_LINK:
                    return False

                if ID == bc_ui.BC_INVERT_COLOR:
                    return False

            if ID == bc_ui.BC_ADD_TARGET_TAG:
                return True

            if ID == bc_ui.BC_WIDTH:
                return True

            if ID == bc_ui.BC_HIDTH:
                return True

            if ID == bc_ui.BC_RADIUS:
                return True

            if ID == bc_ui.BC_LIGHT_COLOR:
                return True

            if ID == bc_ui.BC_POWER:
                return True

            if ID == bc_ui.BC_SB_CAMERA:
                return True

            if ID == bc_ui.BC_SB_TRANSPARENCY:
                return True

            if ID == bc_ui.BC_V_EDITOR:
                return True

            if ID == bc_ui.BC_LIGHT_RAY:
                return True

            if ID == bc_ui.BC_LIGHT_GI:
                return True

        elif rd[c4d.RDATA_RENDERENGINE] != S.Standard or rd[c4d.RDATA_RENDERENGINE] != S.Physical:
            
            if ID == bc_ui.BC_ADD_TARGET_TAG:
                return False

            if ID == bc_ui.BC_WIDTH:
                return False

            if ID == bc_ui.BC_HIDTH:
                return False

            if ID == bc_ui.BC_RADIUS:
                return False

            if ID == bc_ui.BC_LIGHT_COLOR:
                return False

            if ID == bc_ui.BC_POWER:
                return False

            if ID == bc_ui.BC_SB_CAMERA:
                return False

            if ID == bc_ui.BC_SB_TRANSPARENCY:
                return False

            if ID == bc_ui.BC_V_EDITOR:
                return False

            if ID == bc_ui.BC_LIGHT_RAY:
                return False

            if ID == bc_ui.BC_LIGHT_GI:
                return False

            if ID == bc_ui.BC_USED:
                    return False

            if ID == bc_ui.BC_LINK:
                return False

            if ID == bc_ui.BC_INVERT_COLOR:
                return False

        #-------------------------------------------------------------------------------------------------

        return True
    #---------------------------------------------------------------------- КОНЕЦ  выкл/вкл интерфейса


#------------------------------------------------------------------------------------ КОНЕЦ BounceCard


# инициализация компонентов
if __name__ == '__main__':

    dir, file = os.path.split(__file__)

    # BounceCard
    iconBC = c4d.bitmaps.BaseBitmap()
    iconBC.InitWith(os.path.join(dir, S.pathicons, S.bounceIcon))
    plugins.RegisterObjectPlugin(id = bc_ui.BOUNCE, str = "BounceCard", g = BounceCard, description = "BounceCard", info = c4d.OBJECT_GENERATOR, icon = iconBC)
