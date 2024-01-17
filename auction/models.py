from datetime import datetime, timedelta
import pytz
from django.core.validators import MinValueValidator

from django.db import models
from django.db.models.signals import post_init, post_save
from django.dispatch import receiver
import threading
from time import sleep

from background_task import \
    background  # install: pip install django4-background-tasks AND python manage.py process_tasks

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
    entry_price = models.DecimalField(decimal_places=PRICE_DECIMAL_PLACES, max_digits=MAX_PRICE_DIGITS,
                                      validators=[MinValueValidator(0, 'Entry price cannot be negative.')])
    current_price = models.DecimalField(decimal_places=PRICE_DECIMAL_PLACES, max_digits=MAX_PRICE_DIGITS,
                                        default=0)
    # optional currency
    active = models.BooleanField(default=True)
    current_bidder = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    bidder = models.ManyToManyField(User, related_name='bidders_auctions')

    def save(self, *args, **kwargs):
        # Set on_auction to True in the corresponding Item
        first_save = False
        if not self.pk:
            first_save = True
            self.item.on_auction = True
            self.item.save()
        super().save(*args, **kwargs)
        if first_save:
            # timedelta needed (timezone difference in execution)
            close_auction(schedule=self.end_time - timedelta(hours=1), auction_id=self.id)

    def check_auction(self):
        # This method can be called to close the auction
        print(pytz.utc.localize(datetime.now()))
        # TODO "if" statement is not needed (optional if (sleep) in end_auction)
        if self.active and self.end_time <= pytz.utc.localize(datetime.now()):
            self.item.on_auction = False
            self.item.save()
            self.active = False
            self.save()

    def bid(self, price, bidder):
        if not self.active:
            return 'This auction is not active.'
        if self.end_time <= pytz.utc.localize(datetime.now()):
            return 'This auction has expired.'
        if price <= self.current_price:
            return 'The price must be higher than current price.'
        if price < self.entry_price:
            return 'The price must be higher than entry price.'
        if price == 0:
            return 'The price must be higher than 0.'
        if bidder == self.current_bidder:
            return 'You are the current bidder.'
        if bidder == self.item.seller:
            return 'You cannot bid your own auctions.'
        self.current_price = price
        if bidder not in self.bidder.all():
            self.bidder.add(bidder)
        self.current_bidder = bidder
        self.save()
        return None


@background
def close_auction(auction_id):
    print("closing auction...")
    auction = Auction.objects.get(id=auction_id)
    auction.check_auction()


# @receiver(post_save, sender=Auction)
def run_auction_closing_process(sender, instance, **kwargs):
    # Check if the auction is finished and update on_auction accordingly
    if not instance.active:
        return
    end_time = instance.end_time
    close_auction(schedule=end_time, auction_id=instance.id)

    # Optionally possible solve with Threads
    # start_time = instance.start_time
    # thread = threading.Thread(target=end_auction, args=(start_time, end_time, instance))
    # print("Thread started")
    # print(pytz.utc.localize(datetime.now()))
    # thread.start()


# optional solution
def convert_to_seconds(start_time, end_time):
    delta = (end_time - start_time)
    if delta.total_seconds() < 0:
        return 0
    return delta.total_seconds()


def end_auction(start_time, end_time, auction):
    seconds_to_sleep = convert_to_seconds(start_time, end_time)
    print("counting seconds_to_sleep")
    sleep(seconds_to_sleep)
    print("woke up")
    auction.check_auction()
    print("finished auction")
    print(pytz.utc.localize(datetime.now()))
