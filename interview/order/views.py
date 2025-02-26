from django.shortcuts import render, get_object_or_404
from django.views import View
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer

# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    

class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer


class OrderUpdateView(generics.UpdateAPIView): # Changed base class to generics.UpdateAPIView
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'pk' # Important to specify lookup_field as 'pk' to match <int:pk> in URL

    def patch(self, request, pk=None): # Removed @api_view and corrected method signature
        instance = self.get_object() # get_object() is now available from generics.UpdateAPIView

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        is_active_from_serializer = serializer.validated_data.get('is_active')

        if is_active_from_serializer is not None:
            if is_active_from_serializer is False and not instance.is_active:
                return Response({"message": "Order is already deactivated."}, status=status.HTTP_400_BAD_REQUEST)
            if is_active_from_serializer is True and instance.is_active:
                return Response({"message": "Order is already activated."}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer) # Use perform_update for saving

        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer): # Override perform_update to use serializer.save()
        serializer.save()
