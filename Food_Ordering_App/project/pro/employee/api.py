from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Employer
from account.permissions import IsAdmin, IsEmployerObject, IsEmployer
from .serializer import EmployerSerializer1, EmployerSerializer2, EmployerSerializer3
from orders.api import order_details

class EmployerUpdateApi(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated,IsAdmin]
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer1

@api_view(['PUT','GET'])
@permission_classes([permissions.IsAuthenticated,IsEmployer])
def EmployerLocationApi(request):
	employer=request.user.employer
	if request.method == 'GET':
		serializer=EmployerSerializer2(employer)
		return Response(serializer.data)
	elif request.method == 'PUT':
		serializer=EmployerSerializer2(data=request.data)
		serializer.is_valid(raise_exception=True)
		employer.latitude=serializer.validated_data['latitude']
		employer.longitude=serializer.validated_data['longitude']
		employer.save()
		return Response({"message":"location updated"})

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated,IsEmployer])
def EmployerOrdersApi(request):
	if request.method == 'GET':
		orders_list=request.user.employer.order_set.all()
		details={}
		for i in range(len(orders_list)):
			order=orders_list[i]
			details["order"+str(i+1)]=order_details(order)
	return Response({"message":"Your Assigned Orders","orders":details})



