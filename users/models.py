from django.db import models
from django.contrib.auth.models import AbstractUser
import cloudinary.models

class CustomUser (AbstractUser):
    bio= models.TextField(null=True,blank=True,max_length=300)
    profile_picture=cloudinary.models.CloudinaryField('image',blank=True,null=True)
    phone= models.CharField(null=True,blank=True,max_length=16)

    def __str__(self):
        return self.username
