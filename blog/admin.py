from django.contrib import admin
from blog.models import Blogger, Post, Comment


class BloggerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',)

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'blogger', 'title', 'timestamp')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'timestamp')



# Register your models here.
admin.site.register(Blogger, BloggerAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)