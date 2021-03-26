from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator

# Create your models here.
class Employer(models.Model):
	user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	latitude = models.DecimalField(_('latitude'), max_digits=22, decimal_places=16, null=True)
	longitude = models.DecimalField(_('latitude'), max_digits=22, decimal_places=16, null=True)
	available = models.BooleanField(_('available'), default=False)
	order_taken = models.BooleanField(_('order taken'), default=False)
	area = models.CharField(_('area name'), max_length=60,default='')
	city = models.CharField(_('city name'), max_length=60,default='')
	state = models.CharField(_('state name'), max_length=60,default='')
	country = models.CharField(_('country name'), max_length=60,default='')
	


