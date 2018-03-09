# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError

from photos.models import Photos
from photos.settings import BADWORDS


class PhotoForm(forms.ModelForm):
    """
    Formulario para el modelo Photo
    """
    class Meta:
        model = Photos
        exclude = ['owner']

    def clean(self):
        """
        Valida si en la descripción de han puesto tacos definidos en
        settings.BADWORDS
        :return: diccionario con los atributos si Ok
        """
        cleaned_data = super(PhotoForm, self).clean()

        description = cleaned_data.get('description', '')

        for badwords in BADWORDS:
            if badwords.lower() in description.lower():
                raise ValidationError(u'La palabra {0} no está permitida'.format(badwords))

        #Sitodo va ok devuelvo los datos limpios
        return cleaned_data