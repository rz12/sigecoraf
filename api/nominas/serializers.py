from rest_framework import serializers

from app.nominas import models
from app.nominas.models import Empleado, RolPago, Cargo, Contrato


class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = '__all__'


class RolPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolPago


class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = '__all__'


class ContratoSerializer(serializers.ModelSerializer):
    class Meta:
        models = Contrato
