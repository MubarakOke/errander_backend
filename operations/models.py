from django.db import models
from django.contrib.auth import get_user_model

User= get_user_model()


#  File location naming
def customer_image_location(instance, filename):
    return f"Aservices/Customer/{instance.user.email}/photo/{filename}"

def errander_image_location(instance, filename):
    return f"Aservices/Errander/{instance.user.email}/photo/{filename}"



# Create your models here.

# Customer Model
class Customer(models.Model):  
    user= models.OneToOneField(User, blank=True, on_delete= models.CASCADE, related_name="customer")  
    picture= models.ImageField(upload_to=customer_image_location, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"



# Errander model
class Errander(models.Model):
    # Personal information fields
    user= models.OneToOneField(User, blank=True, on_delete= models.CASCADE, related_name="errander")
    address= models.CharField(max_length=150, blank=True, null=True)
    lga= models.CharField(max_length=150, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    gender= models.CharField(max_length=50, blank=True, null=True)
    date_of_birth= models.DateField(blank=True, null=True)
    education_qualification= models.CharField(max_length=150, blank=True, null=True)
    internet_usage= models.CharField(max_length=50, blank=True, null=True)
    skill= models.TextField(blank=True, null=True)
    deadline_handling= models.TextField(blank=True, null=True)
    project= models.TextField(blank=True, null=True)
    expectation= models.TextField(blank=True, null=True)
    relevant_information=models.TextField(blank=True, null=True)
    interest= models.TextField(blank=True, null=True)
    familiar_location=models.TextField(blank=True, null=True)
    picture= models.ImageField(upload_to=errander_image_location, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_declined = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"