from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField


class User(AbstractUser):
    age = models.PositiveIntegerField(null=True, validators=[MaxValueValidator(99)])
    pay = models.BooleanField(default=True)
    credit_Card = CardNumberField('card number')
    expired_Card = CardExpiryField('expiration date', null=True)
    secCode_Card = SecurityCodeField('security code', null=True)
    subscription = models.CharField(max_length=20)

    def _str_(self):
        return self.username


class Profile(models.Model):
    name = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
