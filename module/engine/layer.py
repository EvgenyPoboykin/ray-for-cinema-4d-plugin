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




#------------------------------------------- функция поиска слоя по имени
def GetLayer (layername):

    doc = c4d.documents.GetActiveDocument()

    root = doc.GetLayerObjectRoot() # менеджере слоев
    LayersList = root.GetChildren() # список слоев

    for layers in LayersList:

        name = layers.GetName()

        if (name == layername):
            return layers
#--------------------------------------------------------- создание слоя
def matlayer():

    doc = c4d.documents.GetActiveDocument()

    root = doc.GetLayerObjectRoot() # менеджере слоев
    LayersList = root.GetChildren() # список слоев

    #--------------------------------------- если в менеджере слоев пусто
    if root.GetDown() == None:

        layer = c4d.documents.LayerObject() # новый слой
        layer[c4d.ID_BASELIST_NAME] = 'Materials Rays plugin'
        layer[c4d.ID_LAYER_COLOR] = c4d.Vector(0.945, 0.906, 0.208)
        layer[c4d.ID_LAYER_MANAGER] = False
        layer[c4d.ID_LAYER_LOCKED] = False

        layer.InsertUnder(root)
        c4d.EventAdd()

    #---------------------------------------- если менеджер слоев не пуст
    elif root.GetDown() != None:

        #--------------------------------------------- ищем слой по имени
        GetLayer('Materials Rays plugin')

        #----------------------- если имени нет, тогда создаем новый слой
        if GetLayer('Materials Rays plugin') == None:

            layer = c4d.documents.LayerObject() # новый слой
            layer[c4d.ID_BASELIST_NAME] = 'Materials Rays plugin'
            layer[c4d.ID_LAYER_COLOR] = c4d.Vector(0.945, 0.906, 0.208)
            layer[c4d.ID_LAYER_MANAGER] = False
            layer[c4d.ID_LAYER_LOCKED] = False

            layer.InsertUnder(root)
            c4d.EventAdd()
#-------------------------------------------------------------------------------------------- конец создание и поиск слоев
