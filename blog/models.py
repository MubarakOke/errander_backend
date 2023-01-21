from datetime import datetime
from time import timezone
from django.db import models
from django.contrib.auth import get_user_model
from operations.models import Customer

User= get_user_model()

def blog_image_location(instance, filename):
    title= instance.title
    if len(instance.title) > 10:
        title= instance.title[10]
    return f"Aservices/blog/{title}/photo/{filename}"

def blogger_image_location(instance, filename):
    return f"Aservices/blogger/{instance.user.email}/photo/{filename}"
# Create your models here.

class Blogger(models.Model):  
    user= models.OneToOneField(User, blank=True, on_delete= models.CASCADE, related_name="blogger") 
    picture= models.ImageField(upload_to=blogger_image_location, blank=True, null=True) 

    @property
    def pictureURL(self):
        if self.picture:
            return self.picture.url
        return None
    
    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"
    
    class Meta:
        ordering= ("-user__id",)

class Post(models.Model): 
    blogger= models.ForeignKey(Blogger, on_delete=models.SET_NULL, blank=True, null=True, related_name="post")
    title= models.CharField(max_length=250, blank=False, null=False, default="")
    content= models.TextField(blank=True, null=True)
    picture= models.ImageField(upload_to=blog_image_location, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,)
    timestamp = models.DateTimeField(auto_now=True,)
    date= models.DateField(auto_now=True)
    draft= models.BooleanField(default=True)

    class Meta:
        ordering= ['-timestamp']

    def __str__(self):
        if self.title:
            return self.title
        return ""

class Comment(models.Model): 
    post= models.ForeignKey(Post, on_delete=models.SET_NULL, blank=True, null=True, related_name="comment")
    user= models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="comment")
    name= models.CharField(max_length=255, blank=False, null=False, default='anonymous')
    imageURL= models.CharField(max_length=1000, blank=True, null=True)
    content= models.TextField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True,)
    date= models.DateField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True) 

    class Meta:
        ordering= ['-timestamp']

    def __str__(self):
        return str(self.name)