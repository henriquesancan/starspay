from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Artista, Genero


class ArtistaViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.genero = Genero.objects.create(nome='Jazz')
        self.artista_data = {
            'nome': 'Artista Testes',
            'genero': self.genero.id
        }
        self.artista = Artista.objects.create(nome='Artista Teste', genero=self.genero)
        self.artista_url = reverse('artistas-detalhe', kwargs={'pk': self.artista.pk})

    def test_create_artista(self):
        response = self.client.post(reverse('artistas'), self.artista_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_artista(self):
        response = self.client.get(self.artista_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], self.artista.nome)

    def test_update_artista(self):
        updated_data = {
            'nome': 'Artista Atualizado',
            'genero': self.genero.id
        }
        response = self.client.put(self.artista_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.artista.refresh_from_db()
        self.assertEqual(self.artista.nome, 'Artista Atualizado')

    def test_delete_artista(self):
        response = self.client.delete(self.artista_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Artista.objects.filter(pk=self.artista.pk).exists())

    def test_get_all_artistas(self):
        response = self.client.get(reverse('artistas'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
