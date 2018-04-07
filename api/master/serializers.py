from rest_framework import serializers

from app.master import models
from app.master.models import Parametrizacion, DetalleParametrizacion


class DetalleParametrizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleParametrizacion
        fields = '__all__'


class ParametrizacionSerializer(serializers.ModelSerializer):
    detalles = DetalleParametrizacionSerializer(many=True, read_only=True)

    class Meta:
        model = Parametrizacion
        fields = ('id', 'codigo', 'nombre', 'descripcion', 'detalles')