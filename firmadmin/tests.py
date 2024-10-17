from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Item

class ItemTests(APITestCase):
    def test_create_item(self):
        url = reverse('item-list')
        data = {'name': 'Test Item', 'description': 'Test Description'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
