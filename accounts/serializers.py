from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.conf import settings



User = get_user_model()

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields= [
            'first_name',
            'last_name',
            'email',
            'phone',
            'user_type',
            'is_admin',
        ]
        extra_kwargs= {'is_super_admin':{'read_only':True}}