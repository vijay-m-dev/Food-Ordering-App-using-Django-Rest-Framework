from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, permissions
from .serializer import HotelRegisterSerializer, FoodRegisterSerializer, HotelSerializer, FoodSerializer
from rest_framework.response import Response
from account.permissions import IsSeller, IsSellerHotelObject, IsSellerFoodObject, IsCustomer
from .models import Hotel, Food
from math import sin,cos,sqrt,atan2,radians
from django.shortcuts import get_object_or_404
from orders.api import order_details,distance_lat_lon
from decimal import Decimal


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated,IsSeller])
def HotelRegisterApi(request):
	if request.method == 'POST':
		request.data['user_id']=request.user.id
		serializer=HotelRegisterSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user=serializer.save()
		return Response({"message": "Hotel created successfully",})

class HotelListApi(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Hotel.objects.all()
    serializer_class = HotelRegisterSerializer

class HotelDestroyApi(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated,IsSellerHotelObject]
    queryset = Hotel.objects.all()

class HotelUpdateApi(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated,IsSellerHotelObject]
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

class HotelRetrieveApi(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Hotel.objects.all()
    serializer_class = HotelRegisterSerializer

class HotelSellerListApi(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated,IsSeller]
    serializer_class = HotelRegisterSerializer
    def get_queryset(self):
    	return self.request.user.hotel_set.all()

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated,IsSeller])
def FoodRegisterApi(request):
	if request.method == 'POST':
		serializer=FoodRegisterSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		if serializer.validated_data['hotel'] in request.user.hotel_set.all():
			user=serializer.save()
			return Response({"message": "Food added successfully",})
		else:
			return Response({"message": "Not authorised",})

class FoodUpdateApi(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated,IsSellerFoodObject]
    queryset = Food.objects.all()
    serializer_class = FoodRegisterSerializer

class FoodDestroyApi(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated,IsSellerFoodObject]
    queryset = Food.objects.all()

class FoodRetrieveApi(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Food.objects.all()
    serializer_class = FoodRegisterSerializer

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def FoodHotelListApi(request,pk):
	if request.method == 'GET':
		hotel=Hotel.objects.filter(id=pk)
		if hotel:
			foods=hotel[0].food_set.all()
			serializer=FoodSerializer(foods,many=True)
			return Response(serializer.data)
		else:
			return Response({"message": "Hotel does not exist",})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated,IsCustomer])
def HotelsNearMeApi(request):
	if request.method == 'GET':
		delivery_location=request.user.deliverylocation.delivery_location
		if delivery_location==None:
			return Response({"message":"Please set the delivery location"})
		lat=delivery_location.latitude
		lon=delivery_location.longitude
		dif=Decimal(0.18)
		lat1=lat-dif
		lat2=lat+dif
		lon1=lon-dif
		lon2=lon+dif
		hotels=Hotel.objects.filter(latitude__gte=lat1,latitude__lte=lat2,longitude__gte=lon1,longitude__lte=lon2,available=True)
		hotels_nearby=[]
		for hotel in hotels:
			dis=distance_lat_lon(hotel.latitude,delivery_location.latitude,hotel.longitude,delivery_location.longitude)
			if dis<=6.0:
				hotels_nearby.append(hotel)
		serializer=HotelSerializer(hotels_nearby,many=True)
		return Response({"hotels":serializer.data})

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated,IsSeller])
def EmployerHotelOrdersApi(request,pk):
	if request.method == 'GET':
		hotel_obj=get_object_or_404(Hotel,pk=pk)
		if hotel_obj in request.user.hotel_set.all():
			orders_list=hotel_obj.order_set.all()
			details={}
			for i in range(len(orders_list)):
				order=orders_list[i]
				details["order"+str(i+1)]=order_details(order)
			return Response({"message":"orders","details":details})
		else:
			return Response({"message":"You are not authorized"})

