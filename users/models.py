from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField


class Membership(models.Model):
    name = models.CharField(max_length=10)
    limitProfiles = models.PositiveSmallIntegerField()
    limitActiveSessions = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class User(AbstractUser):
    age = models.PositiveIntegerField(null=True, validators=[MaxValueValidator(99)])
    pay = models.BooleanField(default=True)
    credit_Card = CardNumberField('card number')
    expired_Card = CardExpiryField('expiration date', null=True)
    secCode_Card = SecurityCodeField('security code', null=True)
    subscription = models.ForeignKey(Membership, on_delete=models.CASCADE, null=True, blank=True)

    def _str_(self):
        return self.username