
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


from django.contrib.auth import get_user_model

from accounts.serializers import UserSerializer


User = get_user_model()


# Authenticate
# generate token
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
            }

# Authenticate User view
class AuthenticateView(APIView):
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
                    return Response({
                                    "refresh": token["refresh"], 
                                    "access_token": token["access"],
                                    "user": UserSerializer(user).data,
                                    # "picture": user.customer.picture,                                          
                                    }, status=201)
                elif user.user_type== 'Errander':
                    return Response({
                                    "refresh": token["refresh"], 
                                    "access_token": token["access"],
                                    "user": UserSerializer(user).data,
                                    "lga": user.errander.lga,
                                    "city": user.errander.city,
                                    "gender": user.errander.gender,
                                    "date_of_birth": user.errander.date_of_birth,
                                    "education_qualification": user.errander.education_qualification,
                                    "internet_usage": user.errander.internet_usage,
                                    "skill": user.errander.skill,
                                    "deadline_handling": user.errander.deadline_handling,
                                    "project": user.errander.project,
                                    "expectation": user.errander.expectation,
                                    "relevant_information": user.errander.relevant_information,
                                    "interest": user.errander.interest,
                                    "familiar_location": user.errander.familiar_location,
                                    # "picture": user.errander.picture,
                                    "is_verified": user.errander.is_verified,
                                    }, status=200)
                elif user.user_type == 'Admin':
                    return Response({
                                    "refresh": token["refresh"], 
                                    "access_token": token["access"],
                                    "user": UserSerializer(user).data,                                        
                                    }, status=200)
                else:
                    Response({"error":"Unknown user"}, status=400)

            return Response({"error": "invalid password"}, status=401)
        return Response({"error": "invalid email or password"}, status=400)