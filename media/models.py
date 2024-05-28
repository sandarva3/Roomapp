from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.exceptions import ValidationError

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=30, unique=True)
    # Add a unique=True argument to the username field
    username = models.CharField(max_length=150, unique=True)
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True
    )
    def __str__(self):
        return self.username

class Item(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=255)
    number = models.IntegerField()
    is_purchased = models.BooleanField(default=False)
    notpurchased = models.BooleanField(default=False)
    date = models.DateField(default=None, null=True)

    def __str__(self):
        return self.text

class Whole(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=255)
    number = models.IntegerField()
    date = models.DateField(default=None, null=True)
    event_id = models.IntegerField(null=True)

    def __str__(self):
        return self.text
