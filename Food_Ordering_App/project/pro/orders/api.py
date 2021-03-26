from rest_framework.decorators import api_view, permission_classes
from .serializer import UserOrderSerializer, OrderSerializer, OrderHotelSerializer, OrderFoodSerializer, OrderUserSerializer, OrderDeliveryPersonSerializer, OrderStatusSerializer, OrderStatusUpdateSerializer, OrderRatingSerializer
from rest_framework.response import Response
from rest_framework import permissions
from account.permissions import IsCustomer, IsEmployer
from hotels.models import Food,Hotel
from employee.models import Employer
from .models import Order, HotelOrdered, FoodOrdered, OrderedUser, DeliveryPerson, OrderStatus
from django.shortcuts import get_object_or_404
import datetime
from decimal import Decimal
from math import radians,sin,cos,atan2,sqrt

#Used to calculate food cost with offer
def cost_with_offer(obj,quantity):
	offer=float(obj.offer)
	cost=float(obj.cost)
	cost=cost-((cost)*(offer/100.0))
	cost=round(cost*quantity)
	return cost

#Used to find the distance between two locations
def distance_lat_lon(lat1,lat2,lon1,lon2):
	r=6373.0
	lat1=radians(lat1)
	lat2=radians(lat2)
	lon1=radians(lon1)
	lon2=radians(lon2)
	dlat=lat2-lat1
	dlon=lon2-lon1
	a=sin(dlat/2)**2+cos(lat1)*cos(lat2)*sin(dlon/2)**2
	c=2*atan2(sqrt(a),sqrt(1-a))
	d=r*c
	return d

#Used to serialize the order details
def order_details(order):
	foodordered=order.foodordered_set.all()
	userordered=order.ordereduser
	hotelordered=order.hotelordered
	deliveryperson=order.deliveryperson
	orderstatus=order.orderstatus
	order_serializer=OrderSerializer(order)
	user_serializer=OrderUserSerializer(userordered)
	hotel_serializer=OrderHotelSerializer(hotelordered)
	deliver_serializer=OrderDeliveryPersonSerializer(deliveryperson)
	food_serializer=OrderFoodSerializer(foodordered,many=True)
	status_serializer=OrderStatusSerializer(orderstatus)
	details={"order":order_serializer.data,
			"user":user_serializer.data,
			"hotel":hotel_serializer.data,
			"food":food_serializer.data,
			"delivery_person":deliver_serializer.data,
			"status":status_serializer.data}
	return details


