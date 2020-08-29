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

#-------------------------------------------------------------------- Helps
doc_dounce_rel_path = '../help/BounceCard.html'
bounce_URL = os.path.join(folder, doc_dounce_rel_path)

doc_daylight_rel_path = '../help/Daylight.html'
daylight_URL = os.path.join(folder, doc_daylight_rel_path)

doc_globallight_rel_path = '../help/Globallight.html'
globallight_URL = os.path.join(folder, doc_globallight_rel_path)

doc_floor_rel_path = '../help/Floor.html'
floor_URL = os.path.join(folder, doc_floor_rel_path)

doc_overhead_rel_path = '../help/Overhead.html'
overhead_URL = os.path.join(folder, doc_overhead_rel_path)

doc_sky_rel_path = '../help/Sky.html'
sky_URL = os.path.join(folder, doc_sky_rel_path)

doc_softbox_rel_path = '../help/Softbox.html'
softbox_URL = os.path.join(folder, doc_softbox_rel_path)

doc_studio_rel_path = '../help/Studio.html'
studio_URL = os.path.join(folder, doc_studio_rel_path)
#-------------------------------------------------------------------- end