from django.contrib import admin
from .models import Order,HotelOrdered,FoodOrdered,OrderedUser,DeliveryPerson,OrderStatus
# Register your models here.
admin.site.register(Order)
admin.site.register(HotelOrdered)
admin.site.register(FoodOrdered)
admin.site.register(OrderedUser)
admin.site.register(DeliveryPerson)
admin.site.register(OrderStatus)