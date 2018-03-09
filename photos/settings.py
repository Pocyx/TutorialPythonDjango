# -*- coding: utf-8 -*-
from django.conf import settings

COPYRIGHT = 'RIG'
COPYLEFT = 'LEF'
CREATIVE_COMMONS = 'CC'

DEFAULT_LICENSES = (
    (COPYRIGHT, 'Copyright'),
    (COPYLEFT, 'Copyleft'),
    (CREATIVE_COMMONS, 'Creative commons')
)

LICENSES = getattr(settings, 'LICENSES', DEFAULT_LICENSES)
# BUSCA VARIABLE LICENSES EN SETTINGS DEL PROYECTO, SI NO USA DEFAUL_LICENSES

BADWORDS = getattr(settings, 'BADWORDS', [])