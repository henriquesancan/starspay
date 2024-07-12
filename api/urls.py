from django.urls import path
from .views import ArtistaView, GeneroView

urlpatterns = [
    path('artistas/', ArtistaView.as_view(), name='artistas'),
    path('artistas/<int:pk>/', ArtistaView.as_view(), name='artistas-detalhe'),

    path('generos/', GeneroView.as_view(), name='generos'),
]
