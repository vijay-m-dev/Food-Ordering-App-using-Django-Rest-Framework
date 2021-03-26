from django.db import models
from account.models import User
from hotels.models import Hotel,Food
from employee.models import Employer
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator,MaxValueValidator,RegexValidator
from decimal import Decimal
from django.conf import settings

# Create your models here.



class Order(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
	hotel=models.ForeignKey(Hotel,on_delete=models.SET_NULL, null=True)
	food=models.ManyToManyField(Food)
	delivery_guy=models.ForeignKey(Employer,on_delete=models.CASCADE)
	total_cost=models.DecimalField(_('cost'),max_digits=12,decimal_places=2, validators=[MinValueValidator(Decimal('0.0'))])
	order_date_time=models.DateTimeField(_('order date time'), auto_now_add=True)
	delivery_date_time = models.DateTimeField(_('order date time'), default=None,null=True)

class OrderStatus(models.Model):
	order = models.OneToOneField(Order,on_delete=models.CASCADE)
	order_taken = models.BooleanField(_('on the way'), default=False)
	on_the_way = models.BooleanField(_('on the way'), default=False)
	delivered = models.BooleanField(_('food delivered'), default=False)
	rating = models.IntegerField(_('rating'), default=4,validators=[MinValueValidator(0),MaxValueValidator(5)])

class HotelOrdered(models.Model):
	order = models.OneToOneField(Order,on_delete=models.CASCADE)
	name = models.CharField(_('name'), max_length=60)
	latitude = models.DecimalField(_('latitude'), max_digits=22, decimal_places=16)
	longitude = models.DecimalField(_('latitude'), max_digits=22, decimal_places=16)
	street = models.CharField(_('street name'), max_length=60,default='')
	area = models.CharField(_('area name'), max_length=60,default='')
	city = models.CharField(_('city name'), max_length=60,default='')
	state = models.CharField(_('state name'), max_length=60,default='')
	country = models.CharField(_('country name'), max_length=60,default='')

class FoodOrdered(models.Model):
	order = models.ForeignKey(Order,on_delete=models.CASCADE)
	name = models.CharField(_('name'), max_length=60)
	cost = models.DecimalField(_('cost'), max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.0'))])
	offer = models.IntegerField(_('offer'), validators=[MinValueValidator(0)])
	quantity = models.IntegerField(_('quantity'), validators=[MinValueValidator(1)])
	total_cost = models.IntegerField(_('total cost'), validators=[MinValueValidator(1)])
	major_category = models.CharField(_('major category'), max_length=60)
	minor_category = models.CharField(_('minor category'), max_length=60)

class OrderedUser(models.Model):
	order = models.OneToOneField(Order,on_delete=models.CASCADE)
	user_id = models.IntegerField(_('user id'),default=None)
	name = name = models.CharField(_('name'), max_length=60)
	email = models.EmailField(_('email address'))
	mobile_no = models.CharField(_('mobile no'),max_length=17,validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$',message="Phone no must be enter in the format: +999999999. upto 15 digits")])

class DeliveryPerson(models.Model):
	order = models.OneToOneField(Order,on_delete=models.CASCADE)
	employer_id = models.IntegerField(_('employer id'),default=None)
	name = name = models.CharField(_('name'), max_length=60)
	email = models.EmailField(_('email address'))
	mobile_no = models.CharField(_('mobile no'),max_length=17,validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$',message="Phone no must be enter in the format: +999999999. upto 15 digits")])
