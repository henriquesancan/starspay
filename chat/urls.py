from django.urls import path
from .views import IndexView, SalaView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<str:nome_sala>/', SalaView.as_view(), name='sala'),
]