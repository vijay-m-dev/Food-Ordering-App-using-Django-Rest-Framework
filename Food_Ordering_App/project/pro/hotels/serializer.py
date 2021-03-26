from rest_framework import serializers
from .models import Hotel, Food

class HotelRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields="__all__"

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        exclude = ['user_id']

class FoodRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields="__all__"

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        exclude = ['hotel']
