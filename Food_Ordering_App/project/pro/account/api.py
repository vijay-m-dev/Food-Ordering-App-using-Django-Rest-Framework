from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import generics, permissions
from .serializer import RegisterSerializer, UserSerializer, OtpMailSerializer, UpdatePasswordOtpMailSerializer, LocationSerializer1, LocationSerializer2
from django.core.mail import EmailMessage
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from .models import User,Location
from employee.serializer import EmployerSerializer3
from .permissions import IsCustomer
import pyotp,base64
from datetime import datetime
import pygeoip

class RegisterApi(generics.GenericAPIView):
	permission_classes = (AllowAny,)
	serializer_class = RegisterSerializer
	def post(self, request, *args,  **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User created successfully.",
        })


def generateKey(reset,counter):
		return reset+str(datetime.now())+"qpwoei2892dhddjcjwcwj"+str(counter)

@api_view(['GET','POST','PUT'])
def ResetPasswordEmailApi(request,email):
	if request.method=='GET':
		user=User.objects.filter(email=email)
		if user:
			user=user[0]
			user.passwordupdation.reset_counter+=1
			user.passwordupdation.save()
			secret_key=generateKey(email,user.passwordupdation.reset_counter).encode()
			otp=pyotp.HOTP(base64.b32encode(secret_key))
			otp_digit=otp.at(user.passwordupdation.reset_counter)
			user.passwordupdation.secret_key=secret_key
			user.passwordupdation.last_otp_datetime=datetime.now()
			user.passwordupdation.otp_accepted=False
			user.passwordupdation.password_update=False
			user.passwordupdation.otp_sent=True
			user.passwordupdation.save()
			email_obj = EmailMessage('Food Ordering App - OTP for reset password request: ',"OTP is:"+str(otp_digit),settings.EMAIL_HOST_USER,[email])
			email_obj.fail_silently=False
			email_obj.send()
			return Response({"message": "OTP is sent to email",})
		else:
			return Response({"message": "account does not exist",})
	elif request.method=='POST':
		user=User.objects.filter(email=email)
		if user:
			user=user[0]
			serializer=OtpMailSerializer(data=request.data)
			if serializer.is_valid() and user.passwordupdation.otp_sent==True:
				if (datetime.now()-user.passwordupdation.last_otp_datetime.replace(tzinfo=None)).total_seconds()<90:
					otp=pyotp.HOTP(base64.b32encode(user.passwordupdation.secret_key))
					if otp.verify(request.data["otp"],user.passwordupdation.reset_counter):
						user.passwordupdation.otp_accepted=True
						user.passwordupdation.save()
						return Response({"message": "OTP received is correct",})
					else:
						return Response({"message": "OTP received is incorrect",})
				else:
					return Response({"message": "OTP expired",})
			else:
				return Response({"message": "Error",})
		else:
			return Response({"message": "Error",})
	elif request.method=='PUT':
		user=User.objects.filter(email=email)
		if user:
			user=user[0]
			serializer=UpdatePasswordOtpMailSerializer(data=request.data)
			serializer.is_valid(raise_exception=True)
			if user.passwordupdation.otp_accepted==True:
				if (datetime.now()-user.passwordupdation.last_otp_datetime.replace(tzinfo=None)).total_seconds()<90:
					otp=pyotp.HOTP(base64.b32encode(user.passwordupdation.secret_key))
					if otp.verify(request.data["otp"],user.passwordupdation.reset_counter):
						user.passwordupdation.secret_key=None
						user.passwordupdation.otp_sent=False
						user.passwordupdation.otp_accepted=False
						user.passwordupdation.save()
						user.set_password(serializer.validated_data['password'])
						user.save()
						return Response({"message": "Password Updated",})
					else:
						return Response({"message": "OTP is incorrect",})
				else:
					return Response({"message": "OTP expired",})				
			else:
				return Response({"message": "send otp first",})
		else:
			return Response({"message": "Error",})

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def LocationIpApi(request,ip):
	if request.method=='POST':
		gip=pygeoip.GeoIP('GeoLiteCity.dat')
		res=gip.record_by_addr(ip)
		if res and res['latitude']!=None and res['longitude']!=None:
			d={'latitude':None,'longitude':None,'city':None,'country_name':None}
			for key in d:
				if res[key]!=None:
					d[key]=res[key]
			if request.user.groups.filter(name='customers').exists():
				location=Location(user=request.user,latitude=d['latitude'],longitude=d['longitude'],city=d['city'].lower(),country=d['country_name'].lower())
				location.save()
				deliverylocation=request.user.deliverylocation
				deliverylocation.delivery_location=location
				deliverylocation.save()
			elif request.user.groups.filter(name='employee').exists():
				employer_obj=request.user.employer
				employer_obj.latitude=d['latitude']
				employer_obj.longitude=d['longitude']
				employer_obj.city=d['city'].lower()
				employer_obj.country=d['country_name'].lower()
				employer_obj.save()
			else:
				return Response({"message":"Error"})
			return Response({"message":"Location Updated"})
		return Response({"message": "Ip address doesn't exist in database Please try to give latitude and longitude to set location"})

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def ProfileApi(request):
	if request.method == 'GET':
		user=request.user
		serializer1=UserSerializer(user)
		if user.user_type!='employee':
			return Response({
            "user": serializer1.data
        })
		else:
			employer=user.employer
			serializer2=EmployerSerializer3(employer)
			return Response({
            "user": serializer1.data,
            "employee": serializer2.data
        })

@api_view(['POST','GET'])
@permission_classes([permissions.IsAuthenticated,IsCustomer])
def LocationApi(request):
	user=request.user
	if request.method == 'POST':
		request.data['user']=user.id
		serializer=LocationSerializer1(data=request.data)
		serializer.is_valid(raise_exception=True)
		location=serializer.save()
		user.deliverylocation.delivery_location=location
		user.deliverylocation.save()
		return Response({"message":"Location Set"})
	elif request.method == 'GET':
		if user.deliverylocation.delivery_location!=None:
			serializer=LocationSerializer2(user.deliverylocation.delivery_location)
			return Response({"delivery_location":serializer.data})
		else:
			return Response({"message":"Location not set"})

@api_view(['PUT',])
@permission_classes([permissions.IsAuthenticated,IsCustomer])
def LocationUpdateApi(request,pk):
	if request.method=='PUT':
		location=Location.objects.filter(id=pk)
		if location:
			if location[0].user.id==request.user.id:
				deliverylocation_obj=request.user.deliverylocation
				deliverylocation_obj.delivery_location=location[0]
				deliverylocation_obj.save()
				return Response({"message":"Delivery Location Updated"})
			else:
				return Response({"message":"You are not authorized"})
		else:
			return Response({"message":"location does not exist"})

class LocationListApi(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated,IsCustomer]
    serializer_class = LocationSerializer2
    def get_queryset(self):
    	return self.request.user.location_set.all()