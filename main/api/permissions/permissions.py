from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return  request.user and request.user.is_authenticated
    
    message = "You must be the owner of this product."
    def has_object_permission(self, request, view, obj):
        return (obj.user == request.user) or request.user.is_superuser

class NotAuthenticated(BasePermission):
    message = "You already have an account"
    def has_permission(self,request, view):
        return not request.user.is_authenticated

        #return (obj.user == request.user) or request.user.is_staff
        #if admin panel registration permission 
        #Allow Any -- Everyone
        #IsAuthenticated -- Aktif User 
        #IsAdminUser -- Is Staff 
#class IsOWnerReadOnly(BasePermission):
#    def has_object_permission(self, request, view, obj):
#        if request.method in permissions.SAFE_METHODS:
#            return True
#        return obj.owner == request.user

