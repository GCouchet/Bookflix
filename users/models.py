from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator

class User(AbstractUser):
    age= models.PositiveIntegerField(null=True, validators=[MaxValueValidator(99)])
    credit_Card= models.IntegerField(null=True)
    expired_Card = models.DateField(null=True)
    secCode_Card = models.CharField(null=True, max_length=30)

    def __str__(self):
        return self.username