@api_view(['POST','GET'])
@permission_classes([permissions.IsAuthenticated,IsCustomer])
def OrderApi(request):
	if request.method == 'POST':
		delivery_location=request.user.deliverylocation.delivery_location
		if delivery_location==None:
			return Response({"message":"Please set the delivery location"})
		serializer=UserOrderSerializer(data=request.data,many=True)
		serializer.is_valid(raise_exception=True)
		orders=serializer.data
		hotels=[]
		food_objs=[]
		total_cost=0
		for food in orders:
			food_dict=dict(food)
			food_obj=get_object_or_404(Food,pk=food_dict['food_id'])
			if food_obj.available==False:
				{"message":"Food is not available","food_name":food_obj.name}
			cost=cost_with_offer(food_obj,food_dict['quantity'])
			total_cost+=cost
			food_objs.append([food_obj,food_dict['quantity'],cost])
			hotels.append(food_obj.hotel.id)
		hotels=set(hotels)
		#checking whether the order is one hotel or multiple hotels
		if len(hotels)!=1:
			return Response({"message":"You cannot order food from different hotels"})
		hotel_obj=get_object_or_404(Hotel,pk=list(hotels)[0])
		distance_hotel_to_delivery=distance_lat_lon(hotel_obj.latitude,delivery_location.latitude,hotel_obj.longitude,delivery_location.longitude)
		#checking the hotel is 20km greater than delivery location
		if distance_hotel_to_delivery>20.0:
			return Response({"message":"Hotel is too far from delivery location","hotel_name":hotel_obj.name})
		#checking for the availability of hotel
		if hotel_obj.available==False:
			return Response({"message":"Hotel is not available","hotel_name":hotel_obj.name})
		lat=hotel_obj.latitude
		lon=hotel_obj.longitude
		#diff is latitude and longitude difference. 0.1 degree = 11.1km
		dif=Decimal(0.1)
		lat1=lat-dif
		lat2=lat+dif
		lon1=lon-dif
		lon2=lon+dif
		employee_objs=Employer.objects.filter(latitude__gte=lat1,latitude__lte=lat2,longitude__gte=lon1,longitude__lte=lon2,available=True,order_taken=False)
		if not employee_objs:
			return Response({"message":"Your order is valid. But, there is no delivery person available nearby. Please try after some time"})
		employee_available=[]
		for employer in employee_objs:
			distance_employer_to_hotel=distance_lat_lon(employer.latitude,hotel_obj.latitude,employer.longitude,hotel_obj.longitude)
			#checking for the delivery person is within 10km near to the hotel
			if distance_employer_to_hotel<=10.0:
				employee_available.append([distance_employer_to_hotel,employer])
		#sorting delivery persons based on the distance from hotel
		sorted_employee_available=sorted(employee_available,key=lambda x:x[0])
		#getting delivery person nearer to hotel
		delivery_person=sorted_employee_available[0][1]
		delivery_person.order_taken=True
		delivery_person.save()
		#getting distance of employer to hotel
		distance_employer_to_hotel=sorted_employee_available[0][0]
		delivery_minutes=round((distance_employer_to_hotel+distance_hotel_to_delivery)*8+10)
		order=Order(user=request.user,hotel=hotel_obj,delivery_guy=delivery_person,total_cost=round(total_cost))
		order.save()
		for food_obj in food_objs:
			order.food.add(food_obj[0])
		delivery_datetime=order.order_date_time+datetime.timedelta(minutes=delivery_minutes)
		order.delivery_date_time=delivery_datetime
		order.save()
		hotelordered=HotelOrdered(order=order,name=hotel_obj.name,latitude=hotel_obj.latitude,longitude=hotel_obj.longitude,street=hotel_obj.street,area=hotel_obj.area,city=hotel_obj.city,state=hotel_obj.state,country=hotel_obj.country)
		hotelordered.save()
		userordered=OrderedUser(order=order,user_id=request.user.id,name=request.user.username,email=request.user.email,mobile_no=request.user.mobile_no)
		userordered.save()
		deliveryperson=DeliveryPerson(order=order,employer_id=delivery_person.user.id,name=delivery_person.user.username,email=delivery_person.user.email,mobile_no=delivery_person.user.mobile_no)
		deliveryperson.save()
		food_ordered=[]
		for food_obj in food_objs:
			food=food_obj[0]
			food_quantity=food_obj[1]
			food_cost=food_obj[2]
			foodordered=FoodOrdered(order=order,name=food.name,cost=food.cost,offer=food.offer,quantity=food_quantity,total_cost=food_cost,major_category=food.major_category,minor_category=food.minor_category)
			foodordered.save()
			food_ordered.append(foodordered)
		orderstatus=OrderStatus(order=order,order_taken=True,on_the_way=False,delivered=False)
		orderstatus.save()
		return Response({"message":"Order is successfully made",
			 "order_details":order_details(order)})
	if request.method == 'GET':
		orders_list=request.user.order_set.all()
		details={}
		for i in range(len(orders_list)):
			order=orders_list[i]
			details["order"+str(i+1)]=order_details(order)
		return Response({"message":"Your Orders",
			"orders":details})

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated,IsCustomer])
def SingleOrderApi(request,pk):
	if request.method == "GET":
		order=get_object_or_404(Order,pk=pk)
		if order.user.id==request.user.id:
			details=order_details(order)
			return Response({"order_details":details})
		else:
			return Response({"message":"You are not authorized"})

@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated,IsEmployer])
def OrderStatusUpdateApi(request,pk):
	order=get_object_or_404(Order,pk=pk)
	if request.method == 'PUT':
		if order in request.user.employer.order_set.all():
			serializer=OrderStatusUpdateSerializer(data=request.data)
			serializer.is_valid(raise_exception=True)
			orderstatus=order.orderstatus
			orderstatus.on_the_way=serializer.validated_data['on_the_way']
			orderstatus.delivered=serializer.validated_data['delivered']
			if serializer.validated_data['delivered']==True:
				order.delivery_guy.order_taken=False
				order.delivery_guy.save()
			orderstatus.save()
			return Response({"message":"Status Updated"})

@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated,IsCustomer])
def OrderRatingApi(request,pk):
	if request.method == "PUT":
		order=get_object_or_404(Order,pk=pk)
		if order.user.id==request.user.id:
			serializer=OrderRatingSerializer(data=request.data)
			serializer.is_valid(raise_exception=True)
			orderstatus=order.orderstatus
			if orderstatus.delivered==False:
				return Response({"message":"Please rate after delivered"})
			orderstatus.rating=serializer.validated_data['rating']
			orderstatus.save()
			return Response({"message":"Thank you for your rating"})
		else:
			return Response({"message":"You are not authorized"})