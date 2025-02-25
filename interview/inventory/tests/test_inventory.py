from datetime import datetime, timezone, timedelta

from rest_framework.test import APITestCase
from django.urls import reverse


class TestInventoryListGetItemsView(APITestCase):
    @staticmethod
    def assert_inventory_items_equal(item_data, inventory_item):
        assert item_data['id'] == inventory_item.id
        assert item_data['name'] == inventory_item.name
        assert item_data['type'] == inventory_item.type.id
        assert item_data['language'] == inventory_item.language.id
        assert item_data['tags'] == [inventory_tag.id for inventory_tag in inventory_item.tags.all()]
        assert item_data['metadata'] == inventory_item.metadata

    def test_get_inventory_items_created_after_valid_date(self, api_client, inventory_items):
        created_after_date = datetime.now(timezone.utc) - timedelta(days=1.5) # Date between item1 and item2/item3 creation

        url = reverse('inventory-items-created-after') # Assuming you named your url 'inventory-items-created-after'
        response = api_client.get(url, {'created_after': created_after_date.isoformat()})

        assert response.status_code == 200
        data = response.json()

        assert len(data) == 2 # Expecting item2 and item3
        self.assert_inventory_items_equal(data[0], inventory_items[1]) # item2
        self.assert_inventory_items_equal(data[1], inventory_items[2]) # item3