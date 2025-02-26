from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import datetime, timedelta

from interview.inventory.models import Inventory, InventoryType, InventoryLanguage, InventoryTag

class InventoryListGetItemsViewTest(APITestCase):

    def setUp(self):
        self.url = reverse('inventory-items')
        self.inventory_type = InventoryType.objects.create(name='Book')
        self.inventory_language = InventoryLanguage.objects.create(name='English')
        self.inventory_tag_1 = InventoryTag.objects.create(name='Fiction')
        self.inventory_tag_2 = InventoryTag.objects.create(name='Non-Fiction')

        now = datetime.now()
        for i in range(5):
            created_at = now - timedelta(days=i)
            inventory_item = Inventory.objects.create(
                name=f'Item {i+1}',
                type=self.inventory_type,
                language=self.inventory_language,
                metadata={'key': 'value'},
            )
            inventory_item.created_at = created_at
            inventory_item.save()
            inventory_item.tags.add(self.inventory_tag_1)

    def test_created_after_required(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'created_after parameter is required'})

    def test_invalid_created_after_format(self):
        response = self.client.get(self.url, {'created_after': 'invalid-date-format'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Invalid created_after date format. Please use ISO format.'})

    def test_invalid_limit_format(self):
        created_after_str = datetime.now().isoformat() + 'Z'
        response = self.client.get(self.url, {'created_after': created_after_str, 'limit': 'abc'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Limit must be an integer'})

    def test_valid_pagination(self):
        created_after_str = (datetime.now() - timedelta(days=7)).isoformat() + 'Z'
        response = self.client.get(self.url, {'created_after': created_after_str, 'page': '1', 'limit': '2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], 'Item 5')
        self.assertEqual(response.data[1]['name'], 'Item 4')

        response_page_2 = self.client.get(self.url, {'created_after': created_after_str, 'page': '2', 'limit': '2'})
        self.assertEqual(response_page_2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_page_2.data), 2)
        self.assertEqual(response_page_2.data[0]['name'], 'Item 3')
        self.assertEqual(response_page_2.data[1]['name'], 'Item 2')

        response_page_3 = self.client.get(self.url, {'created_after': created_after_str, 'page': '3', 'limit': '2'})
        self.assertEqual(response_page_3.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_page_3.data), 1)
        self.assertEqual(response_page_3.data[0]['name'], 'Item 1')

    def test_max_limit_enforcement(self):
        created_after_str = (datetime.now() - timedelta(days=7)).isoformat() + 'Z'
        response = self.client.get(self.url, {'created_after': created_after_str, 'limit': '5'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_empty_page(self):
        created_after_str = (datetime.now() - timedelta(days=7)).isoformat() + 'Z'
        response = self.client.get(self.url, {'created_after': created_after_str, 'page': '999'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'data': [], 'message': 'Page is empty'})

    def test_default_limit_and_page(self):
        created_after_str = (datetime.now() - timedelta(days=7)).isoformat() + 'Z'
        response = self.client.get(self.url, {'created_after': created_after_str})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['name'], 'Item 5')
