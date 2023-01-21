from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


# image location
def image_location(instance, filename):
    return f"{instance.email}/passport/{filename}"

class MyUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, phone, user_type, password=None):      
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            first_name= first_name,
            last_name= last_name,
            email= self.normalize_email(email),
            phone= phone,
            user_type= user_type    
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            first_name= "",
            last_name= "",
            email= email,
            phone= "",
            user_type= "Admin",
            password=password,    
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# User model
class User(AbstractBaseUser):
    first_name= models.CharField(max_length=255, blank=False, null=True)
    last_name= models.CharField(max_length=255, blank=False, null=True)
    middle_name= models.CharField(max_length=255, blank=False, null=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )
    phone= models.CharField(max_length=15, blank=False, null=True)
    user_type= models.CharField(max_length=255, blank=False, null=True)
    is_admin = models.BooleanField(default=False) # a superuser

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def fullname(self):
        fullname= f"{self.last_name} {self.first_name}"
        if self.middle_name:
            fullname += f" {self.middle_name}"
        return fullname