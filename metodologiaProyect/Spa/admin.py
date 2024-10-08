

# Spa/admin.py
from django.contrib import admin
from .models import Post, Denuncia

class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'fecha_posteo')  # Muestra el título, autor y fecha de publicación
    actions = ['eliminar_posts', 'eliminar_posts_denunciados']  # Añadimos acción para eliminar publicaciones denunciadas

    def eliminar_posts(self, request, queryset):
        queryset.delete()  # Elimina las publicaciones seleccionadas
        self.message_user(request, "Publicaciones eliminadas con éxito.")

    def eliminar_posts_denunciados(self, request, queryset):
        for post in queryset:
            if post.denuncias.exists():  # Verifica si hay denuncias
                post.delete()  # Elimina el post
                self.message_user(request, f'Publicación "{post.titulo}" eliminada junto con sus denuncias.')
            else:
                self.message_user(request, f'La publicación "{post.titulo}" no tiene denuncias asociadas.')
    eliminar_posts_denunciados.short_description = "Eliminar publicaciones denunciadas"



class DenunciaAdmin(admin.ModelAdmin):
    list_display = ('post', 'denunciante', 'motivo', 'fecha_denuncia', 'estado')  # Campos de denuncia
    actions = ['eliminar_denuncias', 'bancar_denuncias']  # Añadimos acción para banear denuncias

    def eliminar_denuncias(self, request, queryset):
        for denuncia in queryset:
            post = denuncia.post  # Obtiene el post relacionado
            denuncia.delete()  # Elimina la denuncia

            # Verifica si quedan denuncias para este post
            if not post.denuncias.exists():  # Si no quedan denuncias
                post.delete()  # Elimina el post

        self.message_user(request, "Denuncias eliminadas con éxito.")

    def bancar_denuncias(self, request, queryset):
        for denuncia in queryset:
            post = denuncia.post  # Obtiene el post relacionado
            denuncia.estado = 'baneado'  # Cambia el estado a baneado
            denuncia.save()  # Guarda la denuncia

            # Elimina el post y la denuncia
            denuncia.delete()  # Elimina la denuncia
            post.delete()  # Elimina el post

            self.message_user(request, f'Denuncia baneada y post "{post.titulo}" eliminado.')

    bancar_denuncias.short_description = "Bannear y eliminar denuncias seleccionadas"

    eliminar_denuncias.short_description = "Eliminar selecciones de denuncias"



# Registra los modelos en el panel de administración
admin.site.register(Post, PostAdmin)
admin.site.register(Denuncia, DenunciaAdmin)

