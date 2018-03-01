from django.db import models
from django.contrib.auth.models import *

class Usuario(User):
    empresa = models.ForeignKey('master.Empresa', related_name='usuarios', on_delete=models.CASCADE)
