from django.urls import path
from .views import (BloggerCreateListView, BloggerListView, BloggerDetailView, 
                    PostCreateView, PostListView, PostPublishListView, PostDetailView,
                    CommentCreateView, CommentListView, CommentDetailView)
                    

app_name= 'blog'

urlpatterns = [
    # blogger 
    path('blogger/', BloggerCreateListView.as_view(), name='Create_Blogger'),
    path('blogger/list/', BloggerListView.as_view(), name='List_Blogger'),
    path('blogger/<int:id>/', BloggerDetailView.as_view(), name='Detail_Blogger'),
    # post
    path('post/', PostCreateView.as_view(), name='Create_Post'),
    path('post/list/', PostListView.as_view(), name='List_Post'),
    path('post/publish/list/', PostPublishListView.as_view(), name='List_Published_Post'),
    path('post/<int:id>/', PostDetailView.as_view(), name='Detail_Post'),
    # comment
    path('comment/', CommentCreateView.as_view(), name='Create_Comment'),
    path('comment/list/', CommentListView.as_view(), name='List_Comment'),
    path('comment/<int:id>/', CommentDetailView.as_view(), name='Detail_Comment'),
    
]