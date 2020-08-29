# coding: utf-8

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

#----------------------------------------- Пути к файлам c4d и материалам
card_rel_path = '../materials/luma.c4d'
cardMat = os.path.join(folder, card_rel_path)

floor_rel_path = '../materials/floor.c4d'
floorMat = os.path.join(folder, floor_rel_path)

mat_SI_rel_path = '../materials/illumination.c4d'
mat_SI = os.path.join(folder, mat_SI_rel_path)

mat_SR_rel_path = '../materials/refiection.c4d'
mat_SR = os.path.join(folder, mat_SR_rel_path)

studio_mat_rel_path = '../materials/studio.c4d'
studio_mat = os.path.join(folder, studio_mat_rel_path)

# Default HDRI
hdr_path = '../materials/tex/default.hdr'
hdr_file_path = os.path.join(folder, hdr_path)
#-------------------------------------------------------------------- end