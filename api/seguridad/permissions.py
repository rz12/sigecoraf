import json

from django.http.response import HttpResponse
from rest_framework import status

from app.master.utils.enums import AuthEnum
from app.seguridad.views import verificar_permisos_acceso


class IsAuthenticated(object):
    '''
    Decorador que se ejecuta al consumir el API.
    Valida si el usuario esta logueado y si tienen permisos a una funcionalid o
    menu.
    '''

    def __call__(self, funcion):
        """
        Funcion que valida la permisos
        para ejecutar la función
        :param funcion: función del API a ejecutar:
        """

        def wrapper(request, *args, **kwargs):
            token = request.META['HTTP_AUTHORIZATION']
            menu = None
            if 'MENU' in request.GET:
                menu = request.GET['MENU']

            permission = verificar_permisos_acceso(token, menu,
                                                   None)
            if (permission['isPermission'] is False):
                return HttpResponse(
                    json.dumps({'status': status.HTTP_401_UNAUTHORIZED,
                                'message': permission['message']}),
                    content_type='application/json')

            return funcion(request, *args, **kwargs)

        return wrapper
