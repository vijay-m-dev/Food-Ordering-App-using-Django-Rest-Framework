from rest_framework import serializers
from .models import Order, HotelOrdered, FoodOrdered, OrderedUser, DeliveryPerson, OrderStatus

class UserOrderSerializer(serializers.Serializer):
    food_id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(required=True,min_value=1)

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','total_cost','order_date_time','delivery_date_time']

class OrderHotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelOrdered
        exclude = ['order']

class OrderFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodOrdered
        exclude = ['order']

class OrderUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedUser
        exclude = ['order']

class OrderDeliveryPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryPerson
        exclude = ['order']

class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        exclude = ['order','rating']

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = OrderStatus
		fields = ['on_the_way','delivered']
		extra_kwargs = {'on_the_way':{'required':True},'delivered':{'required':True}}

class OrderRatingSerializer(serializers.ModelSerializer):
	class Meta:
		model = OrderStatus
		fields = ['rating']
		extra_kwargs = {'rating':{'required':True}}