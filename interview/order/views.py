from django.db.models import Q
from rest_framework import generics

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer

# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    

class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer


class OrderDateRangeListView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.all()
        lookup_start_date = self.request.query_params.get('lookup_start_date')
        lookup_embargo_date = self.request.query_params.get('lookup_embargo_date')


        if lookup_start_date and lookup_embargo_date:
            queryset = queryset.filter(
                Q(start_date__gte=lookup_start_date) & Q(embargo_date__lte=lookup_embargo_date)
            )
        elif lookup_start_date: # Only lookup start date is provided
            queryset = queryset.filter(start_date__gte=lookup_start_date)
        elif lookup_embargo_date: # Only lookup embargo date is provided
             queryset = queryset.filter(embargo_date__lte=lookup_embargo_date)

        return queryset