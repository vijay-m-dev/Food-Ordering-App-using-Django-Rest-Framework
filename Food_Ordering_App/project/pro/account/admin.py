from django.contrib import admin
from .models import User,PasswordUpdation,Location,DeliveryLocation
# Register your models here.
admin.site.register(User)
admin.site.register(PasswordUpdation)
admin.site.register(Location)
admin.site.register(DeliveryLocation)