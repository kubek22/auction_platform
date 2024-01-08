from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

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
    # TODO an item can be only on one auction in the same time
    on_auction = models.BooleanField(default=False)


class Auction(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    entry_price = models.DecimalField(decimal_places=PRICE_DECIMAL_PLACES, max_digits=MAX_PRICE_DIGITS)
    current_price = models.DecimalField(decimal_places=PRICE_DECIMAL_PLACES, max_digits=MAX_PRICE_DIGITS,
                                        default=0)
    # TODO optional currency
    active = models.BooleanField(default=True)
    # TODO after deactivation, set Item.on_auction to false

    def save(self, *args, **kwargs):
        # Set on_auction to True in the corresponding Item
        if not self.pk:
            self.item.on_auction = True
            self.item.save()
        super().save(*args, **kwargs)

    def close_auction(self):
        # This method can be called to close the auction
        if self.end_time < timezone.now():
            self.item.on_auction = False
            self.item.save()
            self.active = False
            self.save()


@receiver(post_save, sender=Auction)
def check_auction_status(sender, instance, **kwargs):
    # Check if the auction is finished and update on_auction accordingly
    instance.close_auction()
