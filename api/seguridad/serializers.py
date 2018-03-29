from rest_framework import serializers

from app.seguridad.models import Usuario, Menu


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'username', 'email')


class MenusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ('__all__')
