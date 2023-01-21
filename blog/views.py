from django.shortcuts import render
from . import serializers
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, CreateAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from blog.models import Blogger, Post, Comment
from django.contrib.auth.models import AnonymousUser


from rest_framework.permissions import IsAuthenticated
from accounts.permissions import SuperuserPermissionOnly, CreatePermissionOnly, OrderCreatorOrUpdatePermission, UpdatePermissionOnly

# Create your views here.
# Blogger views
# Create Blogger View
class BloggerCreateListView(CreateAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class= serializers.BloggerCreateSerializer
    permission_classes= [] #[IsAuthenticated&SuperuserPermissionOnly]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# List Blogger View
class BloggerListView(ListAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class= serializers.BloggerListSerializer
    permission_classes= [] #[IsAuthenticated&SuperuserPermissionOnly]
    queryset= Blogger.objects.all()
    search_fields= ('user_email', 'user_first_name', 'user_last_name')



# Update Blogger View
class BloggerDetailView(UpdateModelMixin, DestroyModelMixin, RetrieveAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class= serializers.BloggerUpdateSerializer
    permission_classes= [] #[IsAuthenticated&SuperuserPermissionOnly]
    queryset= Blogger.objects.all()
    lookup_field= 'id'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)




# Post views
# Create Post View
class PostCreateView(CreateAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class= serializers.PostSerializer
    permission_classes= [] #[IsAuthenticated&SuperuserPermissionOnly]

    def perform_create(self, serializer):
        serializer.save(blogger=self.request.user.blogger)
    
# Detail Post View
class PostDetailView(UpdateModelMixin, DestroyModelMixin, RetrieveAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class= serializers.PostListPublishedSerializer
    permission_classes= [] #[IsAuthenticated&SuperuserPermissionOnly]
    queryset= Post.objects.all()
    lookup_field= 'id'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

# List Post View
class PostListView(ListAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class= serializers.PostListSerializer
    permission_classes= [] #[IsAuthenticated&SuperuserPermissionOnly]
    queryset= Post.objects.all().order_by('-timestamp')
    search_fields= ("title", "date", "draft")

# List Published Post View
class PostPublishListView(ListAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class= serializers.PostListPublishedSerializer
    permission_classes= [] #[IsAuthenticated&SuperuserPermissionOnly]
    queryset= Post.objects.filter(draft=False).order_by('-timestamp')
    search_fields= ("title", "date", "draft")


# Comment views
# Create Comment View
class CommentCreateView(CreateAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class= serializers.CommentSerializer
    permission_classes= [] #[IsAuthenticated&SuperuserPermissionOnly]

    def perform_create(self, serializer):
        if str(self.request.user) == 'AnonymousUser':
            serializer.save()
        else:
            serializer.save(user=self.request.user)
        
        
        


# List Comment View
class CommentListView(ListAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class= serializers.CommentSerializer
    permission_classes= [IsAuthenticated] #[IsAuthenticated&SuperuserPermissionOnly]
    queryset= Comment.objects.all().order_by("-timestamp")



# Detail Comment View
class CommentDetailView(UpdateModelMixin, DestroyModelMixin, RetrieveAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class= serializers.CommentSerializer
    permission_classes= [] #[IsAuthenticated&SuperuserPermissionOnly]
    queryset= Comment.objects.all()
    lookup_field= 'id'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
