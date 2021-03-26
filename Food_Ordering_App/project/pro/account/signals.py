from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, PasswordUpdation, DeliveryLocation
from django.contrib.auth.models import Group
from employee.models import Employer

@receiver(post_save,sender=User)
def passenger_profile(sender, instance, created, **kwargs):
	if created:
		password_obj=PasswordUpdation(user=instance)
		password_obj.save()
		try:
			group = Group.objects.get(name='customers')
		except:
			group=Group()
			group.name='customers'
			group.save()
		try:
			group = Group.objects.get(name='employee')
		except:
			group=Group()
			group.name='employee'
			group.save()
		try:
			group = Group.objects.get(name='sellers')
		except:
			group=Group()
			group.name='sellers'
			group.save()
		try:
			group = Group.objects.get(name='admins')
		except:
			group=Group()
			group.name='admins'
			group.save()
		if instance.is_superuser or instance.user_type == 'admins':
			group = Group.objects.get(name='admins')
		elif instance.user_type == 'employee':
			group = Group.objects.get(name='employee')
			employer = Employer(user=instance)
			employer.save()
		elif instance.user_type == 'sellers':
			group = Group.objects.get(name='sellers')
		else:
			group = Group.objects.get(name='customers')
			delivery_location=DeliveryLocation(user=instance,delivery_location=None)
			delivery_location.save()
		instance.groups.add(group)

