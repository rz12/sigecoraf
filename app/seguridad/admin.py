from django.contrib import admin

from app.master.models import Empresa
from app.seguridad.models import Usuario


class EmpresaAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'descripcion')
    list_display = ('nombre', 'descripcion',)
    list_display_links = ('nombre',)
    list_per_page = 25


class UsuarioAdmin(admin.ModelAdmin):
    exclude = ('password',)
    search_fields = ('username',)
    list_display = ('username', 'email', 'empresa')
    list_display_links = ('username',)
    list_per_page = 25


admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Empresa, EmpresaAdmin)
