from django.conf import settings
from django.contrib.auth.models import *
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Usuario(User):
    """
    Modelo Usuario que hereda de User del modelo de seguridad de Django.
    """
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
    padre = models.ForeignKey('self', related_name='submenus', null=True,
                              blank=True, on_delete=models.CASCADE)
    orden = models.IntegerField(default=True, null=True, blank=True)
    icono = models.CharField(max_length=250, blank=False, null=False)

    def __str__(self):
        return self.codigo


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


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
