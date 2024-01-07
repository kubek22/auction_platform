from django.db import models

from user.models import User

# Create your models here.

MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 256
PRICE_DECIMAL_PLACES = 2
MAX_PRICE_DIGITS = 10


class Item(models.Model):
    name = models.CharField(max_length=MAX_NAME_LENGTH)
    description = models.CharField(max_length=MAX_DESCRIPTION_LENGTH, blank=True, default='')
    photo = models.ImageField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE)


class Auction(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    entry_price = models.DecimalField(decimal_places=PRICE_DECIMAL_PLACES, max_digits=MAX_PRICE_DIGITS)
    # currency
    active = models.BooleanField(default=True)
