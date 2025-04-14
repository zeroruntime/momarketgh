from django.db import models
from accounts.models import User

class AdminActivity(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.TextField()
    target_type = models.CharField(max_length=50)
    target_id = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)