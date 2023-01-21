
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.conf import settings
from django.contrib.auth import get_user_model

from accounts.serializers import UserSerializer, RequestPassswordResetEmailSerializer
from accounts.utils import send_password_reset_email, decode_user_id, password_reset_token_is_valid
from operations.models import Customer, Errander


User = get_user_model()


# Authenticate
# generate token
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
            }

# Authenticate Customer
class AuthenticateCustomerView(APIView):
    permission_classes= []
    authentication_classes= []

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({"detail":"You are already authenticated"}, status= 400)
        email= request.data.get('email')
        password= request.data.get('password')
        obj= User.objects.filter(email__iexact= email)
        if obj.count()==1:
            user_obj= obj.first() 
            if user_obj.check_password(password):
                user = user_obj
                token= get_tokens_for_user(user)
                if user.user_type == 'Customer':
                    return Response({"id": user.customer.id,
                                    "token": token["access"],
                                    "user": UserSerializer(user).data,
                                    "fullname": user.fullname,
                                    "picture": user.customer.pictureURL,
                                    "is_verified": user.customer.is_verified                                          
                                    }, status=201)
                else:
                    Response({"error":"Unknown user"}, status=400)

            return Response({"error": "Invalid email or password"}, status=401)
        return Response({"error": "Invalid email or password"}, status=401)
    
# Authenticate Errander
class AuthenticateErranderView(APIView):
    permission_classes= []
    authentication_classes= []

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({"detail":"You are already authenticated"}, status= 400)
        email= request.data.get('email')
        password= request.data.get('password')
        obj= User.objects.filter(email__iexact= email)
        if obj.count()==1:
            user_obj= obj.first() 
            if user_obj.check_password(password):
                user = user_obj
                token= get_tokens_for_user(user)
                if user.user_type== 'Errander':
                    return Response({"id": user.errander.id,
                                    "token": token["access"],
                                    "user": UserSerializer(user).data,
                                    "fullname": user.fullname,
                                    "lga": user.errander.lga,
                                    "city": user.errander.city,
                                    "picture": user.errander.pictureURL,
                                    "is_verified": user.errander.is_verified,
                                    "active": user.errander.active,
                                    }, status=200)
                else:
                    Response({"error":"Unknown user"}, status=400)

            return Response({"error": "Invalid email or password"}, status=401)
        return Response({"error": "Invalid email or password"}, status=400)


# Authenticate Blogger
class AuthenticateBloggerView(APIView):
    permission_classes= []
    authentication_classes= []

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({"detail":"You are already authenticated"}, status= 400)
        email= request.data.get('email')
        password= request.data.get('password')
        obj= User.objects.filter(email__iexact= email)
        if obj.count()==1:
            user_obj= obj.first() 
            if user_obj.check_password(password):
                user = user_obj
                token= get_tokens_for_user(user)
                if user.user_type == 'Blogger':
                    return Response({
                                    "id": user.blogger.id,
                                    "token": token["access"],
                                    "user": UserSerializer(user).data, 
                                    "picture": user.blogger.pictureURL,                                        
                                    }, status=201)
                else:
                    Response({"error":"Unknown user"}, status=400)

            return Response({"error": "invalid email or password"}, status=401)
        return Response({"error": "invalid email or password"}, status=401)

# Authenticate Admin
class AuthenticateAdminView(APIView):
    permission_classes= []
    authentication_classes= []

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({"detail":"You are already authenticated"}, status= 400)
        email= request.data.get('email')
        password= request.data.get('password')
        obj= User.objects.filter(email__iexact= email)
        if obj.count()==1:
            user_obj= obj.first() 
            if user_obj.check_password(password):
                user = user_obj
                token= get_tokens_for_user(user)
                if user.user_type == 'Admin':
                    return Response({
                                    "token": token["access"],
                                    "user": UserSerializer(user).data,                                        
                                    }, status=200)
                else:
                    Response({"error":"Unknown user"}, status=400)

            return Response({"error": "invalid email or password"}, status=401)
        return Response({"error": "invalid email or password"}, status=401)

class CustomerRequestPassswordResetVew(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer= RequestPassswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email= serializer.data['email']
        user= User.objects.filter(email=email)
        if not user.exists():
            return Response({"error":"user with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        user= user.first()
        if user.user_type != "Customer":
            return Response({"error":"user with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)

        server= settings.SERVER
        password_sent= send_password_reset_email(user, request, "customer", server)
        if password_sent:
            return Response({"detail":"password reset link has been sent to your email"}, status=status.HTTP_200_OK)
        else:
            return Response({"error":"Email not sent"}, status=status.HTTP_400_BAD_REQUEST)

class ErranderRequestPassswordResetVew(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer= RequestPassswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email= serializer.data['email']
        user= User.objects.filter(email=email)
        if not user.exists():
            return Response({"error":"user with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)

        user= user.first()
        if user.user_type != "Errander":
            return Response({"error":"user with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)

        if not user.has_usable_password():
            return Response({"error":"user with this email is yet to be verified"}, status=status.HTTP_404_NOT_FOUND)

        server= settings.SERVER
        password_sent= send_password_reset_email(user, request, "errander", server)
        if password_sent:
            return Response({"detail":"password reset link has been sent to your email"}, status=status.HTTP_200_OK)
        else:
            return Response({"error":"Email not sent"}, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        user_id_encoded= request.data.get("user", None)
        token= request.data.get("token", None)
        password1= request.data.get("password1", None)
        password2= request.data.get("password2", None)

        # Check all request data are complete
        if not user_id_encoded or not token or not password1 or not password2:
            return Response({"error":"Please provide all data"}, status=status.HTTP_400_BAD_REQUEST)
        
        if password1 != password2:
            return Response({"error":"passwords don't match"}, status=status.HTTP_400_BAD_REQUEST)

        user_id= decode_user_id(user_id_encoded)
        if not user_id:
            return Response({"error":"unable to identify user"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user= User.objects.get(id= user_id)
        except:
            return Response({"error":"user does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        if not password_reset_token_is_valid(user, token):
            return Response({"error":"token not valid, please request a new one"}, status=status.HTTP_400_BAD_REQUEST)            

        user.set_password(password1)
        user.save()
        return Response({"detail":"password successfully changed"}, status=status.HTTP_200_OK)