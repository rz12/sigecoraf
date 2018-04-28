from rest_framework import serializers

from api.master.serializers import EmpresaSerializer, ItemSerializer
from app.nominas.models import Empleado, RolPago, Cargo, Contrato, \
    ConsolidadoRolPago


class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = '__all__'


class EmpleadoDTOSerializer(serializers.ModelSerializer):
    empresa = EmpresaSerializer(read_only=True)
    tipo_documento_identificacion = ItemSerializer(read_only=True)
    estado_civil = ItemSerializer(read_only=True)
    genero = ItemSerializer(read_only=True)

    class Meta:
        model = Empleado
        fields = '__all__'


class CargoSerializer(serializers.ModelSerializer):
    empresa = EmpresaSerializer(read_only=True)

    class Meta:
        model = Cargo
        fields = '__all__'


class ContratoSerializer(serializers.ModelSerializer):
    empleado = EmpleadoDTOSerializer(read_only=True)
    cargo = CargoSerializer(read_only=True)

    class Meta:
        model = Contrato
        fields = '__all__'


class RolPagoSerializer(serializers.ModelSerializer):
    contrato = ContratoSerializer(read_only=True)

    class Meta:
        model = RolPago
        fields = '__all__'


class ConsolidadRolPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsolidadoRolPago
        fields = '__all__'
