from rest_framework import serializers

from app.nominas import models
from app.nominas.models import Empleado, RolPago


class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado

class RolPagoSerializer(serializers.ModelSerializer):
    class Meta:
        models = RolPago
