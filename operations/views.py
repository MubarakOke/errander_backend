from accounts.views import AuthenticateView
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from datetime import date, datetime
from datetime import timedelta
from threading import Thread

from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, CreateAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
import jwt

from accounts.permissions import SuperuserPermissionOnly, CreatePermissionOnly, OrderCreatorOrUpdatePermission, UpdatePermissionOnly
from operations.models import Customer, Errander, Order, Stock
from . import serializers

# Email sending on another thread
class EmailThread(Thread):
    def __init__(self, subject, message, from_email, recipient_list, fail_silently):
        self.subject= subject
        self.message= message
        self.from_email= from_email
        self.recipient_list= recipient_list
        self.fail_silently= fail_silently
        Thread.__init__(self)
        
    def run(self):
        send_mail(self.subject, self.message, self.from_email, self.recipient_list, self.fail_silently)

User= get_user_model()

# generate password for user
def generate_password():
    characters= "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXWZ1234567890"
    password= User.objects.make_random_password(length=10, allowed_chars=characters)
    return password



# Customer views
# Create Customer View
class CustomerCreateView(CreateAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class= serializers.CustomerCreateSerializer
    permission_classes= [] #[IsAuthenticated&SuperuserPermissionOnly]

    def perform_create(self, serializer):
        customer_obj= serializer.save()
        token= str(RefreshToken.for_user(customer_obj.user).access_token)
        current_site= get_current_site(self.request).domain
        path= reverse("operations:Verify_Customer", kwargs={'token':token})
        url= f'https://{current_site}{path}'
        # Constructing email parameters
        subject= 'Verify your Email address'
        message= f'Dear {customer_obj.user.first_name}, \nWe are glad to have you on board, Click this link below to verify your your email address \n \n \n{url} \n \n \nPlease do not reply to this email. This email is not monitored'
        from_email= settings.EMAIL_HOST_USER
        recipient_list= [customer_obj.user.email]
        fail_silently=False
        # Sending email on a new thread
        email_thread= EmailThread(subject, message, from_email, recipient_list, fail_silently)
        email_thread.start()
class CustomerVerifyView(APIView):
    permission_classes= []
    def get(self, request, *args, **kwargs):
        token= kwargs.get('token')
        try:
            decode_token= jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
            user_email= decode_token.get("user_id")
            customer_obj= Customer.objects.get(user__email=user_email)
            customer_obj.is_verified=True
            customer_obj.save()
            return Response({"details":"Email verified successfully"}, status=200)
        except jwt.exceptions.ExpiredSignatureError:
            return Response({"details":"Token expired"}, status=401)
        except jwt.exceptions.DecodeError:
            return Response({"details":"Token cannot be decoded"}, status=404)

    

# List Customer View
class CustomerListView(ListAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class= serializers.CustomerListSerializer
    permission_classes= [] #[IsAuthenticated&SuperuserPermissionOnly]
    queryset= Customer.objects.all()
    search_fields= ('user_email', 'user_first_name', 'user_last_name')

# Detail Customer View
class CustomerDetailView(UpdateModelMixin, DestroyModelMixin, RetrieveAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
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

# Create Errander View
class ErranderCreateView(CreateAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    serializer_class= serializers.ErranderCreateSerializer
    permission_classes= [] #[IsAuthenticated&SuperuserPermissionOnly]


# List Errander View
class ErranderRequestedListView(ListAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    serializer_class= serializers.ErranderListSerializer
    permission_classes= [] #[IsAuthenticated&SuperuserPermissionOnly]
    queryset= Errander.objects.filter(is_verified= False, is_declined=False, user__is_admin=False)
    search_fields= ('user_email', 'user_first_name', 'user_last_name')

# List Verified Errander view
class ErranderVerifiedListView(ListAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    serializer_class= serializers.ErranderListSerializer
    permission_classes= [] #[IsAuthenticated&SuperuserPermissionOnly]
    queryset= Errander.objects.filter(is_verified= True)
    search_fields= ('user_email', 'user_first_name', 'user_last_name')

# List Declined Errander View
class ErranderDeclinedListView(ListAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    serializer_class= serializers.ErranderListSerializer
    permission_classes= [] #[IsAuthenticated&SuperuserPermissionOnly]
    queryset= Errander.objects.filter(is_declined= True)
    search_fields= ('user_email', 'user_first_name', 'user_last_name')

# Detail Errander View
class ErranderDetailView(UpdateModelMixin, DestroyModelMixin, RetrieveAPIView):
    parser_classes = ( JSONParser, MultiPartParser, FormParser)
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

# Verify Errander View
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
                    errander_obj.is_verified= True
                    errander_obj.is_declined= False
                    user.save()
                    errander_obj.save()
                    email_thread= EmailThread(subject, message, from_email, recipient_list, fail_silently)
                    email_thread.start()
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

# Decline Errander View
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

# Craete Order View
class OrderCreateView(CreateAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class= serializers.OrderSerializer
    permission_classes= [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer)


# List Initiated and Running Order View
class OrderInitiatedandRunningListView(ListAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class= serializers.OrderListSerializer
    permission_classes= [IsAuthenticated]
    def get_queryset(self):
        user=self.request.user
        try:
            if user.user_type=="Admin":
                return Order.objects.all().exclude(status="completed").order_by('-timestamp')
            elif user.user_type=="Errander":
                return Order.objects.all().filter(status="initiated").order_by('-timestamp')
            elif user.user_type=="Customer":
                return user.customer.order.all().exclude(status="completed").order_by('-timestamp')
            else:
                return ""
        except:
            return ""

# List Completed Order View
class OrderCompletedListView(ListAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class= serializers.OrderListSerializer
    permission_classes= [IsAuthenticated]
    def get_queryset(self):
        user=self.request.user
        try:
            if user.user_type=="Admin":
                return Order.objects.all().filter(status="completed").order_by('-timestamp')
            elif user.user_type=="Errander":
                return user.errander.order.all().filter(status="completed").order_by('-timestamp')
            elif user.user_type=="Customer":
                return user.customer.order.all().filter(status="completed").order_by('-timestamp')
            else:
                return ""
        except:
            return ""

# List Running Order View 
class OrderRunningListView(ListAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class= serializers.OrderListSerializer
    permission_classes= [IsAuthenticated]
    def get_queryset(self):
        user=self.request.user
        try:
            if user.user_type=="Admin":
                return Order.objects.all().filter(status="running").order_by('-timestamp')
            elif user.user_type=="Errander":
                return user.errander.order.all().filter(status="running").order_by('-timestamp')
            elif user.user_type=="Customer":
                return user.customer.order.all().filter(status="running").order_by('-timestamp')
            else:
                return ""
        except:
            return ""

# Update Order View 
class OrderUpdateView(UpdateModelMixin, DestroyModelMixin, RetrieveAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class= serializers.OrderSerializer
    permission_classes= [OrderCreatorOrUpdatePermission&IsAuthenticated]
    queryset= Order.objects.all()
    lookup_field= 'id'

    def perform_update(self, serializer):
        serializer.save(errander=self.request.user.errander)


    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, kwargs)

    def delete(self, request, *args, **kwargs):
        id= kwargs.get("id")
        order_obj= Order.objects.get(id==id)
        if (order_obj.status=="running"):
            return Response({"details":"Order already started, it can't be cancelled"})
        return self.destroy(request, *args, **kwargs)


# Admin Monitor Opperation View
class MonitorOperationView(APIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    permission_classes= [] #IsAuthenticated&SuperuserPermissionOnly]
    def get(self, request, *args, **kwargs):
        active_errander= Errander.objects.filter(active=True).distinct() 
        active_errander_count= active_errander.count()
        completed_order= Order.objects.filter(date_completed=date.today(), status="completed")
        completed_order_count= completed_order.count()
        active_customer= Customer.objects.filter(order__date_completed=date.today(), order__status="running").distinct()
        # completed_order= Order.objects.filter(date__gte=date.today()-timedelta(days=2), status="completed")

        
        return Response({'active_errander_count':active_errander_count,
                         'completed_order_count': completed_order_count,
                         'active_errander': serializers.ErranderListSerializer(active_errander, many=True).data,
                         'active_customer':serializers.CustomerListSerializer(active_customer, many=True).data}, status=200)


# Admin History View
class HistoryView(ListAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class= serializers.OrderListSerializer
    permission_classes= [] #IsAuthenticated]
    def get_queryset(self):
        if self.request.GET.get('date', None):
            date_param= self.request.GET.get('date')
            date_obj= datetime.strptime(date_param, '%Y-%m-%d').date()
            return Order.objects.filter(date_completed= date_obj).order_by("-timestamp")
        elif self.request.GET.get('week', None):
            week= float(self.request.GET.get('week'))
            return Order.objects.filter(date_completed__gte= date.today()-timedelta(weeks=week)).order_by("-timestamp")
        else:
            return Order.objects.filter(date_completed=date.today()).order_by("-timestamp")











# class OrderCreateListView(CreateModelMixin, ListAPIView):
#     parser_classes = (JSONParser, MultiPartParser, FormParser)
#     serializer_class= serializers.OrderSerializer
#     permission_classes= [IsAuthenticated]
#     def get_queryset(self):
#         user=self.request.user
#         try:
#             if user.user_type=="Admin":
#                 return Order.objects.all().order_by('-timestamp')
#             elif user.user_type=="Errander":
#                 return user.errander.order.all().order_by('-timestamp')
#             elif user.user_type=="Customer":
#                 return user.customer.order.all().order_by('-timestamp')
#             else:
#                 return ""
#         except:
#             return ""

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

#     def perform_create(self, serializer):
#         serializer.save(customer=self.request.user.customer)