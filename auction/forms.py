from datetime import datetime
import pytz

from django import forms

from auction.models import Item, Auction, PRICE_DECIMAL_PLACES, MAX_PRICE_DIGITS


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ["seller", "on_auction"]


class AuctionForm(forms.ModelForm):
    form_end_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}))
    form_end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Auction
        fields = ["entry_price"]

    def save(self, commit=True):
        auction = super(AuctionForm, self).save(commit=False)
        auction.entry_price = self.cleaned_data["entry_price"]
        form_end_date = self.cleaned_data["form_end_date"]
        form_end_time = self.cleaned_data["form_end_time"]
        t = datetime.combine(form_end_date, form_end_time)
        t = pytz.utc.localize(t)
        auction.end_time = t
        return auction


class BidForm(forms.Form):
    price = forms.DecimalField(decimal_places=PRICE_DECIMAL_PLACES, max_digits=MAX_PRICE_DIGITS)
