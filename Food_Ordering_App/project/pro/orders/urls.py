from django.urls import path
from .api import OrderApi, SingleOrderApi, OrderStatusUpdateApi, OrderRatingApi


urlpatterns = [
    path('api/order/', OrderApi),
    path('api/order/<int:pk>/', SingleOrderApi),
    path('api/order_status/update/<int:pk>/',OrderStatusUpdateApi),
    path('api/order_rating/update/<int:pk>/',OrderRatingApi)
]

