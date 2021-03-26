from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .api import RegisterApi,ResetPasswordEmailApi,ProfileApi,LocationApi,LocationUpdateApi,LocationListApi, LocationIpApi


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterApi.as_view()),
    path('api/reset-password-email/<str:email>/',ResetPasswordEmailApi),
    path('api/profile/',ProfileApi),
    path('api/delivery_location_list/',LocationListApi.as_view()),
    path('api/delivery_location/',LocationApi),
    path('api/delivery_location/update/<int:pk>/',LocationUpdateApi),
    path('api/locationIp/<str:ip>/',LocationIpApi)
]

