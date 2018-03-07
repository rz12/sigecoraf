from django.contrib.auth.models import *
from django.db import models


class Usuario(User):
    empresa = models.ForeignKey('master.Empresa', related_name='usuarios',
                                on_delete=models.CASCADE)



class Menu(models.Model):
    codigo = models.CharField(max_length=50, unique=True, blank=False,
                              null=False)
    nombre = models.CharField(max_length=250, blank=False, null=False)
    descripcion = models.TextField(max_length=500, blank=True, null=True)
    estado = models.BooleanField(default=True)
    formulario = models.CharField(max_length=250, blank=True, null=True)
    empresa = models.ForeignKey('master.Empresa', related_name='menus',
                                on_delete=models.CASCADE)


class MenuUsuario(models.Model):
    menu = models.ForeignKey('seguridad.Menu', related_name='menus_usuario',
                             on_delete=models.CASCADE)
    usuario = models.ForeignKey('seguridad.Usuario', related_name='menus',
                                on_delete=models.CASCADE)


class MenuGroup(models.Model):
    menu = models.ForeignKey('seguridad.Menu', related_name='menus_group',
                             on_delete=models.CASCADE)
    group = models.ForeignKey('auth.Group', related_name='menus',
                              on_delete=models.CASCADE)
