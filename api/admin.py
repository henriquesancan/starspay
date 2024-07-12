from django.contrib import admin
from .models import Artista, Genero


class ArtistaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'genero', 'created_at')


class GeneroAdmin(admin.ModelAdmin):
    list_display = ('nome', 'created_at')


admin.site.register(Artista, ArtistaAdmin)
admin.site.register(Genero, GeneroAdmin)
