from email.headerregistry import Group

from django.contrib.auth.models import *
from rest_framework.authtoken.models import Token

from app.master.utils.enums import MessageEnum
from app.seguridad.models import MenuGroup


def verificar_permisos_acceso(token, menu=None, permiso=None):
    '''

    :param token:
    :param menu:
    :param permiso:
    :return:
    '''
    result = {'isPermission': True, 'message': 'Validación Exitosa'}
    try:
        t = Token.objects.get(key=token)
        if t is None:
            result['isPermission'] = False
            result['message'] = MessageEnum.USER_NOT_AUTHORIZED.value
            return result

        user = t.user
        if user is None:
            result['isPermission'] = False
            result['message'] = MessageEnum.USER_NOT_AUTHORIZED.value
            return result
        if menu is not None:
            if verificar_menu_group(user, menu) is False:
                result['isPermission'] = False
                result['message'] = MessageEnum.USER_NOT_AUTHORIZED.value
                return result
        if permiso is not None:
            if verificar_permission_group(user, permiso) is False:
                result['isPermission'] = False
                result['message'] = MessageEnum.USER_NOT_PERMISSION.value
                return result

        return result

    except Exception as e:
        result['isPermission'] = False
        result['message'] = MessageEnum.USER_NOT_AUTHORIZED.value
        return result

    return result


def verificar_menu_group(user, menu):
    '''
     Permite verificar si el usuario tiene permisos para acceder a un menu.
    :param user:
    :param funcionalidadValue:
    :return:
    '''
    result = False
    encontrado = False
    gruposUsuario = Group.objects.filter(user__id=user.id)
    for grupoUsuario in gruposUsuario:
        menus_group = MenuGroup.objects.filter(
            group=grupoUsuario)
        if encontrado is True:
            break
        for menu_grupo in menus_group:
            if menu_grupo.menu.codigo == menu:
                result = True
                encontrado = True
                break
    return result


def verificar_permission_group(user, permission):
    '''
    Permite verificar si un usuario posee permisos para realizar una acción
    sobre un modelo.
    :param user:
    :param permission:
    :return:
    '''
    result = False
    encontrado = False
    gruposUsuario = Group.objects.filter(user__id=user.id)
    for grupoUsuario in gruposUsuario:
        permissions = Permission.objects.filter(group=grupoUsuario)
        if encontrado is True:
            break
        for permission in permissions:
            if permission.codename == permission:
                result = True
                encontrado = True
                break
    return result
