from django import forms

from auction.models import Item, Auction


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ["seller"]


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        # fields = "__all__"
        exclude = ["item"]