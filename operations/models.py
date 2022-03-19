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
    is_verified= models.BooleanField(default=False)
    
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
    is_verified= models.BooleanField(default=False)
    is_declined= models.BooleanField(default=False)

    active= models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"


# Order model
class Order(models.Model):
    customer= models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, related_name="order")
    errander= models.ForeignKey(Errander, on_delete=models.SET_NULL, blank=True, null=True, related_name='order')
    created_at = models.DateTimeField(auto_now_add=True,)
    timestamp = models.DateTimeField(auto_now=True,)
    date_created= models.DateField(auto_now_add=True)
    date_completed= models.DateField(auto_now=True)
    status= models.CharField(max_length=50, blank=True, null=True)
    address= models.CharField(max_length=150, blank=True, null=True)
    relevant_detail= models.TextField(blank=True, null=True)
    preferred_shop= models.CharField(max_length=150, blank=True, null=True)
    preferred_shop_location= models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f"Order {self.id} by {self.customer.user.first_name}"


# Stock model
class Stock(models.Model): 
    name= models.CharField(max_length=255, blank=True, null=True)
    quantity= models.IntegerField(blank=True, null=True)
    price= models.FloatField(blank=True, null=True)
    order= models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True, related_name='stock')
    customer= models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, related_name="stock")


    def __str__(self):
        return self.name



