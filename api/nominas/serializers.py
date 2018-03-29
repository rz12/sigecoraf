from rest_framework import serializers

from app.nominas import models
from app.nominas.models import Empleado, RolPago, Cargo, Contrato


class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado

class RolPagoSerializer(serializers.ModelSerializer):
    class Meta:
        models = RolPago

class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        models = Cargo

class ContratoSerializer(serializers.ModelSerializer):
    class Meta:
        models = Contrato


