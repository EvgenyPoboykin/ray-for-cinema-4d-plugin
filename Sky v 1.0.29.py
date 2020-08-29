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


from module.engine import s_ui
from module.engine import d_ui
from module.engine import S
from module.engine import h
from module.engine import m
from module.engine.layer import *
from module.engine.helper import *




#-------------------------------------------------------------------------------------------- Sky
class Sky(c4d.plugins.ObjectData):


    dialog = None


    #--------------------------------------------------------------------------- оптимизация кэша
    def __init__(self):

        self.SetOptimizeCache(True)
    #--------------------------------------------------------------------------------------------


    #-------------------------------------------------------------- значение поумолчанию настроек
    def Init(self, op):

        # инициализация настроек интерфейса
        self.InitAttr(op, str, [s_ui.S_FILE])
        self.InitAttr(op, bool, [s_ui.S_SHOW_PREVIEW])
        self.InitAttr(op, bool, [s_ui.S_COLORIZE])
        self.InitAttr(op, bool, [s_ui.S_SEEN_BY_TRANS])
        self.InitAttr(op, bool, [s_ui.S_SEEN_BY_REFRACTION])
        self.InitAttr(op, float, [s_ui.S_ROT_X])
        self.InitAttr(op, float, [s_ui.S_HDRI_HUE])
        self.InitAttr(op, float, [s_ui.S_HDRI_SATURAYION])
        self.InitAttr(op, float, [s_ui.S_HDRI_LIGHTNESS])
        self.InitAttr(op, float, [s_ui.S_HDRI_BRIGHTNESS])
        self.InitAttr(op, float, [s_ui.S_HDRI_CONTRAST])
        self.InitAttr(op, float, [s_ui.S_HDRI_GAMMA])
        self.InitAttr(op, float, [s_ui.S_RADIUS_PREVIEW])

        self.InitAttr(op, float, [s_ui.S_BRIGHTNESS])

        # значения поумолчанию
        op[s_ui.S_FILE] = m.hdr_file_path
        op[s_ui.S_SHOW_PREVIEW] = False
        op[s_ui.S_COLORIZE] = False
        op[s_ui.S_SEEN_BY_TRANS] = False
        op[s_ui.S_SEEN_BY_REFRACTION] = False
        op[s_ui.S_ROT_X] = 0.0
        op[s_ui.S_HDRI_HUE] = 0.0
        op[s_ui.S_HDRI_SATURAYION] = 0.0
        op[s_ui.S_HDRI_LIGHTNESS] = 0.0
        op[s_ui.S_HDRI_BRIGHTNESS] = 0.0
        op[s_ui.S_HDRI_CONTRAST] = 0.0
        op[s_ui.S_HDRI_GAMMA] = 1.0
        op[s_ui.S_RADIUS_PREVIEW] = 100.0

        op[s_ui.S_BRIGHTNESS] = 1.0

        return True
    #--------------------------------------------------------------------------------------------


    #-------------------------------------------------------------------------- Генерация объекта
    def GetVirtualObjects(self, op, hierarchyhelp):

        matlayer()

        doc = op.GetDocument()
        rd = doc.GetActiveRenderData()

        #------------------------------------------------------------------------------------------------------------------- материалы
        if rd[c4d.RDATA_RENDERENGINE] == S.Standard or rd[c4d.RDATA_RENDERENGINE] == S.Physical:

            self.base = c4d.BaseObject(c4d.Onull)
            self.base.SetName(op.GetName())

            root = doc.GetLayerObjectRoot()
        
            if doc.SearchMaterial(op.GetName() + ' illumination map') == None and doc.SearchMaterial(op.GetName() + ' reflection map') == None:

                self.matIn_SR = c4d.documents.MergeDocument(doc, m.mat_SR, c4d.SCENEFILTER_MATERIALS)
                self.MatTemp_SR = doc.SearchMaterial('reflection map')
                self.MatTemp_SR.SetName(op.GetName() + ' reflection map')

                self.matIn_SI = c4d.documents.MergeDocument(doc, m.mat_SI, c4d.SCENEFILTER_MATERIALS)
                self.MatTemp_SI = doc.SearchMaterial('illumination map')
                self.MatTemp_SI.SetName(op.GetName() + ' illumination map')

                self.MatTemp_SR.SetLayerObject(root.GetDown())
                self.MatTemp_SI.SetLayerObject(root.GetDown())

                c4d.EventAdd()

            elif doc.SearchMaterial(op.GetName() + ' illumination map') != None and doc.SearchMaterial(op.GetName() + ' reflection map') == None:

                self.matIn_SR = c4d.documents.MergeDocument(doc, m.mat_SR, c4d.SCENEFILTER_MATERIALS)
                self.MatTemp_SR = doc.SearchMaterial('reflection map')
                self.MatTemp_SR.SetName(op.GetName() + ' reflection map')

                self.MatTemp_SR.SetLayerObject(root.GetDown())

                c4d.EventAdd()

            elif doc.SearchMaterial(op.GetName() + ' illumination map') == None and doc.SearchMaterial(op.GetName() + ' reflection map') != None:

                self.matIn_SI = c4d.documents.MergeDocument(doc, m.mat_SI, c4d.SCENEFILTER_MATERIALS)
                self.MatTemp_SI = doc.SearchMaterial('illumination map')
                self.MatTemp_SI.SetName(op.GetName() + ' illumination map')

                self.MatTemp_SI.SetLayerObject(root.GetDown())

                c4d.EventAdd()
            #-------------------------------------------------------------------------------------------------- конец материалы


            #------------------------------------------------------------------------------------------------------- настройки материалов
            self.mat_SR = doc.SearchMaterial(op.GetName() + ' reflection map')
            self.mat_SR[c4d.MATERIAL_LUMINANCE_BRIGHTNESS] = op[s_ui.S_BRIGHTNESS]
            self.mat_SR[c4d.MATERIAL_GLOBALILLUM_GENERATE] = False
            self.mat_SR[c4d.MATERIAL_GLOBALILLUM_RECEIVE] = False
            self.mat_SR[c4d.MATERIAL_CAUSTICS_GENERATE] = False
            self.mat_SR[c4d.MATERIAL_CAUSTICS_RECEIVE] = False

            self.mat_SI = doc.SearchMaterial(op.GetName() + ' illumination map')
            self.mat_SI[c4d.MATERIAL_LUMINANCE_BRIGHTNESS] = op[s_ui.S_BRIGHTNESS]
            self.mat_SI[c4d.MATERIAL_GLOBALILLUM_RECEIVE] = False
            self.mat_SI[c4d.MATERIAL_CAUSTICS_RECEIVE] = False

            if op[s_ui.S_LOCK_GI] == True:
                self.mat_SI[c4d.MATERIAL_GLOBALILLUM_GENERATE_STRENGTH] = op[s_ui.S_BRIGHTNESS]
            elif op[s_ui.S_LOCK_GI] == False:
                self.mat_SI[c4d.MATERIAL_GLOBALILLUM_GENERATE_STRENGTH] = op[s_ui.S_GI]

            #-------------------------------------------------------------------------------------------------------- превью объект с материалом
            self.sky_preview = c4d.BaseObject(5160)
            self.sky_preview.SetName(op.GetName() + ' sky preview map')
            self.sky_preview.InsertUnder(self.base)

            if op[s_ui.S_SHOW_PREVIEW] == False:
                self.sky_preview[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 1
            elif op[s_ui.S_SHOW_PREVIEW] == True:
                self.sky_preview[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 0

            self.sky_preview[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 1
            self.sky_preview[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_X] = op[s_ui.S_ROT_X]
            self.sky_preview[c4d.PRIM_SPHERE_RAD] = op[s_ui.S_RADIUS_PREVIEW]
            self.sky_preview[c4d.ID_BASEOBJECT_XRAY] = 1

            self.tag_mat_SP_onSky = self.sky_preview.MakeTag(5616)
            self.tag_mat_SP_onSky[c4d.ID_BASELIST_NAME] = (op.GetName() + ' texture tag preview')
            self.tag_mat_SP_onSky[c4d.TEXTURETAG_MATERIAL] = self.mat_SR

            self.dis_preview = self.sky_preview.MakeTag(5613)
            self.dis_preview[c4d.DISPLAYTAG_AFFECT_DISPLAYMODE] = 1
            self.dis_preview[c4d.DISPLAYTAG_SDISPLAYMODE] = 1
            #--------------------------------------------------------------------------------------------------------



            #-------------------------------------------------------------------------------------------------------- объект отражения с материалами
            self.sky_reflection = c4d.BaseObject(5105)
            self.sky_reflection.SetName(op.GetName() + ' sky reflection map')
            self.sky_reflection.InsertUnder(self.base)
            self.sky_reflection[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 1
            self.sky_reflection[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_X] = self.sky_preview[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_X]

            self.tag_mat_SR_onSky = self.sky_reflection.MakeTag(5616)
            self.tag_mat_SR_onSky[c4d.ID_BASELIST_NAME] = (op.GetName() + ' texture tag itself')
            self.tag_mat_SR_onSky[c4d.TEXTURETAG_MATERIAL] = self.mat_SR

            self.shadeer_filter_SR = self.mat_SR.GetFirstShader().GetNext()
            # print self.shadeer_filter_SR
            self.shadeer_filter_SR[c4d.SLA_FILTER_HUE] = op[s_ui.S_HDRI_HUE]
            self.shadeer_filter_SR[c4d.SLA_FILTER_SATURATION] = op[s_ui.S_HDRI_SATURAYION]
            self.shadeer_filter_SR[c4d.SLA_FILTER_LIGHTNESS] = op[s_ui.S_HDRI_LIGHTNESS]
            self.shadeer_filter_SR[c4d.SLA_FILTER_COLORIZE] = op[s_ui.S_COLORIZE]
            self.shadeer_filter_SR[c4d.SLA_FILTER_BRIGHNESS] = op[s_ui.S_HDRI_BRIGHTNESS]
            self.shadeer_filter_SR[c4d.SLA_FILTER_CONTRAST] = op[s_ui.S_HDRI_CONTRAST]
            self.shadeer_filter_SR[c4d.SLA_FILTER_GAMMA] = op[s_ui.S_HDRI_GAMMA]

            self.shader_bitmap_SR = self.shadeer_filter_SR[c4d.SLA_FILTER_TEXTURE]
            # print self.shader_bitmap_SR

            if op[s_ui.S_FILE] != None:
                self.shader_bitmap_SR[c4d.BITMAPSHADER_FILENAME] = op[s_ui.S_FILE]

            self.tag_comp_SR_onSky = self.sky_reflection.MakeTag(5637)
            self.tag_comp_SR_onSky[c4d.ID_BASELIST_NAME] = (op.GetName() + ' compositing tag itself')
            self.tag_comp_SR_onSky[c4d.COMPOSITINGTAG_CASTSHADOW] = 0
            self.tag_comp_SR_onSky[c4d.COMPOSITINGTAG_RECEIVESHADOW] = 0
            self.tag_comp_SR_onSky[c4d.COMPOSITINGTAG_SEENBYCAMERA] = 0
            self.tag_comp_SR_onSky[c4d.COMPOSITINGTAG_SEENBYRAYS] = 1
            self.tag_comp_SR_onSky[c4d.COMPOSITINGTAG_SEENBYGI] = 0

            self.tag_comp_SR_onSky[c4d.COMPOSITINGTAG_SEENBYTRANSPARENCY] = 0
            self.tag_comp_SR_onSky[c4d.COMPOSITINGTAG_SEENBYREFRACTION] = 0
            self.tag_comp_SR_onSky[c4d.COMPOSITINGTAG_SEENBYREFLECTION] = 1
            self.tag_comp_SR_onSky[c4d.COMPOSITINGTAG_SEENBYAO] = 0
            #--------------------------------------------------------------------------------------------------------



            #-------------------------------------------------------------------------------------------------------- объект освещения с материалами
            self.sky_illimination = c4d.BaseObject(5105)
            self.sky_illimination.SetName(op.GetName() + ' sky illumination map')
            self.sky_illimination.InsertUnder(self.base)
            self.sky_illimination[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 1
            self.sky_illimination[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_X] = self.sky_preview[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_X]

            self.tag_mat_SI_onSky = self.sky_illimination.MakeTag(5616)
            self.tag_mat_SI_onSky[c4d.ID_BASELIST_NAME] = (op.GetName() + ' texture tag itself')
            self.tag_mat_SI_onSky[c4d.TEXTURETAG_MATERIAL] = self.mat_SI

            self.shadeer_filter_SI = self.mat_SI.GetFirstShader()
            # print self.shadeer_filter_SI
            self.shadeer_filter_SI[c4d.SLA_FILTER_HUE] = op[s_ui.S_HDRI_HUE]
            self.shadeer_filter_SI[c4d.SLA_FILTER_SATURATION] = op[s_ui.S_HDRI_SATURAYION]
            self.shadeer_filter_SI[c4d.SLA_FILTER_LIGHTNESS] = op[s_ui.S_HDRI_LIGHTNESS]
            self.shadeer_filter_SI[c4d.SLA_FILTER_COLORIZE] = op[s_ui.S_COLORIZE]
            self.shadeer_filter_SI[c4d.SLA_FILTER_BRIGHNESS] = op[s_ui.S_HDRI_BRIGHTNESS]
            self.shadeer_filter_SI[c4d.SLA_FILTER_CONTRAST] = op[s_ui.S_HDRI_CONTRAST]
            self.shadeer_filter_SI[c4d.SLA_FILTER_GAMMA] = op[s_ui.S_HDRI_GAMMA]

            self.shader_bitmap_SI = self.shadeer_filter_SI[c4d.SLA_FILTER_TEXTURE]
            # print self.shader_bitmap_SI

            if op[s_ui.S_FILE] != None:
                self.shader_bitmap_SI[c4d.BITMAPSHADER_FILENAME] = op[s_ui.S_FILE]

            self.tag_comp_SI_onSky = self.sky_illimination.MakeTag(5637)
            self.tag_comp_SI_onSky[c4d.ID_BASELIST_NAME] = (op.GetName() + ' compositing tag itself')
            self.tag_comp_SI_onSky[c4d.COMPOSITINGTAG_CASTSHADOW] = 0
            self.tag_comp_SI_onSky[c4d.COMPOSITINGTAG_RECEIVESHADOW] = 0
            self.tag_comp_SI_onSky[c4d.COMPOSITINGTAG_SEENBYCAMERA] = 0
            self.tag_comp_SI_onSky[c4d.COMPOSITINGTAG_SEENBYRAYS] = 1
            self.tag_comp_SI_onSky[c4d.COMPOSITINGTAG_SEENBYGI] = 1

            self.tag_comp_SI_onSky[c4d.COMPOSITINGTAG_SEENBYTRANSPARENCY] = 0
            self.tag_comp_SI_onSky[c4d.COMPOSITINGTAG_SEENBYREFRACTION] = 0
            self.tag_comp_SI_onSky[c4d.COMPOSITINGTAG_SEENBYREFLECTION] = 0
            self.tag_comp_SI_onSky[c4d.COMPOSITINGTAG_SEENBYAO] = 0
            #--------------------------------------------------------------------------------------------------------

        elif rd[c4d.RDATA_RENDERENGINE] != S.Standard or rd[c4d.RDATA_RENDERENGINE] != S.Physical:
            return None

        return self.base
    #-------------------------------------------------------------------- КОНЕЦ Генерации объекта


    #--------------------------------------------------------------------------------- Прорисовка
    def Message(self, op, type, data):

        if type == c4d.MSG_DESCRIPTION_COMMAND:

            # Helper
            if data["id"][0].id == s_ui.S_HELP:

                self.dialog = Helper()
                self.dialog.show(os.path.join(h.sky_URL), S.STR_BROWSERDIALOG_TITLE, 200, 100, 700, 700)

        #-------------------------------------------- DAYLIGHT контейнер
        if op[s_ui.S_SUN] != None:

            if op[s_ui.S_SUN].GetType() == d_ui.DAYLIGHT:

                daylight = op[s_ui.S_SUN]

                daylight[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_X] = op[s_ui.S_ROT_X]

            elif op[s_ui.S_SUN].GetType() != d_ui.DAYLIGHT:

                op[s_ui.S_SUN] = None

        return True
    #--------------------------------------------------------------------------- КОНЕЦ Прорисовки


    #------------------------------------------------------------------------ выкл/вкл интерфейса
    def GetDEnabling(self, op, id, t_data, flags, itemdesc):

        data = op.GetDataInstance()
        if data is None: return
        ID = id[0].id

        doc = op.GetDocument()
        rd = doc.GetActiveRenderData()

        #--------------------------------------------------
        if rd[c4d.RDATA_RENDERENGINE] == S.Standard:
            op[s_ui.S_RENDERER] = S.R_S

        elif rd[c4d.RDATA_RENDERENGINE] == S.Physical:
            op[s_ui.S_RENDERER] = S.R_P

        elif rd[c4d.RDATA_RENDERENGINE] != S.Standard or rd[c4d.RDATA_RENDERENGINE] != S.Physical:
            op[s_ui.S_RENDERER] = S.WARNING

        if rd[c4d.RDATA_RENDERENGINE] == S.Standard or rd[c4d.RDATA_RENDERENGINE] == S.Physical:
            if op[s_ui.S_LOCK_GI] == True:
                if ID == S_GI:
                    return False

            elif op[s_ui.S_LOCK_GI] == False:
                if ID == S_GI:
                    return True

        elif rd[c4d.RDATA_RENDERENGINE] != S.Standard or rd[c4d.RDATA_RENDERENGINE] != S.Physical:
            
            if ID == s_ui.S_FILE:
                return False

            if ID == s_ui.S_SUN:
                return False

            if ID == s_ui.S_SHOW_PREVIEW:
                return False

            if ID == s_ui.S_RADIUS_PREVIEW:
                return False

            if ID == s_ui.S_ROT_X:
                return False

            if ID == s_ui.S_BRIGHTNESS:
                return False

            if ID == s_ui.S_HDRI_HUE:
                return False

            if ID == s_ui.S_HDRI_SATURAYION:
                return False

            if ID == s_ui.S_HDRI_LIGHTNESS:
                return False

            if ID == s_ui.S_COLORIZE:
                return False

            if ID == s_ui.S_HDRI_BRIGHTNESS:
                return False

            if ID == s_ui.S_HDRI_CONTRAST:
                return False

            if ID == s_ui.S_HDRI_GAMMA:
                return False
        #--------------------------------------------------

        return True
    #----------------------------------------------------------------- КОНЕЦ  выкл/вкл интерфейса


#-------------------------------------------------------------------------------------- КОНЕЦ Sky


# инициализация компонентов
if __name__ == '__main__':

    dir, file = os.path.split(__file__)

    # Sky
    iconS = c4d.bitmaps.BaseBitmap()
    iconS.InitWith(os.path.join(dir, S.pathicons, S.skyIcon))
    plugins.RegisterObjectPlugin(id = s_ui.SKY, str = "Sky", g = Sky, description = "Sky", info = c4d.OBJECT_GENERATOR, icon = iconS )