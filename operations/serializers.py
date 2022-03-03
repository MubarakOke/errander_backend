from rest_framework import serializers
from operations.models import Customer
from accounts.serializers import UserSerializer
from django.contrib.auth import get_user_model
from operations.models import Customer, Errander
from django.conf import settings

User = get_user_model()

# Customer Serializer
# Create Customer Serailizer
class CustomerCreateSerializer(serializers.ModelSerializer):
    user= UserSerializer(read_only=True)
    first_name= serializers.CharField(write_only=True, required=False)
    last_name= serializers.CharField(write_only=True, required=False)
    email= serializers.EmailField(write_only=True, required=True)
    phone= serializers.CharField(write_only=True, required=False)
    password= serializers.CharField(write_only=True, required=True)
    confirm_password= serializers.CharField(write_only=True, required=True)
    class Meta:
        model= Customer
        fields= [
                'id',
                'user',
                'first_name', 
                'last_name',
                'email',
                'phone',
                'picture',
                'password',
                'confirm_password',
                ]

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"details":"password does not match"})
        return data

    def create(self, validated_data):
        first_name= validated_data.pop('first_name', None)
        last_name= validated_data.pop('last_name', None)
        email= validated_data.pop('email', None)
        phone= validated_data.pop('phone', None)
        password= validated_data.pop('password', None)

        # Create user object for admin instance
        user_obj= User.objects.create(
                                    first_name= first_name,
                                    last_name= last_name,
                                    email= email,
                                    phone= phone
                                    )
        user_obj.user_type= "Customer"
        user_obj.set_password(password)
        user_obj.save()

        customer_obj = Customer.objects.create(user=user_obj,
                                            picture=validated_data.get('picture', None),       
                                        )
        customer_obj.save()
        return customer_obj

# Update Customer Serializer
class CustomerUpdateSerializer(serializers.ModelSerializer):
    user= UserSerializer(read_only=True)
    first_name= serializers.CharField(write_only=True, required=False)
    last_name= serializers.CharField(write_only=True, required=False)
    email= serializers.EmailField(write_only=True, required=False)
    phone= serializers.CharField(write_only=True, required=False)
    password= serializers.CharField(write_only=True, required=False)
    class Meta:
        model= Customer
        fields= [
                'id',
                'user',
                'first_name', 
                'last_name',
                'email',
                'phone',
                'picture',
                'password'
                ]

    def update(self, instance, validated_data):
        instance.user.first_name = validated_data.get('first_name', instance.user.first_name)
        instance.user.last_name= validated_data.get('last_name', instance.user.last_name)
        instance.user.email= validated_data.get('email', instance.user.email)
        instance.user.phone= validated_data.get('phone', instance.user.phone)
        instance.user.set_password(validated_data.get('password', instance.user.password))
        instance.user.save()
        instance.picture= validated_data.get('picture', instance.picture)
        instance.save()
        return instance


# Errander Serializer
# Create Errander Serializer
class ErranderCreateSerializer(serializers.ModelSerializer):
    user= UserSerializer(read_only=True)
    first_name= serializers.CharField(write_only=True, required=False)
    last_name= serializers.CharField(write_only=True, required=False)
    email= serializers.EmailField(write_only=True, required=True)
    phone= serializers.CharField(write_only=True, required=False)
    date_of_birth = serializers.DateField(input_formats=settings.DATE_INPUT_FORMATS, required=False)
    class Meta:
        model= Errander
        fields= [
                'id',
                'user',
                'first_name', 
                'last_name',
                'email',
                'phone',
                'address',
                'lga',
                'city',
                'gender',
                'date_of_birth',
                'education_qualification',
                'internet_usage',
                'skill',
                'deadline_handling',
                'project',
                'expectation',
                'relevant_information',
                'interest',
                'familiar_location',
                'picture',
                'is_verified',
                'is_declined'
                ]
    
    def create(self, validated_data):
        first_name= validated_data.pop('first_name', None)
        last_name= validated_data.pop('last_name', None)
        email= validated_data.pop('email', None)
        phone= validated_data.pop('phone', None)

        # Create user object for errander instance
        user_obj= User.objects.create(
                                    first_name= first_name,
                                    last_name= last_name,
                                    email= email,
                                    phone= phone
                                    )
        user_obj.user_type= "Errander"
        user_obj.save()

        errander_obj = Errander.objects.create(user=user_obj,
                                            address=validated_data.get('address', None),
                                            lga=validated_data.get('lga', None),
                                            city=validated_data.get('city', None),
                                            gender=validated_data.get('gender', None),
                                            date_of_birth=validated_data.get('date_of_birth', None),
                                            education_qualification=validated_data.get('education_qualification', None),
                                            internet_usage=validated_data.get('internet_usage', None),
                                            skill=validated_data.get('skill', None),
                                            deadline_handling=validated_data.get('deadline_handling', None),
                                            project=validated_data.get('project', None),
                                            expectation=validated_data.get('expectation', None),
                                            relevant_information=validated_data.get('relevant_information', None),
                                            interest=validated_data.get('interest', None),
                                            familiar_location=validated_data.get('familiar_location', None),
                                            picture=validated_data.get('picture', None),       
                                            )
        errander_obj.save()
        return errander_obj

# Update Errander Serializer
class ErranderUpdateSerializer(serializers.ModelSerializer):
    user= UserSerializer(read_only=True)
    first_name= serializers.CharField(write_only=True, required=False)
    last_name= serializers.CharField(write_only=True, required=False)
    email= serializers.EmailField(write_only=True, required=False)
    phone= serializers.CharField(write_only=True, required=False)
    date_of_birth = serializers.DateField(input_formats=settings.DATE_INPUT_FORMATS, required=False)
    password= serializers.CharField(write_only=True, required=False)
    class Meta:
        model= Errander
        fields= [
                'id',
                'user',
                'first_name', 
                'last_name',
                'email',
                'phone',
                'address',
                'lga',
                'city',
                'gender',
                'date_of_birth',
                'education_qualification',
                'internet_usage',
                'skill',
                'deadline_handling',
                'project',
                'expectation',
                'relevant_information',
                'interest',
                'familiar_location',
                'picture',
                'password',
                'is_verified',
                'is_declined',
                ]

    def update(self, instance, validated_data):
        instance.user.first_name = validated_data.get('first_name', instance.user.first_name)
        instance.user.last_name= validated_data.get('last_name', instance.user.last_name)
        instance.user.email= validated_data.get('email', instance.user.email)
        instance.user.phone= validated_data.get('phone', instance.user.phone)
        instance.user.set_password(validated_data.get('password', instance.user.password))
        instance.user.save()  
        instance.lga=validated_data.get('lga', instance.lga)
        instance.city=validated_data.get('city', instance.city)
        instance.gender=validated_data.get('gender', instance.gender)
        instance.date_of_birth=validated_data.get('date_of_birth', instance.date_of_birth)
        instance.education_qualification=validated_data.get('education_qualification', instance.education_qualification)
        instance.internet_usage= validated_data.get('internet_usage', instance.internet_usage)
        instance.skill= validated_data.get('skill', instance.skill)
        instance.deadline_handling= validated_data.get('deadline_handling', instance.deadline_handling)
        instance.project= validated_data.get('project', instance.project)
        instance.expectation= validated_data.get('expectation', instance.expectation)
        instance.relevant_information= validated_data.get('relevant_information', instance.relevant_information)
        instance.interest=validated_data.get('interest', instance.interest)
        instance.familiar_location=validated_data.get('familiar_location', instance.familiar_location)
        instance.picture= validated_data.get('picture', instance.picture)
        instance.save()
        return instance


