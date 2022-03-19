from rest_framework import serializers
from operations.models import Customer
from accounts.serializers import UserSerializer
from django.contrib.auth import get_user_model
from operations.models import Customer, Errander, Order, Stock
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

# Authenticate
# generate token
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
            }

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
    token= serializers.SerializerMethodField(read_only=True)
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
                'token',
                'is_verified',
                ]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError({"details":"Email already exist"})
        return value

    def get_token(self, obj):
        user= obj.user
        token= get_tokens_for_user(user)
        return token["access"]

    def create(self, validated_data):
        # Create user object for admin instance
        user_obj= User.objects.create(
                                    first_name= validated_data.pop('first_name', None),
                                    last_name= validated_data.pop('last_name', None),
                                    email= validated_data.pop('email', None),
                                    phone= validated_data.pop('phone', None)
                                    )
        user_obj.user_type= "Customer"
        user_obj.set_password(validated_data.pop('password', None))
        user_obj.save()

        customer_obj = Customer.objects.create(user=user_obj,
                                               picture=validated_data.get('picture', None),       
                                              )
        customer_obj.save()

        return customer_obj


# List Customer Serializer
class CustomerListSerializer(serializers.ModelSerializer):
    user= UserSerializer(read_only=True)
    class Meta:
        model= Customer
        fields= [
                'id',
                'user',
                'picture',
                'is_verified',
                ]

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
# Plain errander serializer
class ErranderListSerializer(serializers.ModelSerializer):
    user= UserSerializer(read_only=True)
    class Meta:
        model= Errander
        fields= [
                'id',
                'user',
                'is_verified',
                'is_declined',
                'active',
                ]

# Create Errander Serializer
class ErranderCreateSerializer(serializers.ModelSerializer):
    user= UserSerializer(read_only=True)
    first_name= serializers.CharField(write_only=True, required=False)
    last_name= serializers.CharField(write_only=True, required=False)
    email= serializers.EmailField(write_only=True, required=True)
    phone= serializers.CharField(write_only=True, required=False)
    date_of_birth = serializers.DateField(input_formats=settings.DATE_INPUT_FORMATS, required=False)
    token= serializers.SerializerMethodField(read_only=True)
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
                'is_declined',
                'active',
                'token',
                ]
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError({"details":"Email already exist"})
        return value
    
    def get_token(self, obj):
        user= obj.user
        token= get_tokens_for_user(user)
        return token["access"]

    def create(self, validated_data):
        # Create user object for errander instance
        user_obj= User.objects.create(
                                    first_name= validated_data.pop('first_name', None),
                                    last_name= validated_data.pop('last_name', None),
                                    email= validated_data.pop('email', None),
                                    phone= validated_data.pop('phone', None)
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
                'active',
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

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model= Stock
        fields= [
                'id',
                'name',
                'quantity',
                'price',
                'order',
                'customer'
                ]



class OrderListSerializer(serializers.ModelSerializer):
    stock= serializers.SerializerMethodField(read_only=True)
    customer_name= serializers.SerializerMethodField(read_only=True)
    errander_name= serializers.SerializerMethodField(read_only=True)
    customer= CustomerListSerializer()
    errander= ErranderListSerializer()

    class Meta:
        model= Order
        fields= [
                'id',
                'created_at',
                'timestamp',
                'date_created',
                'date_completed',
                'status',
                'address',
                'relevant_detail',
                'preferred_shop',
                'preferred_shop_location',
                'stock',
                'customer_name',
                'customer',
                'errander_name',
                'errander',
                ]

    def get_stock(self, obj):
        return StockSerializer(obj.stock, many=True).data

    def get_customer_name(self, obj):
        try:
            return obj.customer.user.last_name+" "+ obj.customer.user.first_name
        except:
            return "" 
    
    def get_errander_name(self, obj):
        try:
            return obj.errander.user.last_name+" "+ obj.errander.user.first_name
        except:
            return ""
    

# Create and Update Order Serializer
class OrderSerializer(serializers.ModelSerializer):
    stock_list= serializers.ListField(write_only=True, required=False)
    stock= serializers.SerializerMethodField(read_only=True)
    customer= CustomerListSerializer(read_only=True)
    errander= ErranderListSerializer(read_only=True)
    class Meta:
        model= Order
        fields= [
                'id',
                'created_at',
                'timestamp',
                'date_created',
                'date_completed',
                'status',
                'address',
                'relevant_detail',
                'preferred_shop',
                'preferred_shop_location',
                'stock_list',
                'stock',
                'customer',
                'errander',
                ]
    

    def get_stock(self, obj):
        return StockSerializer(obj.stock, many=True).data

    def create(self, validated_data):
        order_obj= Order.objects.create(customer=validated_data.get('customer', None),
                                        errander=validated_data.get('errander', None),
                                        address=validated_data.get('address', None),
                                        relevant_detail=validated_data.get('relevant_detail', None),
                                        preferred_shop= validated_data.get('preferred_shop'),  
                                        preferred_shop_location= validated_data.get('preferred_shop_location')                                       
                                        )
        order_obj.status= "initiated"
        order_obj.save()

        if validated_data.get("stock_list", None):
            stock_data = validated_data.pop('stock_list')
            for stock in stock_data:
                stock_obj= Stock.objects.create(name=stock['name'],
                                                quantity=stock['quantity'],
                                                price= stock['price'],
                                                customer=order_obj.customer,
                                                order= order_obj)
                stock_obj.save()
                    
        return order_obj
    
    def update(self, instance, validated_data):
        requested_errander= validated_data.get("errander")
        if requested_errander.active:
            if not validated_data.get("status") == 'completed':
              raise serializers.ValidationError({"details":"You are currently busy, please finish up the task"})
        instance.errander= validated_data.get("errander", instance.errander)
        instance.status= validated_data.get("status", instance.status)
        if validated_data.get("status")=="running":
            instance.errander.active= True
            instance.errander.save()
        if validated_data.get("status")=="completed":
            instance.errander.active= False
            instance.errander.save()
        instance.save()
        return instance