from django.db import models
from users.models import User


class Profile(models.Model):
    name = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name