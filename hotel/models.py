from django.db import models
from django.contrib.auth.models import User  

# Create your models here.
class Message(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    message = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.user.username} - {self.message if self.message else 'No message yet'}"