
from django.urls import path
from interview.order.views import OrderListCreateView, OrderTagListCreateView, OrderUpdateView


urlpatterns = [
    path('tags/', OrderTagListCreateView.as_view(), name='order-detail'),
    path('update/<int:pk>', OrderUpdateView.as_view(), name='order-update'),
    path('', OrderListCreateView.as_view(), name='order-list'),

]