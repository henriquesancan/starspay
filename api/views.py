from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Artista, Genero
from .serializers import ArtistaSerializer, GeneroSerializer


class GeneroView(generics.ListCreateAPIView):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer


class ArtistaView(APIView):
    @staticmethod
    def get(request, pk=None):
        if pk is not None:
            try:
                artista = get_object_or_404(Artista, pk=pk)
                serializer = ArtistaSerializer(artista)
            except Artista.DoesNotExist:
                return Response({'error': 'Artista not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            artistas = Artista.objects.all()
            serializer = ArtistaSerializer(artistas, many=True)

        return Response(serializer.data)

    @staticmethod
    def put(request, pk):
        try:
            artista = get_object_or_404(Artista, pk=pk)
            serializer = ArtistaSerializer(artista, data=request.data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()

                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        except Artista.DoesNotExist:
            return Response({'error': 'Artista not found'}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def delete(request, pk):
        try:
            artista = get_object_or_404(Artista, pk=pk)

            artista.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Artista.DoesNotExist:
            return Response({'error': 'Artista not found'}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def post(request):
        serializer = ArtistaSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
