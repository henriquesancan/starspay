from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Artista, Genero
from .serializers import ArtistaSerializer, GeneroSerializer


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class GeneroView(generics.ListCreateAPIView):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ArtistaView(APIView):
    @swagger_auto_schema(
        operation_description='Lista artistas',
        responses={
            200: openapi.Response(
                description='Successful response',
                schema=ArtistaSerializer(many=True)
            ),
            400: 'Bad Request',
            404: 'Not Found'
        },
    )
    def get(self, request, pk=None):
        if pk is not None:
            try:
                artista = get_object_or_404(Artista, pk=pk)
                serializer = ArtistaSerializer(artista)
            except Artista.DoesNotExist:
                return Response({'error': 'Artista not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            artistas = Artista.objects.all()
            serializer = ArtistaSerializer(artistas, many=True)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)('chat_vendas', {
            'type': 'chat_message',
            'message': 'Artistas consultados'
        })

        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description='Atualiza um artista',
        request_body=ArtistaSerializer,
        responses={
            200: ArtistaSerializer,
            400: 'Bad Request',
            404: 'Not Found'
        },
    )
    def put(self, request, pk):
        try:
            artista = get_object_or_404(Artista, pk=pk)
            serializer = ArtistaSerializer(artista, data=request.data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Artista.DoesNotExist:
            return Response({'error': 'Artista not found'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description='Deleta um artista',
        responses={
            204: 'No Content',
            404: 'Not Found'
        },
    )
    def delete(self, request, pk):
        try:
            artista = get_object_or_404(Artista, pk=pk)
            artista.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Artista.DoesNotExist:
            return Response({'error': 'Artista not found'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description='Cria um novo artista',
        request_body=ArtistaSerializer,
        responses={
            201: ArtistaSerializer,
            400: 'Bad Request'
        },
    )
    def post(self, request):
        serializer = ArtistaSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
