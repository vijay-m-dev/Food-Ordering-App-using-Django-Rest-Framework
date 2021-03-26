from rest_framework import serializers
from .models import Employer

class EmployerSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = ['area','city','state','country','available']

class EmployerSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = ['latitude','longitude']
        extra_kwargs = {'latitude':{'required':True},'longitude':{'required':True}}

class EmployerSerializer3(serializers.ModelSerializer):
	class Meta:
		model = Employer
		exclude = ['user']