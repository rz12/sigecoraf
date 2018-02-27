from django.db import models
import datetime

from app.master.models import Persona


class Empleado(Persona):
    fecha_inicio = models.DateField(default=datetime.date.today)
    fecha_fin = models.DateField(default=datetime.date.today, null=True
    blank = True)
    fecha_ingreso_iess = models.DateField(default=datetime.date.today, null=True
    blank = True)
    estado = models.BooleanField(default=True)
    empresa = models.ForeignKey('master.Empresa', related_name='empleados', on_delete=models.CASCADE)


class Cargo(models.Model):
    nombre = models.CharField(max_length=250, blank=False, null=False)
    descripcion = models.TextField(max_length=500, null=True, blank=True)
    estado = models.BooleanField(default=True)
    empresa = models.ForeignKey('master.Empresa', related_name='cargos', on_delete=models.CASCADE)
    sueldo = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        self.nombre


class Contrato(models.Model):
    fecha_inicio = models.DateField(default=datetime.date.today)
    fecha_fin = models.DateField(default=datetime.date.today, null=True, blank=True)
    estado = models.BooleanField(default=True)
    mensualizar_decimos = models.BooleanField(default=True, null=True, blank=True)


class EstructuraDetalleRolPago(models.Model):
    nombre = models.CharField(max_length=250, blank=False, null=False)
    descripcion = models.TextField(max_length=500, blank=True, null=True)
    estado = models.BooleanField(default=True)
    empresa = models.ForeignKey('master.Empresa', related_name='cargos', on_delete=models.CASCADE)
    operacion = models.IntegerField(null=False, blank=False)

    def __str__(self):
        self.nombre


class RolPago(models.Model):
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2)


class DetalleRolPago(models.Model):
    nombre = models.CharField(max_length=250, blank=False, null=False)
    descripcion = models.TextField(max_length=500, null=True, blank=True)
    estructura_detalle_rolpago = models.ForeignKey('master.EstructuraDetalleRolPago', related_name='detalles',
                                                   on_delete=models.CASCADE)
    rol_pago = models.ForeignKey('master.RolPago', related_name='detalles', on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
