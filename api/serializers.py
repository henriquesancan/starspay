from rest_framework import serializers
from .models import Artista, Genero


class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genero
        fields = ['id', 'nome', 'created_at', 'updated_at']


class ArtistaSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(max_length=100)
    genero = serializers.PrimaryKeyRelatedField(queryset=Genero.objects.all())
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    deleted_at = serializers.DateTimeField(read_only=True, allow_null=True)

    @staticmethod
    def validate_nome(value):
        if Artista.objects.filter(nome=value).exists():
            raise serializers.ValidationError("Este nome já está em uso.")

        return value

    def create(self, validated_data):
        return Artista.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.genero = validated_data.get('genero', instance.genero)
        instance.nome = validated_data.get('nome', instance.nome)
        instance.save()

        return instance

