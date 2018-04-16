from rest_framework import serializers

from app.master.models import Parametrizacion, DetalleParametrizacion, Empresa, \
    Item, Catalogo, Direccion


class DetalleParametrizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleParametrizacion
        fields = '__all__'


class ParametrizacionSerializer(serializers.ModelSerializer):
    detalles = DetalleParametrizacionSerializer(many=True, read_only=True)

    class Meta:
        model = Parametrizacion
        fields = ('id', 'codigo', 'nombre', 'descripcion', 'detalles')


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class CatalogoSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Catalogo
        fields = ('id', 'codigo', 'nombre', 'descripcion', 'items')


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'

class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = '__all__'
