from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass

class Contact(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField()
    email = models.EmailField()
    id  = models.IntegerField

    def __str__(self):
        return 'Message from ' + self.name + ' - ' + self.email
