from django.urls import path
from .api import HotelRegisterApi,HotelListApi,HotelRetrieveApi,HotelUpdateApi,HotelDestroyApi,HotelSellerListApi,FoodRegisterApi,FoodRetrieveApi,FoodUpdateApi,FoodDestroyApi,FoodHotelListApi,HotelsNearMeApi,EmployerHotelOrdersApi


urlpatterns = [
    path('api/register/', HotelRegisterApi),
    path('api/hotels/',HotelListApi.as_view()),
    path('api/myhotels/',HotelSellerListApi.as_view()),
    path('api/hotels_near_me/',HotelsNearMeApi),
    path('api/hotel/<int:pk>/',HotelRetrieveApi.as_view()),
    path('api/hotel/update/<int:pk>/',HotelUpdateApi.as_view()),
    path('api/hotel/delete/<int:pk>/',HotelDestroyApi.as_view()),
    path('api/food/register/',FoodRegisterApi),
    path('api/food/<int:pk>/',FoodRetrieveApi.as_view()),
    path('api/food/update/<int:pk>/',FoodUpdateApi.as_view()),
    path('api/food/delete/<int:pk>/',FoodDestroyApi.as_view()),
    path('api/hotel/food/<int:pk>/',FoodHotelListApi),
    path('api/orders/hotel/<int:pk>/',EmployerHotelOrdersApi)
]

