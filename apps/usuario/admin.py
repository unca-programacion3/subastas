from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.usuario.forms import UsuarioForm
from apps.usuario.models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    add_form = UsuarioForm  # Usamos el formulario personalizado para usuarios
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('documento_identidad', 'domicilio')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('documento_identidad', 'domicilio')}),
    )
    search_fields = ('email', 'documento_identidad', 'username',)
