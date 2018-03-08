from django.contrib import admin

# Register your models here.
from app.master.models import Empresa


class EmpresaAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'descripcion')
    list_display = ('nombre', 'descripcion',)
    list_display_links = ('nombre',)
    list_per_page = 25


admin.site.register(Empresa, EmpresaAdmin)
