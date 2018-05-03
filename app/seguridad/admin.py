from django.contrib import admin

from app.master.models import Parametrizacion, DetalleParametrizacion
from app.seguridad.models import Usuario, Menu, MenuGroup


class UsuarioAdmin(admin.ModelAdmin):
    exclude = ('password',)
    search_fields = ('username',)
    list_display = ('username', 'email', 'empresa')
    list_display_links = ('username',)
    list_per_page = 25


class DetalleParametrizacionInline(admin.TabularInline):
    model = DetalleParametrizacion
    extra = 1


class ParametrizacionAdmin(admin.ModelAdmin):
    search_fields = ('codigo',)
    list_display = ('codigo', 'nombre', 'descripcion', 'empresa')
    list_display_links = ('codigo',)
    inlines = [DetalleParametrizacionInline]
    list_per_page = 25


class MenuAdmin(admin.ModelAdmin):
    search_fields = ('codigo',)
    list_display = ('codigo', 'nombre', 'descripcion', 'empresa')
    list_display_links = ('codigo',)
    list_per_page = 25


class MenuGroupAdmin(admin.ModelAdmin):
    search_fields = ('menu.codigo', )
    list_display = ('menu', )
    list_display_links = ('menu',)
    list_per_page = 25


admin.site.register(Parametrizacion, ParametrizacionAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuGroup, MenuGroupAdmin)
