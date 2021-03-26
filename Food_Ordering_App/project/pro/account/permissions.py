from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
	message="You must be Admin"
	def has_permission(self, request, view):
		return request.user.groups.filter(name='admins').exists()

class IsSeller(permissions.BasePermission):
	message="You must be seller person"
	def has_permission(self, request, view):
		return request.user.groups.filter(name='sellers').exists()

class IsCustomer(permissions.BasePermission):
	message="You must be customer"
	def has_permission(self, request, view):
		return request.user.groups.filter(name='customers').exists()

class IsEmployer(permissions.BasePermission):
	message="You must be employer"
	def has_permission(self, request, view):
		return request.user.groups.filter(name='employee').exists()

class IsEmployerObject(permissions.BasePermission):
	message="You are not authorized"
	def has_object_permission(self, request, view, obj):
		return obj and obj.user.id==request.user.id

class IsSellerHotelObject(permissions.BasePermission):
	message="You are not authorised"
	def has_object_permission(self,request,view,obj):
		return obj and obj.user_id.id==request.user.id

class IsSellerFoodObject(permissions.BasePermission):
	message="You are not authorised"
	def has_object_permission(self,request,view,obj):
		return obj and obj.hotel.user_id.id==request.user.id