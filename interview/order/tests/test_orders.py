from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils import timezone

from interview.inventory.models import Inventory, InventoryType, InventoryLanguage, InventoryTag
from interview.order.models import Order, OrderTag


class OrderDateRangeListViewTest(APITestCase):
    def setUp(self):
        # Create Inventory related models
        self.inventory_type = InventoryType.objects.create(name="Test Type")
        self.inventory_language = InventoryLanguage.objects.create(name="Test Language")

        # Create some test data
        self.inventory1 = Inventory.objects.create(
            name="Inventory 1",
            type=self.inventory_type,
            language=self.inventory_language,
            metadata={}
        )
        self.inventory2 = Inventory.objects.create(
            name="Inventory 2",
            type=self.inventory_type,
            language=self.inventory_language,
            metadata={}
        )

        self.tag1 = OrderTag.objects.create(name="Tag 1")
        self.tag2 = OrderTag.objects.create(name="Tag 2")

        self.order1 = Order.objects.create(
            inventory=self.inventory1,
            start_date=timezone.datetime(2025, 3, 1, tzinfo=timezone.utc).date(),
            embargo_date=timezone.datetime(2025, 4, 1, tzinfo=timezone.utc).date(),
        )
        self.order1.tags.add(self.tag1)

        self.order2 = Order.objects.create(
            inventory=self.inventory2,
            start_date=timezone.datetime(2025, 3, 15, tzinfo=timezone.utc).date(),
            embargo_date=timezone.datetime(2025, 3, 25, tzinfo=timezone.utc).date(),
        )
        self.order2.tags.add(self.tag2)

        self.order3 = Order.objects.create(
            inventory=self.inventory1,
            start_date=timezone.datetime(2025, 4, 10, tzinfo=timezone.utc).date(),
            embargo_date=timezone.datetime(2025, 4, 20, tzinfo=timezone.utc).date(),
        )


    def test_filter_by_start_date(self):
        url = reverse('order-date-range')
        response = self.client.get(url, {'lookup_start_date': '2025-03-10'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) # order2 and order3

    def test_filter_by_embargo_date(self):
        url = reverse('order-date-range')
        response = self.client.get(url, {'lookup_embargo_date': '2025-03-30'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) # order2

    def test_filter_by_date_range(self):
        url = reverse('order-date-range')
        response = self.client.get(url, {'lookup_start_date': '2025-03-02', 'lookup_embargo_date': '2025-04-15'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) # order2

    def test_no_filter(self):
        url = reverse('order-date-range')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3) # All orders