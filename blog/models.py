from django.db import models
from django.contrib.auth import get_user_model
from operations.models import Customer

User= get_user_model()

def blog_image_location(instance, filename):
    return f"Aservices/blog/{instance.title[10]}/photo/{filename}"
# Create your models here.

class Blogger(models.Model):  
    user= models.OneToOneField(User, blank=True, on_delete= models.CASCADE, related_name="blogger")  
    
    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"

class Post(models.Model): 
    blogger= models.ForeignKey(Blogger, on_delete=models.SET_NULL, blank=True, null=True, related_name="post")
    title= models.CharField(max_length=250, blank=True, null=True)
    content= models.TextField(blank=True, null=True)
    picture= models.ImageField(upload_to=blog_image_location, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,)
    timestamp = models.DateTimeField(auto_now=True,)
    draft= models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Comment(models.Model): 
    post= models.ForeignKey(Post, on_delete=models.SET_NULL, blank=True, null=True, related_name="comment")
    user= models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="comment")
    content= models.TextField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True,)
    timestamp = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.id