# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff')  # Muestra algunos campos del usuario
    actions = ['eliminar_usuarios']  # Acción personalizada para eliminar usuarios

    def eliminar_usuarios(self, request, queryset):
        queryset.delete()  # Elimina los usuarios seleccionados
        self.message_user(request, "Usuarios eliminados con éxito.")
    eliminar_usuarios.short_description = "Eliminar selecciones de usuarios"

# Registra el admin personalizado para el modelo User
admin.site.unregister(User)  # Esto solo si estás seguro de que está registrado
admin.site.register(User, UserAdmin)  # Registra el admin personalizado
