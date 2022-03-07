from rest_framework import serializers
from blog.models import Blogger, Post, Comment
from accounts.serializers import UserSerializer
from django.contrib.auth import get_user_model
from operations.models import Customer
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


# Blogger Serializer
# Create Blogger Serailizer
class BloggerCreateSerializer(serializers.ModelSerializer):
    user= UserSerializer(read_only=True)
    first_name= serializers.CharField(write_only=True, required=False)
    last_name= serializers.CharField(write_only=True, required=False)
    email= serializers.EmailField(write_only=True, required=True)
    phone= serializers.CharField(write_only=True, required=False)
    password= serializers.CharField(write_only=True, required=True)
    confirm_password= serializers.CharField(write_only=True, required=True)
    class Meta:
        model= Blogger
        fields= [
                'id',
                'user',
                'first_name', 
                'last_name',
                'email',
                'phone',
                'password',
                'confirm_password',
                ]

    def get_token(self, obj):
        user= obj.user
        token= get_tokens_for_user(user)
        return token["access"]

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"details":"password does not match"})
        return data

    def create(self, validated_data):
        # Create user object for admin instance
        user_obj= User.objects.create(
                                    first_name= validated_data.pop('first_name', None),
                                    last_name= validated_data.pop('last_name', None),
                                    email= validated_data.pop('email', None),
                                    phone= validated_data.pop('phone', None),
                                    )
        user_obj.user_type= "Blogger"
        user_obj.set_password(validated_data.pop('password', None))
        user_obj.save()

        blogger_obj = Blogger.objects.create(user=user_obj)
        blogger_obj.save()
        return blogger_obj


# List Blogger Serializer
class BloggerListSerializer(serializers.ModelSerializer):
    user= UserSerializer()
    class Meta:
        model= Blogger
        fields= [
                'id',
                'user',
                ]

# Update Blogger Serializer
class BloggerUpdateSerializer(serializers.ModelSerializer):
    user= UserSerializer(read_only=True)
    first_name= serializers.CharField(write_only=True, required=False)
    last_name= serializers.CharField(write_only=True, required=False)
    email= serializers.EmailField(write_only=True, required=False)
    phone= serializers.CharField(write_only=True, required=False)
    password= serializers.CharField(write_only=True, required=False)
    class Meta:
        model= Blogger
        fields= [
                'id',
                'user',
                'first_name', 
                'last_name',
                'email',
                'phone',
                'password',
                ]

    def update(self, instance, validated_data):
        instance.user.first_name = validated_data.get('first_name', instance.user.first_name)
        instance.user.last_name= validated_data.get('last_name', instance.user.last_name)
        instance.user.email= validated_data.get('email', instance.user.email)
        instance.user.phone= validated_data.get('phone', instance.user.phone)
        instance.user.set_password(validated_data.get('password', instance.user.password))
        instance.user.save()
        instance.save()
        return instance



# Post Serializer
# Create and Update Post Serailizer
class PostSerializer(serializers.ModelSerializer):
    blogger= BloggerListSerializer(read_only=True)
    class Meta:
        model= Post
        fields= [
                'id',
                'blogger',
                'title', 
                'content',
                'picture',
                'draft',
                'created_at',
                'timestamp',
                ]

    def create(self, validated_data):
        # Create post object
        post_obj= Post.objects.create(
                                    blogger= validated_data.pop('blogger', None),
                                    title= validated_data.pop('title', None),
                                    content= validated_data.pop('content', None),
                                    picture= validated_data.pop('picture', None),
                                    draft= validated_data.get('draft', True)
                                    )
        post_obj.save()
        return post_obj
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content= validated_data.get('content', instance.content)
        instance.picture= validated_data.get('picture', instance.picture)
        instance.draft= validated_data.get('draft', instance.draft)
        instance.save()
        return instance
    

# Comment Serializer
# Create Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    post= serializers.SlugRelatedField(slug_field="id", queryset=Post.objects.all(), required=False)
    user= serializers.SlugRelatedField(slug_field="first_name", queryset=User.objects.all(), required=False)
    class Meta:
        model= Post
        fields= [
                'id',
                'post',
                'user', 
                'content',
                'created_at',
                'timestamp',
                ]

    def create(self, validated_data):
        # Create Comment object
        comment_obj= Comment.objects.create(
                                    post= validated_data.pop('post', None),
                                    user= validated_data.pop('user', None),
                                    content= validated_data.pop('content', None),
                                    )
        comment_obj.save()
        return comment_obj



# List Post Serializer
class PostListSerializer(serializers.ModelSerializer):
    blogger= BloggerListSerializer()
    comment= serializers.SerializerMethodField(read_only=True)
    class Meta:
        model= Post
        fields= [
                'id',
                'blogger',
                'title', 
                'content',
                'picture',
                'draft',
                'created_at',
                'timestamp',
                'comment',
                ]
    def get_comment(self, obj):
        return CommentSerializer(obj.comment, many=True).data

