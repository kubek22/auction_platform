from django.db import models

from user.models import User


# Create your models here.


class Item(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256, blank=True, default='')
    photo = models.ImageField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE)


class Auction(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    entry_price = models.DecimalField(decimal_places=2, max_digits=10)
    #currency
    active = models.BooleanField()