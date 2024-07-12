from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import ArtistaView, GeneroView

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    path('artistas/', ArtistaView.as_view(), name='artistas'),
    path('artistas/<int:pk>/', ArtistaView.as_view(), name='artistas-detalhe'),

    path('generos/', GeneroView.as_view(), name='generos'),
]
