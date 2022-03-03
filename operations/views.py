from accounts.views import AuthenticateView
from . import serializers
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

from rest_framework.permissions import IsAuthenticated
from accounts.permissions import SuperuserPermissionOnly, CreatePermissionOnly
from operations.models import (Customer, Errander)

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

User= get_user_model()

# generate password for user
def generate_password():
    characters= "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXWZ1234567890"
    password= User.objects.make_random_password(length=10, allowed_chars=characters)
    return password



# Customer views
# Create and List Customer View
class CustomerCreateListView(CreateModelMixin, ListAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    serializer_class= serializers.CustomerCreateSerializer
    permission_classes= [] #[IsAuthenticated&SuperuserPermissionOnly]
    queryset= Customer.objects.all()
    search_fields= ('user_email', 'user_first_name', 'user_last_name')

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class CustomerDetailView(UpdateModelMixin, DestroyModelMixin, RetrieveAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    serializer_class= serializers.CustomerUpdateSerializer
    permission_classes= [] #[IsAuthenticated&SuperuserPermissionOnly]
    queryset= Customer.objects.all()
    lookup_field= 'id'
    search_fields= ('user_email', 'user_first_name', 'user_last_name')

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ErranderCreateListView(CreateModelMixin, ListAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    serializer_class= serializers.ErranderCreateSerializer
    permission_classes= [] #[IsAuthenticated&SuperuserPermissionOnly]
    queryset= Errander.objects.all()
    search_fields= ('user_email', 'user_first_name', 'user_last_name')

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ErranderDetailView(UpdateModelMixin, DestroyModelMixin, RetrieveAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    serializer_class= serializers.ErranderUpdateSerializer
    permission_classes= [] #[IsAuthenticated&SuperuserPermissionOnly]
    queryset= Errander.objects.all()
    lookup_field= 'id'
    search_fields= ('user_email', 'user_first_name', 'user_last_name')

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ErranderVerifyView(APIView):
    permission_classes= [] #[IsAuthenticated&SuperuserPermissionOnly]
    authentication_classes= []

    def put(self, request, *args, **kwargs):
        id= kwargs.get('id', None)   
        try:
            errander_obj= Errander.objects.get(id=id)
            user= errander_obj.user
            if not user.has_usable_password():
                password= generate_password() #generate password for user   
                user.set_password(password)
                
                #Send password via email
                try:
                    subject= 'Account verified successfully'
                    message= f'Email: {user.email}, \nPassword: {password}'
                    from_email= settings.EMAIL_HOST_USER
                    recipient_list= [user.email]
                    fail_silently=False
                    send_mail(
                        subject,
                        message,
                        from_email,
                        recipient_list,
                        fail_silently,
                    )
                    errander_obj.is_verified= True
                    errander_obj.is_declined= False
                    user.save()
                    errander_obj.save()
                    return Response({"detail": "Email sent successfully"}, status=200)
                except:
                    user.set_unusable_password()
                    user.save()
                    errander_obj.save()
                    return Response({"details":"Email not sent"}, status=501)
            else:
                return Response({"detail":"User already verified"}, status=208)
        except:
            return Response({"detail":"User with this id does not exist"}, status=404)

class ErranderDeclineView(APIView):
    permission_classes= [] #[IsAuthenticated&SuperuserPermissionOnly]
    authentication_classes= []

    def put(self, request, *args, **kwargs):
        id= kwargs.get('id', None)
        try:
            errander_obj= Errander.objects.get(id=id)
            user= errander_obj.user
            user.set_unusable_password()
            user.save()
            errander_obj.is_verified= False
            errander_obj.is_declined= True
            errander_obj.save()
            return Response({"detail":"User declined successfully"}, status=200)
        except:
            return Response({"detail":"User with this id does not exist"}, status=404)
