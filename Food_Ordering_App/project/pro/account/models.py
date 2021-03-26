from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager
from django.core.validators import RegexValidator
from django.conf import settings


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    mobile_no = models.CharField(_('mobile no'),validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$',message="Phone no must be enter in the format: +999999999. upto 15 digits")],max_length=17, unique=True)
    username = models.CharField(_('username'), max_length=30)
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)
    user_type = models.CharField(_('user type'),max_length=10)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=True)
    is_superuser = models.BooleanField(_('superuser'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','mobile_no','user_type']

    def __str__(self):
        return self.email


class PasswordUpdation(models.Model):
    reset_counter = models.IntegerField(_('reset counter'), default=0)
    secret_key = models.BinaryField(_('secret key'), null=True)
    otp_sent = models.BooleanField(_('otp sent'), default=False)
    otp_accepted = models.BooleanField(_('otp accepted'), default=False)
    last_otp_datetime =  models.DateTimeField(_('last otp grnerated'), null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)


class Location(models.Model):
    latitude=models.DecimalField(_('latitude'),max_digits=22, decimal_places=16)
    longitude=models.DecimalField(_('longitude'),max_digits=22, decimal_places=16)
    area = models.CharField(_('area name'), max_length=60,default='')
    city = models.CharField(_('city name'), max_length=60,default='')
    state = models.CharField(_('state name'), max_length=60,default='')
    country = models.CharField(_('country name'), max_length=60,default='')
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

class DeliveryLocation(models.Model):
    delivery_location=models.ForeignKey(Location,on_delete=models.SET_NULL,null=True)
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

