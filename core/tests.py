from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Item

class ItemAPITestCase(APITestCase):
    def test_create_item(self):
        """
        Ensure we can create a new item object.
        """
        url = reverse('item-list')
        data = {'name': 'New Item', 'price': '9.99'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.get().name, 'New Item')