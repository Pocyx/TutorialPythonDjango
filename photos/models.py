# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from photos.settings import LICENSES

#COPYRIGHT = 'RIG'
#COPYLEFT = 'LEF'
#CREATIVE_COMMONS = 'CC'

#LICENSES = (
#    (COPYRIGHT, 'Copyright'),
#    (COPYLEFT, 'Copyleft'),
#    (CREATIVE_COMMONS, 'Creative commons')
#)

PUBLIC = 'PUB'
PRIVATE = 'PRI'

VISIBILITY = (
    (PUBLIC, 'Pública'),
    (PRIVATE, 'Privada')
)

class Photos(models.Model):

    owner = models.ForeignKey(User)
    name = models.CharField(max_length=150)
    url = models.URLField()
    description = models.TextField(blank=True, null=True, default="")
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)
    license = models.CharField(max_length=3, choices=LICENSES)
    visibility = models.CharField(max_length=3, choices=VISIBILITY, default=PUBLIC)

    def __unicode__(self): #metodo de 0 parametros
        return self.name
