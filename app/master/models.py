from django.db import models
import datetime


class Persona(models.Model):
    """
    Esta clase permite administrar una persona (Empleado, Gerente etc.), con sus respectivos datos personales.

    """
    numero_identificacion = models.CharField(max_length=25, unique=True,
                                             blank=False, null=False)
    primer_apellido = models.CharField(max_length=100, blank=False, null=False)
    segundo_apellido = models.CharField(max_length=100, blank=True, null=True)
    primer_nombre = models.CharField(max_length=100, blank=False, null=False)
    segundo_nombre = models.CharField(max_length=100, blank=True, null=True)
    numero_celular = models.CharField(max_length=100, blank=True, null=True)
    foto = models.FileField(null=True)
    fecha_nacimiento = models.DateField(default=datetime.date.today)
    tipo_documento_identificacion = models.ForeignKey('master.Item',
                                                      on_delete=models.CASCADE,
                                                      related_name='tipo_documento_identificacion')
    genero = models.ForeignKey('master.Item', related_name='genero',
                               on_delete=models.CASCADE)
    estado_civil = models.ForeignKey('master.Item', related_name='estado_civil',
                                     on_delete=models.CASCADE)


class Direccion(models.Model):
    """

    """
    calle_principal = models.TextField(max_length=500, blank=False, null=False)
    calle_secundaria = models.TextField(max_length=500, blank=True, null=True)
    pais = models.ForeignKey('master.Item',related_name='paises', on_delete=models.CASCADE)
    ciudad = models.CharField(max_length=250, blank=False, null=False)
    referencia = models.TextField(max_length=500, blank=True, null=True)
    tipo_direccion = models.ForeignKey('master.Item',
                                       related_name='tipo_direccion',
                                       on_delete=models.CASCADE)
    numero_telefono = models.CharField(max_length=500, blank=True, null=True)
    persona = models.ForeignKey('master.Persona', related_name='direcciones',
                                on_delete=models.CASCADE)


class Empresa(models.Model):
    nombre = models.CharField(max_length=250, blank=False, null=False)
    descripcion = models.TextField(max_length=500, blank=False, null=False)
    estado = models.BooleanField(default=True, blank=False, null=False)
    logo = models.FileField(null=True, blank=True)
    autorizacion_sri = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.nombre


class Catalogo(models.Model):
    codigo = models.CharField(max_length=25, blank=False, null=False,
                              unique=True)
    nombre = models.CharField(max_length=250, blank=False, null=False)
    descripcion = models.TextField(max_length=500, null=True, blank=True)
    estado = models.BooleanField(default=True)
    empresa = models.ForeignKey('master.Empresa', related_name='catalogos',
                                on_delete=models.CASCADE,null=True,blank=True)


class Item(models.Model):
    codigo = models.CharField(max_length=25, blank=False, null=False,
                              unique=True)
    nombre = models.CharField(max_length=250, blank=False, null=False)
    descripcion = models.TextField(max_length=500, null=False)
    estado = models.BooleanField(default=True)
    catalogo = models.ForeignKey('master.Catalogo', related_name='items',
                                 on_delete=models.CASCADE)
    padre = models.ForeignKey('self', null=True, blank=True,
                              on_delete=models.CASCADE)
    def __eq__(self, other):
        return self.id== other.id


class Parametrizacion(models.Model):
    codigo = models.CharField(max_length=25, blank=False, null=False,
                              unique=True)
    nombre = models.CharField(max_length=250, blank=False, null=False)
    descripcion = models.TextField(max_length=500, blank=True, null=True)
    estado = models.BooleanField(default=True)
    empresa = models.ForeignKey('master.Empresa',
                                related_name='parametrizaciones',
                                on_delete=models.CASCADE)


class DetalleParametrizacion(models.Model):
    codigo = models.CharField(max_length=25, blank=False, null=False,
                              unique=True)
    nombre = models.CharField(max_length=250, blank=False, null=False)
    descripcion = models.TextField(max_length=500, null=True, blank=True)
    estado = models.BooleanField(default=True)
    valor = models.CharField(max_length=250, blank=False, null=False)
    parametrizacion = models.ForeignKey('master.Parametrizacion',
                                        related_name='detalles',
                                        on_delete=models.CASCADE)

    class Meta:
        unique_together = ('codigo', 'nombre', 'descripcion', 'valor')
        ordering = ['codigo']

    def __unicode__(self):
        return '%s: %s' % (self.codigo, self.nombre)
