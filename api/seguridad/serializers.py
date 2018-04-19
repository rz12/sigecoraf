from rest_framework import serializers

from app.seguridad.models import Usuario, Menu


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'username', 'email','empresa')


class MenuSerializerRecursive(serializers.Serializer):
    def to_representation(self, value):
        if value.estado is False and value.padre is not None:
            value.padre.submenus.remove(value)

        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class MenuSerializer(serializers.ModelSerializer):
    submenus = MenuSerializerRecursive(read_only=True, many=True)

    class Meta:
        model = Menu
        fields = (
        'codigo', 'descripcion', 'nombre', 'estado', 'formulario', 'empresa',
        'padre', 'orden', 'icono', 'submenus')
