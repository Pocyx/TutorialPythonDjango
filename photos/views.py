# -*- coding: utf-8 -*-


from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from photos.forms import PhotoForm
from photos.models import Photos, PUBLIC
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.db.models import Q


class PhotosQueryset(object):

    def get_queryset(self, request):
        if not request.user.is_authenticated():  # si no está autentificado
            photos = Photos.objects.filter(visibility=PUBLIC)
        elif request.user.is_superuser:  # si es administrados
            photos = Photos.objects.all()
        else:  # Usuario normal autentificado
            photos = Photos.objects.filter(Q(owner=request.user) | Q(visibility=PUBLIC))
        return photos

class HomeView(View):
    def get(self, request):
        """
        photos = Photos.objects.all()
        html = '<ul>'
        for photo in photos:
            html += '<li>' + photo.name + '</li>'
        html += '</ul>'

        return HttpResponse(html)
        """
        photos = Photos.objects.filter(visibility=PUBLIC).order_by('-created_at')
        context = {
            'photos_list' : photos[:5]
        }
        return render(request,'photos/home.html', context)


class DetailView(View):

    def get(self, request, pk):
        """
        Carga la página detalle de una foto
        :param request: HttpRequest
        :param pk:  id de la foto
        :return: HttpResponse
        """

        possible_photos = Photos.objects.filter(pk=pk).select_related('owner') #select_related('owner')  para optimizar la consulta haciendo una en lugar de dos
        photo = possible_photos[0] if len(possible_photos) == 1 else None
        if photo is not None:
            # Carga plantilla detalle
            context = {
                'photo': photo
            }
            return render(request, 'photos/detail.html', context)
        else:
            return HttpResponseNotFound('No existe la foto') # 404 not found

class CreateView(View):

    @method_decorator(login_required())
    def get(self, request):
        """
                Muestra un formulario para crear una foto y lo crea si la
                petición es POST
                :param request:
                :return:
                """
        form = PhotoForm()
        context = {
             'form': form,
            'success_message': ''
        }
        return render(request, 'photos/new_photo.html', context)

    @method_decorator(login_required())
    def post(self, request):
        """
                Muestra un formulario para crear una foto y lo crea si la
                petición es POST
                :param request:
                :return:
                """
        success_message = ''

        photo_with_owner = Photos()
        photo_with_owner.owner = request.user  # asigna como propietario de la foto, al user autentificado
        form = PhotoForm(request.POST, instance=photo_with_owner)
        if form.is_valid():
            new_photo = form.save()  # Guarda el objeto photo y melo devuelves
            form = PhotoForm()
            success_message = 'Guardada con éxito!'
            success_message += '<a href="{0}">'.format(reverse('photo_detail', args=[new_photo.pk]))
            success_message += 'Ver foto'
            success_message += '</a>'

        context = {
            'form': form,
            'success_message': success_message
        }
        return render(request, 'photos/new_photo.html', context)


class ListView(View):

    def get(self, request):
        """
        Devuelve:
        - Las fotos públicas si el usuario no está autentificado
        - Las fotos del usuario autentificado o publicas de otro
        - Si el usuario es superadministrador, todas las fotos
        :param request: HttpRequest
        :return: HttpResponse
        """

        if not request.user.is_authenticated(): #si no está autentificado
            photos = Photos.objects.filter(visibility=PUBLIC)
        elif request.user.is_superuser: # si es administrados
            photos = Photos.objects.all()
        else:  #Usuario normal autentificado
            photos = Photos.objects.filter(Q(owner=request.user) | Q(visibility=PUBLIC))
        context = {
            'photos': photos
        }
        return render(request, 'photos/photos_list.html', context)
