from django.urls import path
from .api import EmployerUpdateApi, EmployerLocationApi, EmployerOrdersApi


urlpatterns = [
    path('api/update/<int:pk>/', EmployerUpdateApi.as_view()),
    path('api/location/',EmployerLocationApi),
    path('api/orders/',EmployerOrdersApi)
]

