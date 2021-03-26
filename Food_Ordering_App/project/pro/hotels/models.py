from django.db import models
from django.utils.translation import ugettext_lazy as _
from account.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.conf import settings

# Create your models here.
class Hotel(models.Model):
	user_id = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	name = models.CharField(_('name'), max_length=60)
	latitude = models.DecimalField(_('latitude'), max_digits=22, decimal_places=16)
	longitude = models.DecimalField(_('latitude'), max_digits=22, decimal_places=16)
	available = models.BooleanField(_('available'), default=True)
	street = models.CharField(_('street name'), max_length=60, default='')
	area = models.CharField(_('area name'), max_length=60, default='')
	city = models.CharField(_('city name'), max_length=60,default='')
	state = models.CharField(_('state name'), max_length=60, default='')
	country = models.CharField(_('country name'), max_length=60,default='')

class Food(models.Model):
	name = models.CharField(_('name'), max_length=60)
	available = models.BooleanField(_('available'))
	cost = models.DecimalField(_('cost'), max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.0'))])
	offer = models.IntegerField(_('offer'),validators=[MinValueValidator(0)])
	major_category = models.CharField(_('major category'), max_length=60)
	minor_category = models.CharField(_('minor category'), max_length=60)
	hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE)
