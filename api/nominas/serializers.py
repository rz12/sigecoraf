from rest_framework import serializers

from app.nominas.models import Empleado, RolPago, Cargo, Contrato, \
    ConsolidadoRolPago


class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = '__all__'


class RolPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolPago
        fields = '__all__'


class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = '__all__'


class ContratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contrato
        fields = '__all__'


class ConsolidadRolPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsolidadoRolPago
        fields = '__all__'

