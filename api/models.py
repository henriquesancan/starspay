from django.db import models
from django.utils.timezone import now


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class Genero(models.Model):
    nome = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = SoftDeleteManager()

    def __str__(self):
        return self.nome

    def delete(self, *args, **kwargs):
        self.deleted_at = now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()


class Artista(models.Model):
    nome = models.CharField(max_length=100)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE, related_name='artistas')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = SoftDeleteManager()

    def __str__(self):
        return self.nome

    def delete(self, *args, **kwargs):
        self.deleted_at = now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()
